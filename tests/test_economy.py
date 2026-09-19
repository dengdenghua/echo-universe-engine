from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from echo_engine.bindings import bind_user_to_character
from echo_engine.economy import (
    EconomyError,
    economy_account_summary,
    fulfill_external_purchase,
    list_products,
    purchase_product,
    record_wallet_entry,
    wallet_balance,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def seed_catalog(root: Path) -> None:
    data = root / "data"
    data.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REPO_ROOT / "data" / "economy_catalog.yaml", data / "economy_catalog.yaml")


def seed_characters(root: Path) -> None:
    characters = root / "characters"
    characters.mkdir(parents=True, exist_ok=True)
    (characters / "001_zero.md").write_text(
        """# Zero

```yaml
id: "001"
name: Zero
codename: White Ghost
description: "Captain."
```
""",
        encoding="utf-8",
    )


def test_economy_catalog_loads_defaults(tmp_path):
    seed_catalog(tmp_path)

    products = list_products(root=tmp_path)

    ids = {product.id for product in products}
    assert {"ghost_life_monthly", "realm_pass_atlas", "paid_review_priority"}.issubset(ids)
    assert next(product for product in products if product.id == "ghost_life_monthly").price_credits == 300


def test_wallet_grant_updates_balance_and_summary(tmp_path):
    entry = record_wallet_entry(
        user_id="mobile-user-1",
        amount=500,
        reason="test_topup",
        root=tmp_path,
    )

    assert entry.balance_after == 500
    assert wallet_balance("mobile-user-1", root=tmp_path) == 500
    summary = economy_account_summary("mobile-user-1", root=tmp_path)
    assert summary.wallet_balance == 500
    assert summary.entitlements == []


def test_purchase_realm_pass_debits_wallet_and_grants_entitlement(tmp_path):
    seed_catalog(tmp_path)
    record_wallet_entry(user_id="mobile-user-1", amount=500, reason="test_topup", root=tmp_path)

    result = purchase_product(
        user_id="mobile-user-1",
        product_id="realm_pass_atlas",
        root=tmp_path,
    )

    assert result["wallet_balance"] == 380
    assert result["ledger_entry"]["amount"] == -120
    entitlement = result["entitlements"][0]
    assert entitlement["type"] == "realm_access"
    assert entitlement["ref_id"] == "atlas"
    assert entitlement["expires_at"]


def test_purchase_ghost_monthly_activates_bound_subscription(tmp_path):
    seed_catalog(tmp_path)
    seed_characters(tmp_path)
    bind_user_to_character(user_id="mobile-user-1", character_id="001", root=tmp_path)
    record_wallet_entry(user_id="mobile-user-1", amount=500, reason="test_topup", root=tmp_path)

    result = purchase_product(
        user_id="mobile-user-1",
        product_id="ghost_life_monthly",
        root=tmp_path,
    )

    assert result["wallet_balance"] == 200
    assert result["ghost_subscription"]["character_id"] == "001"
    assert result["ghost_subscription"]["agent_id"] == "echo_zero"
    summary = economy_account_summary("mobile-user-1", root=tmp_path)
    assert summary.ghost_subscription is not None
    assert summary.ghost_subscription.status == "active"
    assert any(item.type == "ghost_life" for item in summary.entitlements)


def test_purchase_rejects_insufficient_funds(tmp_path):
    seed_catalog(tmp_path)

    try:
        purchase_product(user_id="mobile-user-1", product_id="realm_pass_atlas", root=tmp_path)
    except EconomyError as exc:
        assert "insufficient credits" in str(exc)
    else:
        raise AssertionError("expected insufficient funds to fail")


def test_external_fulfillment_is_idempotent_and_does_not_use_local_wallet(tmp_path):
    seed_catalog(tmp_path)

    first = fulfill_external_purchase(
        user_id="mobile-user-1",
        product_id="realm_pass_atlas",
        purchase_ref="echo:mobile-user-1:purchase-1",
        root=tmp_path,
    )
    second = fulfill_external_purchase(
        user_id="mobile-user-1",
        product_id="realm_pass_atlas",
        purchase_ref="echo:mobile-user-1:purchase-1",
        root=tmp_path,
    )

    assert first["duplicate"] is False
    assert second["duplicate"] is True
    assert wallet_balance("mobile-user-1", root=tmp_path) == 0
    assert len(economy_account_summary("mobile-user-1", root=tmp_path).entitlements) == 1


def test_economy_api_purchase_flow(tmp_path, api_client):
    seed_catalog(tmp_path)
    seed_characters(tmp_path)
    bind_user_to_character(user_id="mobile-user-1", character_id="001", root=tmp_path)

    grant = api_client.post(
        "/api/economy/wallet/grant",
        json={"user_id": "mobile-user-1", "amount": 500, "reason": "test_topup"},
    )
    assert grant.status_code == 200

    purchase = api_client.post(
        "/api/economy/purchases",
        json={"user_id": "mobile-user-1", "product_id": "ghost_life_monthly"},
    )
    assert purchase.status_code == 200
    assert purchase.json()["wallet_balance"] == 200

    summary = api_client.get("/api/economy/users/mobile-user-1/summary")
    assert summary.status_code == 200
    assert summary.json()["ghost_subscription"]["agent_id"] == "echo_zero"


def test_cli_wallet_grant_and_purchase(tmp_path):
    seed_catalog(tmp_path)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)

    grant = subprocess.run(
        [
            sys.executable,
            "-m",
            "echo_engine.cli",
            "wallet-grant",
            "--user-id",
            "mobile-user-1",
            "--amount",
            "200",
            "--reason",
            "test_topup",
        ],
        check=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
        text=True,
    )
    assert json.loads(grant.stdout)["balance_after"] == 200

    purchase = subprocess.run(
        [
            sys.executable,
            "-m",
            "echo_engine.cli",
            "purchase",
            "--user-id",
            "mobile-user-1",
            "--product-id",
            "paid_review_standard",
        ],
        check=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
        text=True,
    )
    body = json.loads(purchase.stdout)
    assert body["wallet_balance"] == 140
    assert body["entitlements"][0]["type"] == "review_slot"
