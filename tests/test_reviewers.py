from __future__ import annotations

import json
import os
import subprocess
import sys

from fastapi.testclient import TestClient

from echo_engine.api import app
from echo_engine.config import get_settings
from echo_engine.journal import record_canon_decision
from echo_engine.realm_events import submit_realm_event
from echo_engine.reviewers import (
    authorize_reviewer_for_event,
    get_reviewer_group,
    list_reviewer_groups,
)


def test_reviewer_groups_load_defaults():
    ids = {group.id for group in list_reviewer_groups()}
    assert {"core_world_brain", "atlas_canon_board", "ghost_court_reviewers"}.issubset(ids)
    assert "atlas_editor" in get_reviewer_group("atlas_canon_board").members


def test_authorize_reviewer_for_realm_event(tmp_path, monkeypatch):
    monkeypatch.setenv("ECHO_JOURNAL_PATH", str(tmp_path / "auth.jsonl"))
    get_settings.cache_clear()
    event = submit_realm_event(
        title="Atlas hearing",
        summary="City-level identity dispute.",
        scope="city",
        realm_id="atlas",
    )
    denied = authorize_reviewer_for_event(reviewer="ghost_court_showrunner", event=event)
    assert denied.allowed is False
    allowed = authorize_reviewer_for_event(reviewer="atlas_editor", event=event)
    assert allowed.allowed is True
    assert allowed.matched_group == "atlas_canon_board"
    core = authorize_reviewer_for_event(reviewer="core_author", event=event)
    assert core.allowed is True
    assert core.matched_group == "core_world_brain"
    get_settings.cache_clear()


def test_record_canon_decision_enforces_realm_event_reviewer(tmp_path, monkeypatch):
    monkeypatch.setenv("ECHO_JOURNAL_PATH", str(tmp_path / "decision.jsonl"))
    get_settings.cache_clear()
    event = submit_realm_event(
        title="Atlas hearing",
        summary="City-level identity dispute.",
        scope="city",
        realm_id="atlas",
    )
    try:
        record_canon_decision(
            event_id=str(event.event_id),
            decision="accepted",
            reason="Looks safe.",
            reviewer="ghost_court_showrunner",
        )
    except ValueError as exc:
        assert "not authorized" in str(exc)
    else:
        raise AssertionError("expected unauthorized reviewer to fail")

    decision = record_canon_decision(
        event_id=str(event.event_id),
        decision="accepted",
        reason="City-local canon only.",
        reviewer="atlas_editor",
    )
    auth = decision.metadata["reviewer_authorization"]
    assert auth["allowed"] is True
    assert auth["required_group"] == "atlas_canon_board"
    get_settings.cache_clear()


def test_reviewers_api_authorize(tmp_path, monkeypatch):
    monkeypatch.setenv("ECHO_JOURNAL_PATH", str(tmp_path / "api_auth.jsonl"))
    get_settings.cache_clear()
    event = submit_realm_event(
        title="Ghost Court side case",
        summary="Arc-level case.",
        scope="arc",
        realm_id="ghost_court",
    )
    client = TestClient(app)
    response = client.post(
        "/api/reviewers/authorize",
        json={"reviewer": "ghost_court_showrunner", "event_id": str(event.event_id)},
    )
    assert response.status_code == 200
    assert response.json()["allowed"] is True
    get_settings.cache_clear()


def test_cli_review_candidate_rejects_unauthorized_reviewer(tmp_path):
    env = {**os.environ, "ECHO_JOURNAL_PATH": str(tmp_path / "cli_review.jsonl")}
    submit = subprocess.run(
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
            "City-level identity dispute.",
        ],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    event_id = json.loads(submit.stdout)["event_id"]
    denied = subprocess.run(
        [
            sys.executable,
            "-m",
            "echo_engine.cli",
            "review-candidate",
            "--event-id",
            event_id,
            "--decision",
            "accepted",
            "--reason",
            "Wrong board.",
            "--reviewer",
            "ghost_court_showrunner",
        ],
        capture_output=True,
        text=True,
        env=env,
    )
    assert denied.returncode != 0
    assert "not authorized" in denied.stderr

    allowed = subprocess.run(
        [
            sys.executable,
            "-m",
            "echo_engine.cli",
            "review-candidate",
            "--event-id",
            event_id,
            "--decision",
            "accepted",
            "--reason",
            "Atlas local canon only.",
            "--reviewer",
            "atlas_editor",
        ],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    assert json.loads(allowed.stdout)["metadata"]["reviewer"] == "atlas_editor"
