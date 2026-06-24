from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from fastapi.testclient import TestClient

from echo_engine.api import app
from echo_engine.economy import grant_entitlement
from echo_engine.skins import check_skin_access, list_skin_policies


REPO_ROOT = Path(__file__).resolve().parents[1]


def seed_catalogs(root: Path) -> None:
    data = root / "data"
    data.mkdir(parents=True, exist_ok=True)
    for name in ["skin_policy.yaml", "access_policy.yaml", "realms.yaml"]:
        shutil.copyfile(REPO_ROOT / "data" / name, data / name)


def test_local_skin_is_personal_only(tmp_path):
    seed_catalogs(tmp_path)

    decision = check_skin_access(
        user_id="free-user",
        skin_type="local_skin",
        requested_scope="city",
        realm_id="atlas",
        root=tmp_path,
    )

    assert decision.allowed is False
    assert decision.resolved_scope == "personal"
    assert decision.realm_id == "personal_instance"
    assert decision.required_downgrade == "realm_skin_or_uniform_skin"
    assert "private projections" in decision.reason


def test_edge_user_cannot_publish_realm_skin(tmp_path):
    seed_catalogs(tmp_path)

    decision = check_skin_access(
        user_id="free-user",
        skin_type="realm_skin",
        requested_scope="city",
        realm_id="atlas",
        root=tmp_path,
    )

    assert decision.allowed is False
    assert decision.identity_tier == "edge_ghost"
    assert "cannot publish realm_skin" in decision.reason


def test_realm_pass_user_can_publish_realm_skin_for_that_realm(tmp_path):
    seed_catalogs(tmp_path)
    grant_entitlement(
        user_id="paid-user",
        entitlement_type="realm_access",
        ref_id="atlas",
        source="test",
        root=tmp_path,
    )

    decision = check_skin_access(
        user_id="paid-user",
        skin_type="realm_skin",
        requested_scope="city",
        realm_id="atlas",
        claims=["courier"],
        root=tmp_path,
    )

    assert decision.allowed is True
    assert decision.identity_tier == "realm_participant"
    assert decision.requires_entitlement == "realm_access:atlas"
    assert decision.reviewer_group == "atlas_canon_board"


def test_banned_skin_claims_are_rejected(tmp_path):
    seed_catalogs(tmp_path)
    grant_entitlement(
        user_id="paid-user",
        entitlement_type="realm_access",
        ref_id="atlas",
        source="test",
        root=tmp_path,
    )

    decision = check_skin_access(
        user_id="paid-user",
        skin_type="realm_skin",
        requested_scope="city",
        realm_id="atlas",
        claims=["main_character"],
        root=tmp_path,
    )

    assert decision.allowed is False
    assert "main_character" in decision.reason
    assert decision.required_downgrade == "remove_claim_or_submit_visual_review"


def test_canon_skin_requires_canon_candidate(tmp_path):
    seed_catalogs(tmp_path)

    decision = check_skin_access(
        user_id="free-user",
        skin_type="canon_skin",
        requested_scope="main",
        realm_id="main",
        root=tmp_path,
    )

    assert decision.allowed is False
    assert decision.identity_tier == "edge_ghost"
    assert "cannot publish canon_skin" in decision.reason


def test_skin_policy_api_and_check(tmp_path, monkeypatch):
    seed_catalogs(tmp_path)
    monkeypatch.chdir(tmp_path)
    client = TestClient(app)

    policies = client.get("/api/skins/policies")
    assert policies.status_code == 200
    assert {item["id"] for item in policies.json()}.issuperset({"local_skin", "realm_skin"})

    checked = client.post(
        "/api/skins/check",
        json={
            "user_id": "free-user",
            "skin_type": "local_skin",
            "requested_scope": "city",
            "realm_id": "atlas",
        },
    )
    assert checked.status_code == 200
    assert checked.json()["allowed"] is False


def test_cli_check_skin_access_outputs_json(tmp_path):
    seed_catalogs(tmp_path)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "echo_engine.cli",
            "check-skin-access",
            "--user-id",
            "free-user",
            "--skin-type",
            "local_skin",
            "--requested-scope",
            "city",
            "--realm-id",
            "atlas",
        ],
        check=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert payload["allowed"] is False
    assert payload["required_downgrade"] == "realm_skin_or_uniform_skin"


def test_skin_policies_load_defaults(tmp_path):
    seed_catalogs(tmp_path)

    ids = {policy.id for policy in list_skin_policies(root=tmp_path)}

    assert {"local_skin", "uniform_skin", "realm_skin", "prestige_skin", "canon_skin"}.issubset(ids)
