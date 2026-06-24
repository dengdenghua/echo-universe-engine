from __future__ import annotations

import json
import os
import subprocess
import sys

from fastapi.testclient import TestClient

from echo_engine.api import app
from echo_engine.journal import candidate_queue
from echo_engine.realm_events import realm_event_queue, submit_realm_event
from echo_engine.realms import get_realm, list_realms, route_realm_review


def test_default_realms_include_hierarchy():
    ids = {realm.id for realm in list_realms()}
    assert {"main", "earth", "atlas", "ghost_court", "personal_instance"}.issubset(ids)
    assert get_realm("atlas").parent_id == "earth"


def test_route_arc_review_to_realm_reviewers():
    route = route_realm_review(scope="arc", realm_id="ghost_court")
    assert route.resolved_realm_id == "ghost_court"
    assert route.reviewer_group == "ghost_court_reviewers"
    assert route.approval == "arc_reviewer_required"
    assert route.escalation_path == ["ghost_court", "atlas", "earth", "main"]


def test_route_main_review_to_core_world_brain():
    route = route_realm_review(scope="main")
    assert route.resolved_realm_id == "main"
    assert route.reviewer_group == "core_world_brain"
    assert route.approval == "world_brain_required"


def test_realms_api_review_route():
    client = TestClient(app)
    response = client.post(
        "/api/realms/review-route",
        json={"scope": "city", "realm_id": "atlas"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["resolved_realm_id"] == "atlas"
    assert body["reviewer_group"] == "atlas_canon_board"


def test_cli_route_review_outputs_json():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "echo_engine.cli",
            "route-review",
            "--scope",
            "personal",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    body = json.loads(result.stdout)
    assert body["resolved_realm_id"] == "personal_instance"
    assert body["approval"] == "auto_or_light_review"


def test_cli_submit_realm_event_outputs_routed_event(tmp_path):
    env = {**os.environ, "ECHO_JOURNAL_PATH": str(tmp_path / "cli_realm_events.jsonl")}
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "echo_engine.cli",
            "submit-realm-event",
            "--scope",
            "city",
            "--realm-id",
            "atlas",
            "--title",
            "Atlas side case",
            "--summary",
            "A user Ghost submits a city-level identity dispute.",
        ],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    body = json.loads(result.stdout)
    assert body["event_type"] == "realm_event"
    assert body["metadata"]["reviewer_group"] == "atlas_canon_board"


def test_submit_realm_event_routes_into_reviewer_queue(tmp_path, monkeypatch):
    monkeypatch.setenv("ECHO_JOURNAL_PATH", str(tmp_path / "realm_queue.jsonl"))
    from echo_engine.config import get_settings

    get_settings.cache_clear()
    event = submit_realm_event(
        title="Atlas lower-city Ghost hearing",
        summary="A user Ghost asks the city to recognize a copied memory as legal testimony.",
        scope="city",
        realm_id="atlas",
        submitter="mobile-user-1",
    )
    assert event.event_type == "realm_event"
    assert event.metadata["realm_id"] == "atlas"
    assert event.metadata["reviewer_group"] == "atlas_canon_board"
    assert event.metadata["approval"] == "city_reviewer_required"
    queue = realm_event_queue(reviewer_group="atlas_canon_board")
    assert [item.event_id for item in queue] == [event.event_id]
    candidates = candidate_queue()
    assert candidates[0]["event"]["event_type"] == "realm_event"
    assert candidates[0]["can_promote"] is False
    get_settings.cache_clear()


def test_realm_events_api_submit_and_filter(tmp_path, monkeypatch):
    monkeypatch.setenv("ECHO_JOURNAL_PATH", str(tmp_path / "realm_events.jsonl"))
    from echo_engine.config import get_settings

    get_settings.cache_clear()
    client = TestClient(app)
    response = client.post(
        "/api/realm-events",
        json={
            "title": "Ghost Court side case",
            "summary": "A side case needs arc review.",
            "scope": "arc",
            "realm_id": "ghost_court",
            "submitter": "showrunner-a",
        },
    )
    assert response.status_code == 200
    assert response.json()["metadata"]["reviewer_group"] == "ghost_court_reviewers"
    listed = client.get("/api/realm-events?reviewer_group=ghost_court_reviewers")
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    get_settings.cache_clear()
