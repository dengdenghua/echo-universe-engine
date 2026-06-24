from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from echo_engine.economy import get_ghost_subscription, list_entitlements
from echo_engine.models import (
    AccessDecision,
    IdentityTierPolicy,
    UniverseIdentity,
    UserEntitlement,
    UserIdentityAssignment,
)
from echo_engine.npcs import NPCError, route_npc_interaction
from echo_engine.realms import RealmError, route_realm_review
from echo_engine.store import atomic_write_text


ACCESS_POLICY_PATH = Path("data/access_policy.yaml")
IDENTITIES_PATH = Path("data/user_identities.json")
PERSONAL_NPC_ACTIONS = {"bind", "chat", "diary", "personal_memory", "mission_prompt"}


class IdentityError(ValueError):
    pass


def list_identity_tiers(root: Path | None = None) -> list[IdentityTierPolicy]:
    return sorted(_load_tiers(root).values(), key=lambda item: item.rank)


def assign_identity(
    *,
    user_id: str,
    tier: str,
    realms: list[str] | None = None,
    source: str = "manual",
    metadata: dict[str, Any] | None = None,
    root: Path | None = None,
) -> UserIdentityAssignment:
    clean_user_id = _clean_required(user_id, "user_id")
    clean_tier = _clean_required(tier, "tier")
    tiers = _load_tiers(root)
    if clean_tier not in tiers:
        raise IdentityError(f"unknown identity tier: {clean_tier}")
    state = _load_identity_state(root)
    previous = state["assignments"].get(clean_user_id)
    now = _now()
    assignment = UserIdentityAssignment(
        user_id=clean_user_id,
        tier=clean_tier,
        status="active",
        source=source or "manual",
        created_at=previous.get("created_at", now) if isinstance(previous, dict) else now,
        updated_at=now,
        realms=sorted({item.strip() for item in realms or [] if item.strip()}),
        metadata=metadata or {},
    )
    state["assignments"][clean_user_id] = assignment.model_dump(mode="json")
    _save_identity_state(state, root)
    return assignment


def get_identity_assignment(user_id: str, root: Path | None = None) -> UserIdentityAssignment | None:
    clean_user_id = _clean_required(user_id, "user_id")
    raw = _load_identity_state(root)["assignments"].get(clean_user_id)
    if not isinstance(raw, dict):
        return None
    assignment = UserIdentityAssignment.model_validate(raw)
    return assignment if assignment.status == "active" else None


def get_universe_identity(user_id: str, root: Path | None = None) -> UniverseIdentity:
    clean_user_id = _clean_required(user_id, "user_id")
    tiers = _load_tiers(root)
    assignment = get_identity_assignment(clean_user_id, root)
    entitlements = _active_entitlements(clean_user_id, root)
    subscription = get_ghost_subscription(clean_user_id, root)
    subscription_active = bool(subscription and subscription.status == "active")
    tier_id = assignment.tier if assignment else _default_tier(root)
    if subscription_active and tier_id == "edge_ghost" and "citizen" in tiers:
        tier_id = "citizen"
    if _has_entitlement(entitlements, "realm_access", None) and tiers[tier_id].rank < tiers["realm_participant"].rank:
        tier_id = "realm_participant"
    if _has_entitlement(entitlements, "realm_operator_tools", None) and "realm_operator" in tiers:
        tier_id = "realm_operator"
    policy = tiers[tier_id]
    allowed_realms = set(policy.allowed_realms)
    if assignment:
        allowed_realms.update(assignment.realms)
    for entitlement in entitlements:
        if entitlement.type == "realm_access":
            allowed_realms.add(entitlement.ref_id)
    return UniverseIdentity(
        user_id=clean_user_id,
        tier=policy.id,
        tier_name=policy.name,
        rank=policy.rank,
        status="active",
        source=assignment.source if assignment else "default",
        edge_role="edge_ghost" if policy.id == "edge_ghost" else policy.id,
        allowed_realms=sorted(allowed_realms),
        active_entitlements=[_entitlement_key(item) for item in entitlements],
        ghost_subscription_active=subscription_active,
        can_create_npc_types=policy.can_create_npc_types,
        can_manage_realms=policy.can_manage_realms,
    )


def check_realm_event_access(
    *,
    user_id: str,
    scope: str,
    realm_id: str | None = None,
    root: Path | None = None,
) -> AccessDecision:
    identity = get_universe_identity(user_id, root)
    policy = _load_tiers(root)[identity.tier]
    try:
        route = route_realm_review(scope=scope, realm_id=realm_id, root=root)
    except RealmError as exc:
        raise IdentityError(str(exc)) from exc
    if not _scope_allowed(policy.max_review_scope, route.requested_scope, root):
        return _decision(
            identity=identity,
            allowed=False,
            reason=f"identity tier '{identity.tier}' cannot submit {route.requested_scope} scope",
            action="submit_realm_event",
            scope=route.requested_scope,
            realm_id=route.resolved_realm_id,
            reviewer_group=route.reviewer_group,
            approval=route.approval,
            escalation_path=route.escalation_path,
        )
    if not _realm_allowed(identity, route.resolved_realm_id):
        required = f"realm_access:{route.resolved_realm_id}"
        return _decision(
            identity=identity,
            allowed=False,
            reason=f"missing realm access: {required}",
            action="submit_realm_event",
            scope=route.requested_scope,
            realm_id=route.resolved_realm_id,
            required_entitlement=required,
            reviewer_group=route.reviewer_group,
            approval=route.approval,
            escalation_path=route.escalation_path,
        )
    return _decision(
        identity=identity,
        allowed=True,
        reason="allowed by identity tier and Realm access",
        action="submit_realm_event",
        scope=route.requested_scope,
        realm_id=route.resolved_realm_id,
        reviewer_group=route.reviewer_group,
        approval=route.approval,
        escalation_path=route.escalation_path,
    )


def check_npc_access(
    *,
    user_id: str,
    npc_id: str,
    action: str,
    root: Path | None = None,
) -> AccessDecision:
    identity = get_universe_identity(user_id, root)
    policy = _load_tiers(root)[identity.tier]
    try:
        route = route_npc_interaction(npc_id=npc_id, action=action, root=root)
    except NPCError as exc:
        raise IdentityError(str(exc)) from exc
    effective_scope = "personal" if route.npc_type == "anchor" and route.action in PERSONAL_NPC_ACTIONS else route.review_scope
    effective_realm = (
        "personal_instance"
        if route.npc_type == "anchor" and route.action in PERSONAL_NPC_ACTIONS
        else route.realm_id
    )
    if not _allows(policy.allowed_actions, route.action):
        return _decision(
            identity=identity,
            allowed=False,
            reason=f"identity tier '{identity.tier}' cannot perform action '{route.action}'",
            action=route.action,
            scope=effective_scope,
            realm_id=effective_realm,
            npc_id=route.npc_id,
            required_entitlement=route.requires_entitlement,
            reviewer_group=route.reviewer_group,
            approval=route.approval,
            escalation_path=route.escalation_path,
        )
    if not _allows(policy.allowed_npc_types, route.npc_type):
        return _decision(
            identity=identity,
            allowed=False,
            reason=f"identity tier '{identity.tier}' cannot interact with {route.npc_type} NPCs",
            action=route.action,
            scope=effective_scope,
            realm_id=effective_realm,
            npc_id=route.npc_id,
            required_entitlement=route.requires_entitlement,
            reviewer_group=route.reviewer_group,
            approval=route.approval,
            escalation_path=route.escalation_path,
        )
    if route.requires_entitlement and route.requires_entitlement not in identity.active_entitlements:
        return _decision(
            identity=identity,
            allowed=False,
            reason=f"missing entitlement: {route.requires_entitlement}",
            action=route.action,
            scope=effective_scope,
            realm_id=effective_realm,
            npc_id=route.npc_id,
            required_entitlement=route.requires_entitlement,
            reviewer_group=route.reviewer_group,
            approval=route.approval,
            escalation_path=route.escalation_path,
        )
    if not _scope_allowed(policy.max_review_scope, effective_scope, root):
        return _decision(
            identity=identity,
            allowed=False,
            reason=f"identity tier '{identity.tier}' cannot affect {effective_scope} scope",
            action=route.action,
            scope=effective_scope,
            realm_id=effective_realm,
            npc_id=route.npc_id,
            required_entitlement=route.requires_entitlement,
            reviewer_group=route.reviewer_group,
            approval=route.approval,
            escalation_path=route.escalation_path,
        )
    if not _realm_allowed(identity, effective_realm):
        required = route.requires_entitlement or f"realm_access:{effective_realm}"
        return _decision(
            identity=identity,
            allowed=False,
            reason=f"missing realm access: {required}",
            action=route.action,
            scope=effective_scope,
            realm_id=effective_realm,
            npc_id=route.npc_id,
            required_entitlement=required,
            reviewer_group=route.reviewer_group,
            approval=route.approval,
            escalation_path=route.escalation_path,
        )
    return _decision(
        identity=identity,
        allowed=True,
        reason="allowed by identity tier, entitlement, and Realm policy",
        action=route.action,
        scope=effective_scope,
        realm_id=effective_realm,
        npc_id=route.npc_id,
        required_entitlement=route.requires_entitlement,
        reviewer_group=route.reviewer_group,
        approval=route.approval,
        escalation_path=route.escalation_path,
    )


def _load_tiers(root: Path | None = None) -> dict[str, IdentityTierPolicy]:
    data = _load_policy_data(root)
    raw_tiers = data.get("tiers", {})
    if not isinstance(raw_tiers, dict):
        raise IdentityError("access policy must contain a 'tiers' mapping")
    return {
        tier_id: IdentityTierPolicy.model_validate({"id": tier_id, **raw})
        for tier_id, raw in raw_tiers.items()
        if isinstance(raw, dict)
    }


def _default_tier(root: Path | None = None) -> str:
    data = _load_policy_data(root)
    default = str(data.get("default_tier") or "").strip()
    tiers = _load_tiers(root)
    if default in tiers:
        return default
    for tier in tiers.values():
        if tier.default:
            return tier.id
    raise IdentityError("access policy has no default tier")


def _scope_allowed(max_scope: str, requested_scope: str, root: Path | None = None) -> bool:
    ranks = _scope_ranks(root)
    return ranks.get(requested_scope, 999) <= ranks.get(max_scope, -1)


def _scope_ranks(root: Path | None = None) -> dict[str, int]:
    data = _load_policy_data(root)
    raw = data.get("scope_rank", {})
    if not isinstance(raw, dict):
        raise IdentityError("access policy must contain a 'scope_rank' mapping")
    return {str(key): int(value) for key, value in raw.items()}


def _load_policy_data(root: Path | None = None) -> dict[str, Any]:
    path = _policy_path(root)
    if not path.exists():
        raise IdentityError(f"access policy not found: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _load_identity_state(root: Path | None = None) -> dict[str, Any]:
    path = _identity_state_path(root)
    if not path.exists():
        return {"schema": "echo_user_identities_v1", "assignments": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise IdentityError(f"invalid user identity state: {path}") from exc
    assignments = data.get("assignments", {}) if isinstance(data, dict) else {}
    return {
        "schema": "echo_user_identities_v1",
        "assignments": assignments if isinstance(assignments, dict) else {},
    }


def _save_identity_state(state: dict[str, Any], root: Path | None = None) -> None:
    path = _identity_state_path(root)
    atomic_write_text(path, json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def _active_entitlements(user_id: str, root: Path | None = None) -> list[UserEntitlement]:
    now = datetime.now(UTC)
    active: list[UserEntitlement] = []
    for entitlement in list_entitlements(user_id, root):
        if entitlement.status != "active":
            continue
        if entitlement.expires_at:
            try:
                expires_at = datetime.fromisoformat(entitlement.expires_at.replace("Z", "+00:00"))
            except ValueError:
                continue
            if expires_at <= now:
                continue
        active.append(entitlement)
    return active


def _has_entitlement(
    entitlements: list[UserEntitlement],
    entitlement_type: str,
    ref_id: str | None,
) -> bool:
    return any(
        item.type == entitlement_type and (ref_id is None or item.ref_id == ref_id)
        for item in entitlements
    )


def _entitlement_key(entitlement: UserEntitlement) -> str:
    return f"{entitlement.type}:{entitlement.ref_id}"


def _realm_allowed(identity: UniverseIdentity, realm_id: str) -> bool:
    return "*" in identity.allowed_realms or realm_id in identity.allowed_realms


def _allows(values: list[str], value: str) -> bool:
    return "*" in values or value in values


def _decision(
    *,
    identity: UniverseIdentity,
    allowed: bool,
    reason: str,
    action: str,
    scope: str | None,
    realm_id: str | None,
    npc_id: str | None = None,
    required_entitlement: str | None = None,
    reviewer_group: str | None = None,
    approval: str | None = None,
    escalation_path: list[str] | None = None,
) -> AccessDecision:
    return AccessDecision(
        user_id=identity.user_id,
        allowed=allowed,
        reason=reason,
        identity_tier=identity.tier,
        requested_action=action,
        requested_scope=scope,
        realm_id=realm_id,
        npc_id=npc_id,
        required_entitlement=required_entitlement,
        reviewer_group=reviewer_group,
        approval=approval,
        escalation_path=escalation_path or [],
    )


def _policy_path(root: Path | None = None) -> Path:
    base = root or Path.cwd()
    return base / ACCESS_POLICY_PATH


def _identity_state_path(root: Path | None = None) -> Path:
    base = root or Path.cwd()
    return base / IDENTITIES_PATH


def _clean_required(value: str, field_name: str) -> str:
    clean = str(value or "").strip()
    if not clean:
        raise IdentityError(f"{field_name} is required")
    return clean


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
