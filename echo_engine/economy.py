from __future__ import annotations

import json
import threading
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from uuid import uuid4

import yaml

from echo_engine.bindings import agent_id_for_character, get_user_binding
from echo_engine.config import get_settings
from echo_engine.models import (
    EconomyAccountSummary,
    EconomyProduct,
    GhostSubscription,
    UserEntitlement,
    WalletLedgerEntry,
)
from echo_engine.store import CanonStore, atomic_write_text


CATALOG_PATH = Path("data/economy_catalog.yaml")
STATE_SCHEMA = "echo_economy_state_v1"

# 串行化钱包状态的 read-modify-write，避免并发请求下的双花 / 丢交易。
_STATE_LOCK = threading.Lock()


class EconomyError(ValueError):
    pass


def list_products(root: Path | None = None, *, include_inactive: bool = False) -> list[EconomyProduct]:
    products = sorted(_load_products(root).values(), key=lambda item: (item.category, item.id))
    if include_inactive:
        return products
    return [product for product in products if product.active]


def get_product(product_id: str, root: Path | None = None) -> EconomyProduct:
    clean_id = _clean_required(product_id, "product_id")
    product = _load_products(root).get(clean_id)
    if product is None:
        raise EconomyError(f"product not found: {clean_id}")
    if not product.active:
        raise EconomyError(f"product is inactive: {clean_id}")
    return product


def wallet_balance(user_id: str, root: Path | None = None) -> int:
    clean_user_id = _clean_required(user_id, "user_id")
    state = _load_state(root)
    return _wallet_balance_from_state(state, clean_user_id)


def record_wallet_entry(
    *,
    user_id: str,
    amount: int,
    reason: str,
    ref_id: str | None = None,
    metadata: dict[str, Any] | None = None,
    root: Path | None = None,
) -> WalletLedgerEntry:
    clean_user_id = _clean_required(user_id, "user_id")
    clean_reason = _clean_required(reason, "reason")
    if amount == 0:
        raise EconomyError("amount must not be zero")
    with _STATE_LOCK:
        state = _load_state(root)
        entry = _append_wallet_entry(
            state,
            user_id=clean_user_id,
            amount=amount,
            reason=clean_reason,
            ref_id=ref_id,
            metadata=metadata or {},
        )
        _save_state(state, root)
    return entry


def grant_entitlement(
    *,
    user_id: str,
    entitlement_type: str,
    ref_id: str,
    source: str = "manual",
    duration_days: int | None = None,
    metadata: dict[str, Any] | None = None,
    root: Path | None = None,
) -> UserEntitlement:
    clean_user_id = _clean_required(user_id, "user_id")
    with _STATE_LOCK:
        state = _load_state(root)
        entitlement = _append_entitlement(
            state,
            user_id=clean_user_id,
            entitlement_type=_clean_required(entitlement_type, "entitlement_type"),
            ref_id=_clean_required(ref_id, "ref_id"),
            source=source,
            duration_days=duration_days,
            metadata=metadata or {},
        )
        _save_state(state, root)
    return entitlement


def list_entitlements(user_id: str, root: Path | None = None) -> list[UserEntitlement]:
    clean_user_id = _clean_required(user_id, "user_id")
    state = _load_state(root)
    entitlements = [
        UserEntitlement.model_validate(raw)
        for raw in state["entitlements"]
        if raw.get("user_id") == clean_user_id
    ]
    return sorted(entitlements, key=lambda item: item.created_at, reverse=True)


def get_ghost_subscription(user_id: str, root: Path | None = None) -> GhostSubscription | None:
    clean_user_id = _clean_required(user_id, "user_id")
    raw = _load_state(root)["ghost_subscriptions"].get(clean_user_id)
    return GhostSubscription.model_validate(raw) if isinstance(raw, dict) else None


def activate_ghost_subscription(
    *,
    user_id: str,
    character_id: str | None = None,
    duration_days: int = 30,
    source: str = "manual",
    metadata: dict[str, Any] | None = None,
    root: Path | None = None,
) -> GhostSubscription:
    clean_user_id = _clean_required(user_id, "user_id")
    if duration_days <= 0:
        raise EconomyError("duration_days must be positive")
    character_ref = _resolve_character_ref(clean_user_id, character_id, root)
    with _STATE_LOCK:
        state = _load_state(root)
        subscription = _set_ghost_subscription(
            state,
            user_id=clean_user_id,
            character_id=character_ref["character_id"],
            agent_id=character_ref["agent_id"],
            duration_days=duration_days,
            source=source,
            metadata=metadata or {},
        )
        _save_state(state, root)
    return subscription


def purchase_product(
    *,
    user_id: str,
    product_id: str,
    character_id: str | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    clean_user_id = _clean_required(user_id, "user_id")
    product = get_product(product_id, root)
    with _STATE_LOCK:
        state = _load_state(root)
        balance = _wallet_balance_from_state(state, clean_user_id)
        if balance < product.price_credits:
            raise EconomyError(
                f"insufficient credits: need {product.price_credits}, balance {balance}"
            )

        grants = product.grants
        subscription_grant = _mapping_grant(grants.get("ghost_subscription"))
        character_ref = None
        if subscription_grant is not None:
            character_ref = _resolve_character_ref(clean_user_id, character_id, root)

        ledger_entry = None
        if product.price_credits:
            ledger_entry = _append_wallet_entry(
                state,
                user_id=clean_user_id,
                amount=-product.price_credits,
                reason=f"purchase:{product.id}",
                ref_id=product.id,
                metadata={"product_category": product.category},
            )

        created_entitlements: list[UserEntitlement] = []
        for grant in _list_grants(grants.get("entitlements")):
            created_entitlements.append(
                _append_entitlement(
                    state,
                    user_id=clean_user_id,
                    entitlement_type=str(grant.get("type", "")).strip(),
                    ref_id=str(grant.get("ref_id", "")).strip(),
                    source=f"purchase:{product.id}",
                    duration_days=_optional_positive_int(grant.get("duration_days")),
                    metadata={
                        "product_id": product.id,
                        **{key: value for key, value in grant.items() if key not in {"type", "ref_id"}},
                    },
                )
            )

        ghost_subscription = None
        if subscription_grant is not None and character_ref is not None:
            ghost_subscription = _set_ghost_subscription(
                state,
                user_id=clean_user_id,
                character_id=character_ref["character_id"],
                agent_id=character_ref["agent_id"],
                duration_days=_optional_positive_int(subscription_grant.get("duration_days")) or 30,
                source=f"purchase:{product.id}",
                metadata={"product_id": product.id},
            )

        wallet_credit_grant = _optional_int(grants.get("wallet_credits"))
        if wallet_credit_grant:
            _append_wallet_entry(
                state,
                user_id=clean_user_id,
                amount=wallet_credit_grant,
                reason=f"grant:{product.id}",
                ref_id=product.id,
                metadata={"product_category": product.category},
            )

        _save_state(state, root)
        wallet_balance_after = _wallet_balance_from_state(state, clean_user_id)
    return {
        "ok": True,
        "product": product.model_dump(mode="json"),
        "ledger_entry": ledger_entry.model_dump(mode="json") if ledger_entry else None,
        "entitlements": [item.model_dump(mode="json") for item in created_entitlements],
        "ghost_subscription": ghost_subscription.model_dump(mode="json")
        if ghost_subscription
        else None,
        "wallet_balance": wallet_balance_after,
    }


def fulfill_external_purchase(
    *,
    user_id: str,
    product_id: str,
    purchase_ref: str,
    character_id: str | None = None,
    source: str = "echoai_account",
    root: Path | None = None,
) -> dict[str, Any]:
    """Grant a product already paid through the official EchoAI account ledger.

    The purchase reference is persisted with the grant result, making retries safe after
    timeouts between the account service and this engine.
    """
    clean_user_id = _clean_required(user_id, "user_id")
    clean_ref = _clean_required(purchase_ref, "purchase_ref")
    product = get_product(product_id, root)
    with _STATE_LOCK:
        state = _load_state(root)
        existing = state["fulfilled_purchases"].get(clean_ref)
        if isinstance(existing, dict):
            if existing.get("user_id") != clean_user_id or existing.get("product_id") != product.id:
                raise EconomyError("purchase_ref already belongs to another purchase")
            return {**existing["result"], "duplicate": True}

        grants = product.grants
        subscription_grant = _mapping_grant(grants.get("ghost_subscription"))
        character_ref = None
        if subscription_grant is not None:
            character_ref = _resolve_character_ref(clean_user_id, character_id, root)

        created_entitlements: list[UserEntitlement] = []
        for grant in _list_grants(grants.get("entitlements")):
            created_entitlements.append(
                _append_entitlement(
                    state,
                    user_id=clean_user_id,
                    entitlement_type=str(grant.get("type", "")).strip(),
                    ref_id=str(grant.get("ref_id", "")).strip(),
                    source=f"{source}:{product.id}",
                    duration_days=_optional_positive_int(grant.get("duration_days")),
                    metadata={
                        "product_id": product.id,
                        "purchase_ref": clean_ref,
                        **{key: value for key, value in grant.items() if key not in {"type", "ref_id"}},
                    },
                )
            )

        ghost_subscription = None
        if subscription_grant is not None and character_ref is not None:
            ghost_subscription = _set_ghost_subscription(
                state,
                user_id=clean_user_id,
                character_id=character_ref["character_id"],
                agent_id=character_ref["agent_id"],
                duration_days=_optional_positive_int(subscription_grant.get("duration_days")) or 30,
                source=f"{source}:{product.id}",
                metadata={"product_id": product.id, "purchase_ref": clean_ref},
            )

        result = {
            "ok": True,
            "product": product.model_dump(mode="json"),
            "entitlements": [item.model_dump(mode="json") for item in created_entitlements],
            "ghost_subscription": ghost_subscription.model_dump(mode="json")
            if ghost_subscription
            else None,
        }
        state["fulfilled_purchases"][clean_ref] = {
            "user_id": clean_user_id,
            "product_id": product.id,
            "result": result,
        }
        _save_state(state, root)
    return {**result, "duplicate": False}


def economy_account_summary(user_id: str, root: Path | None = None) -> EconomyAccountSummary:
    clean_user_id = _clean_required(user_id, "user_id")
    return EconomyAccountSummary(
        user_id=clean_user_id,
        wallet_balance=wallet_balance(clean_user_id, root),
        entitlements=list_entitlements(clean_user_id, root),
        ghost_subscription=get_ghost_subscription(clean_user_id, root),
    )


def _load_products(root: Path | None = None) -> dict[str, EconomyProduct]:
    path = _catalog_path(root)
    if not path.exists():
        raise EconomyError(f"economy catalog not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    raw_products = data.get("products", {})
    if not isinstance(raw_products, dict):
        raise EconomyError("economy catalog must contain a 'products' mapping")
    return {
        product_id: EconomyProduct.model_validate({"id": product_id, **raw})
        for product_id, raw in raw_products.items()
        if isinstance(raw, dict)
    }


def _load_state(root: Path | None = None) -> dict[str, Any]:
    path = _state_path(root)
    if not path.exists():
        return _empty_state()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise EconomyError(f"invalid economy state: {path}") from exc
    state = _empty_state()
    if isinstance(data, dict):
        if isinstance(data.get("wallet_ledger"), list):
            state["wallet_ledger"] = data["wallet_ledger"]
        if isinstance(data.get("entitlements"), list):
            state["entitlements"] = data["entitlements"]
        if isinstance(data.get("ghost_subscriptions"), dict):
            state["ghost_subscriptions"] = data["ghost_subscriptions"]
        if isinstance(data.get("fulfilled_purchases"), dict):
            state["fulfilled_purchases"] = data["fulfilled_purchases"]
    return state


def _save_state(state: dict[str, Any], root: Path | None = None) -> None:
    path = _state_path(root)
    atomic_write_text(path, json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def _append_wallet_entry(
    state: dict[str, Any],
    *,
    user_id: str,
    amount: int,
    reason: str,
    ref_id: str | None,
    metadata: dict[str, Any],
) -> WalletLedgerEntry:
    balance_after = _wallet_balance_from_state(state, user_id) + amount
    entry = WalletLedgerEntry(
        id=str(uuid4()),
        user_id=user_id,
        amount=amount,
        balance_after=balance_after,
        reason=reason,
        ref_id=ref_id,
        created_at=_now(),
        metadata=metadata,
    )
    state["wallet_ledger"].append(entry.model_dump(mode="json"))
    return entry


def _append_entitlement(
    state: dict[str, Any],
    *,
    user_id: str,
    entitlement_type: str,
    ref_id: str,
    source: str,
    duration_days: int | None,
    metadata: dict[str, Any],
) -> UserEntitlement:
    clean_type = _clean_required(entitlement_type, "entitlement_type")
    clean_ref = _clean_required(ref_id, "ref_id")
    now = datetime.now(UTC).replace(microsecond=0)
    entitlement = UserEntitlement(
        id=str(uuid4()),
        user_id=user_id,
        type=clean_type,
        ref_id=clean_ref,
        status="active",
        source=source or "manual",
        created_at=_format_dt(now),
        expires_at=_format_dt(now + timedelta(days=duration_days)) if duration_days else None,
        metadata=metadata,
    )
    state["entitlements"].append(entitlement.model_dump(mode="json"))
    return entitlement


def _set_ghost_subscription(
    state: dict[str, Any],
    *,
    user_id: str,
    character_id: str,
    agent_id: str,
    duration_days: int,
    source: str,
    metadata: dict[str, Any],
) -> GhostSubscription:
    now = datetime.now(UTC).replace(microsecond=0)
    existing = state["ghost_subscriptions"].get(user_id)
    start = now
    if isinstance(existing, dict):
        try:
            existing_sub = GhostSubscription.model_validate(existing)
            existing_end = datetime.fromisoformat(
                existing_sub.current_period_end.replace("Z", "+00:00")
            )
            if existing_end > now:
                start = existing_end
        except ValueError:
            start = now
    subscription = GhostSubscription(
        user_id=user_id,
        character_id=character_id,
        agent_id=agent_id,
        status="active",
        current_period_start=_format_dt(start),
        current_period_end=_format_dt(start + timedelta(days=duration_days)),
        source=source or "manual",
        updated_at=_format_dt(now),
        metadata=metadata,
    )
    state["ghost_subscriptions"][user_id] = subscription.model_dump(mode="json")
    return subscription


def _resolve_character_ref(
    user_id: str,
    character_id: str | None,
    root: Path | None = None,
) -> dict[str, str]:
    clean_character_id = str(character_id or "").strip()
    if clean_character_id:
        for card in CanonStore(root).load_character_cards():
            if card.id == clean_character_id or card.name.lower() == clean_character_id.lower():
                return {"character_id": card.id, "agent_id": agent_id_for_character(card)}
        raise EconomyError(f"character not found: {clean_character_id}")
    binding = get_user_binding(user_id, root)
    if binding is None or binding.status != "active":
        raise EconomyError("active user binding is required for a Ghost subscription")
    return {"character_id": binding.character_id, "agent_id": binding.agent_id}


def _wallet_balance_from_state(state: dict[str, Any], user_id: str) -> int:
    balance = 0
    for raw in state["wallet_ledger"]:
        if isinstance(raw, dict) and raw.get("user_id") == user_id:
            try:
                balance += int(raw.get("amount", 0))
            except (TypeError, ValueError):
                continue
    return balance


def _empty_state() -> dict[str, Any]:
    return {
        "schema": STATE_SCHEMA,
        "wallet_ledger": [],
        "entitlements": [],
        "ghost_subscriptions": {},
        "fulfilled_purchases": {},
    }


def _catalog_path(root: Path | None = None) -> Path:
    base = root or Path.cwd()
    return base / CATALOG_PATH


def _state_path(root: Path | None = None) -> Path:
    configured = get_settings().economy_state_path
    if configured.is_absolute():
        return configured
    base = root or Path.cwd()
    return base / configured


def _clean_required(value: str, field_name: str) -> str:
    clean = str(value or "").strip()
    if not clean:
        raise EconomyError(f"{field_name} is required")
    return clean


def _mapping_grant(value: object) -> dict[str, Any] | None:
    return value if isinstance(value, dict) else None


def _list_grants(value: object) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _optional_positive_int(value: object) -> int | None:
    parsed = _optional_int(value)
    if parsed is None:
        return None
    return parsed if parsed > 0 else None


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _now() -> str:
    return _format_dt(datetime.now(UTC).replace(microsecond=0))


def _format_dt(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
