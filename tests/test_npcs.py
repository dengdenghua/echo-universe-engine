from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from fastapi.testclient import TestClient

from echo_engine.api import app
from echo_engine.npcs import get_npc, list_npcs, route_npc_interaction


REPO_ROOT = Path(__file__).resolve().parents[1]


def seed_catalogs(root: Path) -> None:
    data = root / "data"
    data.mkdir(parents=True, exist_ok=True)
    for name in ["npcs.yaml", "realms.yaml"]:
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
faction: White Ghost Team
description: "Captain."
```
""",
        encoding="utf-8",
    )


def test_npc_catalog_loads_anchor_and_realm_npcs(tmp_path):
    seed_catalogs(tmp_path)
    seed_characters(tmp_path)

    rows = list_npcs(root=tmp_path)
    ids = {npc.id for npc in rows}

    assert {"zero", "atlas_identity_clerk", "ghost_court_bailiff"}.issubset(ids)
    zero = get_npc("zero", root=tmp_path)
    assert zero.agent_id == "echo_zero"
    assert zero.codename == "White Ghost"
    assert zero.bindable is True


def test_npc_filters_by_realm_type_and_bindable(tmp_path):
    seed_catalogs(tmp_path)
    seed_characters(tmp_path)

    atlas_npcs = list_npcs(realm_id="atlas", root=tmp_path)
    assert [npc.id for npc in atlas_npcs] == ["atlas_identity_clerk"]

    anchors = list_npcs(npc_type="anchor", bindable=True, root=tmp_path)
    assert {npc.id for npc in anchors}.issuperset({"zero", "kane", "eve", "raven"})


def test_route_npc_interaction_uses_realm_governance(tmp_path):
    seed_catalogs(tmp_path)
    seed_characters(tmp_path)

    route = route_npc_interaction(
        npc_id="ghost_court_bailiff",
        action="submit_realm_event",
        root=tmp_path,
    )

    assert route.realm_id == "ghost_court"
    assert route.reviewer_group == "ghost_court_reviewers"
    assert route.approval == "arc_reviewer_required"
    assert route.requires_entitlement == "realm_access:ghost_court"
    assert route.escalation_path == ["ghost_court", "atlas", "earth", "main"]


def test_route_npc_rejects_disallowed_action(tmp_path):
    seed_catalogs(tmp_path)
    seed_characters(tmp_path)

    try:
        route_npc_interaction(npc_id="atlas_identity_clerk", action="romance", root=tmp_path)
    except ValueError as exc:
        assert "not allowed" in str(exc)
    else:
        raise AssertionError("expected disallowed NPC action to fail")


def test_npcs_api_and_route(tmp_path, monkeypatch):
    seed_catalogs(tmp_path)
    seed_characters(tmp_path)
    monkeypatch.chdir(tmp_path)
    client = TestClient(app)

    listed = client.get("/api/npcs?realm_id=atlas")
    assert listed.status_code == 200
    assert listed.json()[0]["id"] == "atlas_identity_clerk"

    route = client.post("/api/npcs/atlas_identity_clerk/route", json={"action": "file_case"})
    assert route.status_code == 200
    assert route.json()["reviewer_group"] == "atlas_canon_board"


def test_cli_route_npc_outputs_json(tmp_path):
    seed_catalogs(tmp_path)
    seed_characters(tmp_path)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "echo_engine.cli",
            "route-npc",
            "--npc-id",
            "zero",
            "--action",
            "candidate_event",
        ],
        check=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert payload["npc_id"] == "zero"
    assert payload["reviewer_group"] == "core_world_brain"
    assert payload["approval"] == "world_brain_required"
