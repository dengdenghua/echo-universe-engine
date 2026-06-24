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
from echo_engine.identities import (
    assign_identity,
    check_npc_access,
    check_realm_event_access,
    get_universe_identity,
    list_identity_tiers,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def seed_catalogs(root: Path) -> None:
    data = root / "data"
    data.mkdir(parents=True, exist_ok=True)
    for name in ["access_policy.yaml", "realms.yaml", "npcs.yaml"]:
        shutil.copyfile(REPO_ROOT / "data" / name, data / name)


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


def test_default_registered_user_is_edge_ghost(tmp_path):
    seed_catalogs(tmp_path)

    identity = get_universe_identity("free-user", root=tmp_path)

    assert identity.tier == "edge_ghost"
    assert identity.edge_role == "edge_ghost"
    assert identity.allowed_realms == ["personal_instance"]
    assert list_identity_tiers(root=tmp_path)[0].id == "edge_ghost"


def test_edge_ghost_can_do_personal_anchor_chat_but_not_main_candidate(tmp_path):
    seed_catalogs(tmp_path)
    seed_characters(tmp_path)

    chat = check_npc_access(user_id="free-user", npc_id="zero", action="chat", root=tmp_path)
    assert chat.allowed is True
    assert chat.requested_scope == "personal"
    assert chat.realm_id == "personal_instance"

    candidate = check_npc_access(
        user_id="free-user",
        npc_id="zero",
        action="candidate_event",
        root=tmp_path,
    )
    assert candidate.allowed is False
    assert candidate.requested_scope == "main"
    assert "cannot perform action" in candidate.reason


def test_edge_ghost_cannot_submit_city_event_without_progression(tmp_path):
    seed_catalogs(tmp_path)

    decision = check_realm_event_access(
        user_id="free-user",
        scope="city",
        realm_id="atlas",
        root=tmp_path,
    )

    assert decision.allowed is False
    assert decision.identity_tier == "edge_ghost"
    assert "cannot submit city scope" in decision.reason


def test_realm_pass_promotes_access_to_realm_participant(tmp_path):
    seed_catalogs(tmp_path)
    seed_characters(tmp_path)
    grant_entitlement(
        user_id="paid-user",
        entitlement_type="realm_access",
        ref_id="atlas",
        source="test",
        root=tmp_path,
    )

    identity = get_universe_identity("paid-user", root=tmp_path)
    assert identity.tier == "realm_participant"
    assert "realm_access:atlas" in identity.active_entitlements

    npc = check_npc_access(
        user_id="paid-user",
        npc_id="atlas_identity_clerk",
        action="file_case",
        root=tmp_path,
    )
    assert npc.allowed is True
    assert npc.realm_id == "atlas"

    realm = check_realm_event_access(
        user_id="paid-user",
        scope="city",
        realm_id="atlas",
        root=tmp_path,
    )
    assert realm.allowed is True


def test_missing_required_npc_entitlement_is_reported(tmp_path):
    seed_catalogs(tmp_path)
    seed_characters(tmp_path)
    assign_identity(
        user_id="creator-user",
        tier="creator",
        realms=["ghost_court"],
        root=tmp_path,
    )

    decision = check_npc_access(
        user_id="creator-user",
        npc_id="ghost_court_bailiff",
        action="open_hearing",
        root=tmp_path,
    )

    assert decision.allowed is False
    assert decision.required_entitlement == "realm_access:ghost_court"
    assert "missing entitlement" in decision.reason


def test_identity_api_and_assignment(tmp_path, monkeypatch):
    seed_catalogs(tmp_path)
    seed_characters(tmp_path)
    monkeypatch.chdir(tmp_path)
    client = TestClient(app)

    before = client.get("/api/identity/users/free-user")
    assert before.status_code == 200
    assert before.json()["tier"] == "edge_ghost"

    assigned = client.post(
        "/api/identity/assignments",
        json={"user_id": "creator-user", "tier": "creator", "realms": ["ghost_court"]},
    )
    assert assigned.status_code == 200

    checked = client.post(
        "/api/identity/check-npc",
        json={"user_id": "creator-user", "npc_id": "zero", "action": "candidate_event"},
    )
    assert checked.status_code == 200
    assert checked.json()["allowed"] is False
    assert checked.json()["identity_tier"] == "creator"


def test_cli_check_realm_access_outputs_json(tmp_path):
    seed_catalogs(tmp_path)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "echo_engine.cli",
            "check-realm-access",
            "--user-id",
            "free-user",
            "--scope",
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
    assert payload["identity_tier"] == "edge_ghost"
