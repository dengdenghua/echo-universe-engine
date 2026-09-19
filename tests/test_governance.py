from __future__ import annotations

import sqlite3
from pathlib import Path

import yaml
from fastapi.testclient import TestClient

from echo_engine.api import app, get_root
from echo_engine.config import get_settings
from echo_engine.generators import run_story_agent
from echo_engine.governance import (
    GovernanceError,
    get_governance_state,
    promote_public_candidate,
    record_committee_vote,
    record_continuity_check,
    set_resonance,
)
from echo_engine.journal import JournalEvent, journal, record_canon_decision
from echo_engine.promotion import PromotionError, promote_candidate


def _governance_root(tmp_path: Path) -> Path:
    data = tmp_path / "data"
    source = tmp_path / "universe" / "novel" / "content" / "stranger-memory.zh.md"
    data.mkdir(parents=True)
    source.parent.mkdir(parents=True)
    source.write_text("白港不是被闹钟叫醒的。\n", encoding="utf-8")
    registry = {
        "schema": "echo_public_candidates_v1",
        "candidates": {
            "stranger-memory": {
                "version": "candidate-r1",
                "mode": "story",
                "title": {"zh": "陌生记忆", "en": "Stranger Memory"},
                "work": {"zh": "回响纪元", "en": "ECHO AGE"},
                "source_path": "universe/novel/content/stranger-memory.zh.md",
                "public_href": "/universe/novel/stranger-memory/",
                "target_path": "stories/stranger-memory.md",
                "reviewer_group": "canon_promotion_board",
                "required_approvals": 2,
                "continuity_reviewers": ["continuity_editor"],
                "resonance_enabled": True,
            }
        },
    }
    reviewers = {
        "schema": "echo_reviewers_v1",
        "groups": {
            "canon_promotion_board": {
                "id": "canon_promotion_board",
                "name": "Canon Promotion Board",
                "members": ["core_author", "world_brain", "continuity_editor"],
                "can_review_groups": ["canon_promotion_board"],
                "can_review_realms": ["main"],
                "can_review_scopes": ["main"],
            }
        },
    }
    (data / "public_candidates.yaml").write_text(
        yaml.safe_dump(registry, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    (data / "reviewers.yaml").write_text(
        yaml.safe_dump(reviewers, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return tmp_path


def _revision(root: Path) -> str:
    return get_governance_state("stranger-memory", root=root)["candidate"]["revision_sha256"]


def _committee_vote(
    root: Path,
    reviewer: str,
    *,
    decision: str = "approve",
    reason: str = "Approved.",
    actor_identity: str | None = None,
):
    return record_committee_vote(
        "stranger-memory",
        reviewer=reviewer,
        decision=decision,
        expected_revision_sha256=_revision(root),
        actor_identity=actor_identity or f"user:{reviewer}",
        auth_kind="reviewer_jwt",
        reason=reason,
        root=root,
    )


def _continuity_check(
    root: Path,
    *,
    verdict: str = "pass",
    reason: str = "Continuity cleared.",
    issues: list[str] | None = None,
):
    return record_continuity_check(
        "stranger-memory",
        reviewer="continuity_editor",
        verdict=verdict,
        expected_revision_sha256=_revision(root),
        actor_identity="user:continuity_editor",
        auth_kind="reviewer_jwt",
        reason=reason,
        issues=issues,
        root=root,
    )


def test_resonance_is_deduplicated_private_and_advisory(tmp_path):
    root = _governance_root(tmp_path)
    first = set_resonance(
        "stranger-memory",
        identity="device:visitor-1",
        identity_kind="anonymous",
        choice="support",
        secret="test-secret",
        root=root,
    )
    repeated = set_resonance(
        "stranger-memory",
        identity="device:visitor-1",
        identity_kind="anonymous",
        choice="support",
        secret="test-secret",
        root=root,
    )
    changed = set_resonance(
        "stranger-memory",
        identity="device:visitor-1",
        identity_kind="anonymous",
        choice="revise",
        secret="test-secret",
        root=root,
    )
    registered = set_resonance(
        "stranger-memory",
        identity="user:reader-42",
        identity_kind="registered",
        choice="support",
        secret="test-secret",
        root=root,
    )

    assert first["resonance"]["total"] == 1
    assert repeated["resonance"]["total"] == 1
    assert changed["resonance"]["support"] == 0
    assert changed["resonance"]["revise"] == 1
    assert registered["resonance"]["registered"]["support"] == 1
    assert registered["resonance"]["anonymous"]["revise"] == 1
    assert registered["promotion_gate"]["can_promote"] is False

    connection = sqlite3.connect(root / "data" / "echo.sqlite3")
    keys = [row[0] for row in connection.execute("SELECT voter_key FROM canon_resonance_votes")]
    events = [row[0] for row in connection.execute("SELECT actor_key FROM canon_governance_events")]
    connection.close()
    assert keys and all(value.startswith("rv1:") for value in keys)
    assert "visitor-1" not in " ".join(keys + events)
    assert "reader-42" not in " ".join(keys + events)


def test_current_revision_requires_continuity_and_two_committee_approvals(tmp_path):
    root = _governance_root(tmp_path)
    _committee_vote(
        root,
        "core_author",
        reason="Narrative structure holds.",
    )
    state = _committee_vote(
        root,
        "world_brain",
        reason="Canon boundaries hold.",
    )
    assert state["committee"]["approvals"] == 2
    assert state["promotion_gate"]["can_promote"] is False
    assert "continuity_pending" in state["promotion_gate"]["blockers"]

    cleared = _continuity_check(
        root,
        reason="Names, technology and consent boundaries are aligned.",
    )
    assert cleared["promotion_gate"]["can_promote"] is True

    source = root / "universe" / "novel" / "content" / "stranger-memory.zh.md"
    source.write_text(source.read_text(encoding="utf-8") + "正文发生修订。\n", encoding="utf-8")
    revised = get_governance_state("stranger-memory", root=root)
    assert revised["committee"]["approvals"] == 0
    assert revised["continuity"]["status"] == "pending"
    assert revised["committee"]["stale_reviews"] == 2
    assert revised["continuity"]["stale_checks"] == 1
    assert revised["promotion_gate"]["can_promote"] is False


def test_review_rejects_a_stale_revision_and_policy_changes_invalidate_votes(tmp_path):
    root = _governance_root(tmp_path)
    original_revision = _revision(root)
    _committee_vote(root, "core_author")

    registry_path = root / "data" / "public_candidates.yaml"
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    registry["candidates"]["stranger-memory"]["version"] = "candidate-r2"
    registry_path.write_text(
        yaml.safe_dump(registry, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    revised = get_governance_state("stranger-memory", root=root)
    assert revised["candidate"]["revision_sha256"] != original_revision
    assert revised["committee"]["approvals"] == 0
    assert revised["committee"]["stale_reviews"] == 1
    try:
        record_committee_vote(
            "stranger-memory",
            reviewer="world_brain",
            decision="approve",
            expected_revision_sha256=original_revision,
            actor_identity="user:world_brain",
            auth_kind="reviewer_jwt",
            reason="Approval from a stale screen.",
            root=root,
        )
    except GovernanceError as exc:
        assert "refresh before reviewing" in str(exc)
    else:
        raise AssertionError("expected stale revision to fail")


def test_one_authenticated_actor_cannot_take_two_committee_seats(tmp_path):
    root = _governance_root(tmp_path)
    _committee_vote(root, "core_author", actor_identity="admin:single-operator")
    try:
        _committee_vote(root, "world_brain", actor_identity="admin:single-operator")
    except GovernanceError as exc:
        assert "multiple committee seats" in str(exc)
    else:
        raise AssertionError("expected duplicate committee actor to fail")


def test_pre_authentication_review_rows_are_invalidated_and_do_not_count(tmp_path):
    root = _governance_root(tmp_path)
    revision = _revision(root)
    connection = sqlite3.connect(root / "data" / "echo.sqlite3")
    for reviewer in ("core_author", "world_brain"):
        connection.execute(
            """
            INSERT INTO canon_committee_reviews
                (candidate_id, revision_sha256, reviewer, decision, reason, created_at, updated_at)
            VALUES (?, ?, ?, 'approve', '', '2026-08-24T00:00:00Z', '2026-08-24T00:00:00Z')
            """,
            ("stranger-memory", revision, reviewer),
        )
    connection.execute(
        """
        INSERT INTO canon_continuity_checks
            (candidate_id, revision_sha256, reviewer, verdict, reason, issues_json,
             created_at, updated_at)
        VALUES (?, ?, 'continuity_editor', 'pass', '', '[]',
                '2026-08-24T00:00:00Z', '2026-08-24T00:00:00Z')
        """,
        ("stranger-memory", revision),
    )
    connection.commit()
    connection.close()

    state = get_governance_state("stranger-memory", root=root, include_private=True)
    assert state["committee"]["approvals"] == 0
    assert state["continuity"]["status"] == "pending"
    assert state["promotion_gate"]["can_promote"] is False

    connection = sqlite3.connect(root / "data" / "echo.sqlite3")
    auth_kinds = [
        row[0]
        for row in connection.execute(
            "SELECT auth_kind FROM canon_committee_reviews ORDER BY reviewer"
        )
    ]
    connection.close()
    assert auth_kinds == ["invalidated_legacy_identity", "invalidated_legacy_identity"]


def test_only_authorized_reviewers_can_vote_or_issue_hard_veto(tmp_path):
    root = _governance_root(tmp_path)
    try:
        record_committee_vote(
            "stranger-memory",
            reviewer="anonymous_editor",
            decision="approve",
            expected_revision_sha256=_revision(root),
            actor_identity="user:anonymous_editor",
            auth_kind="reviewer_jwt",
            reason="",
            root=root,
        )
    except GovernanceError as exc:
        assert "not a member" in str(exc)
    else:
        raise AssertionError("expected unauthorized committee reviewer to fail")

    blocked = _continuity_check(
        root,
        verdict="veto",
        reason="Consent boundary is incomplete.",
        issues=["consent_boundary"],
    )
    assert blocked["continuity"]["hard_veto"] is True
    assert blocked["promotion_gate"]["state"] == "blocked"
    assert "continuity_veto" in blocked["promotion_gate"]["blockers"]
    try:
        record_continuity_check(
            "stranger-memory",
            reviewer="continuity_editor",
            verdict="pass",
            expected_revision_sha256=_revision(root),
            actor_identity="user:continuity_editor",
            auth_kind="reviewer_jwt",
            reason="Attempted same-revision override.",
            root=root,
        )
    except GovernanceError as exc:
        assert "new content revision" in str(exc)
    else:
        raise AssertionError("expected same-revision veto override to fail")


def test_governed_promotion_writes_once_after_gate_is_ready(tmp_path):
    root = _governance_root(tmp_path)
    _continuity_check(root)
    for reviewer in ("core_author", "world_brain"):
        _committee_vote(root, reviewer)
    revision = _revision(root)
    result = promote_public_candidate(
        "stranger-memory",
        expected_revision_sha256=revision,
        root=root,
    )
    promoted = root / result["output_path"]
    assert promoted.is_file()
    assert "Promoted through ECHO canon governance" in promoted.read_text(encoding="utf-8")
    try:
        promote_public_candidate(
            "stranger-memory",
            expected_revision_sha256=revision,
            root=root,
        )
    except GovernanceError as exc:
        assert "already promoted" in str(exc)
    else:
        raise AssertionError("expected duplicate promotion to fail")

    original_promoted_bytes = promoted.read_bytes()
    promoted.write_text("tampered canon output\n", encoding="utf-8")
    tampered = get_governance_state("stranger-memory", root=root)
    assert tampered["promotion"]["promoted"] is False
    assert tampered["promotion"]["recorded"] is True
    assert tampered["promotion"]["integrity"] == "mismatch"
    assert "promotion_output_integrity" in tampered["promotion_gate"]["blockers"]
    promoted.write_bytes(original_promoted_bytes)

    source = root / "universe" / "novel" / "content" / "stranger-memory.zh.md"
    source.write_text(source.read_text(encoding="utf-8") + "晋升后修订。\n", encoding="utf-8")
    changed = get_governance_state("stranger-memory", root=root)
    assert changed["promotion"]["promoted"] is False
    assert changed["promotion"]["history_count"] == 1
    assert "promoted_revision_changed" in changed["promotion_gate"]["blockers"]


def test_legacy_promotion_cannot_write_a_governed_target_or_escape_root(tmp_path):
    root = _governance_root(tmp_path)
    run_story_agent(root)
    source = journal(root).read_all(event_type="candidate_output")[0]
    record_canon_decision(
        event_id=str(source.event_id),
        decision="accepted",
        reason="Legacy review accepted.",
        root=root,
    )

    try:
        promote_candidate(
            str(source.event_id),
            root=root,
            target_dir="stories",
            filename="stranger-memory.md",
            refresh_octopus_agents=False,
        )
    except PromotionError as exc:
        assert "protected by ECHO canon governance" in str(exc)
    else:
        raise AssertionError("expected governed target to reject the legacy workflow")

    try:
        promote_candidate(
            str(source.event_id),
            root=root,
            target_dir="../outside",
            filename="escape.md",
            refresh_octopus_agents=False,
        )
    except PromotionError as exc:
        assert "escapes its allowed root" in str(exc)
    else:
        raise AssertionError("expected promotion path traversal to fail")

    governed_source_event = JournalEvent(
        event_type="candidate_output",
        mode="story",
        title="Stranger Memory Copy",
        output_path="universe/novel/content/stranger-memory.zh.md",
    )
    journal(root).append(governed_source_event)
    record_canon_decision(
        event_id=str(governed_source_event.event_id),
        decision="accepted",
        reason="Attempted legacy acceptance of a governed source.",
        root=root,
    )
    try:
        promote_candidate(
            str(governed_source_event.event_id),
            root=root,
            target_dir="stories",
            filename="stranger-memory-copy.md",
            refresh_octopus_agents=False,
        )
    except PromotionError as exc:
        assert "protected by ECHO canon governance" in str(exc)
    else:
        raise AssertionError("expected governed source to reject the legacy workflow")


def test_production_fails_closed_without_admin_and_governance_secrets(
    tmp_path,
    monkeypatch,
):
    root = _governance_root(tmp_path)
    monkeypatch.chdir(root)
    for name in (
        "ECHO_ADMIN_API_KEY",
        "ECHO_ADMIN_API_KEY_FILE",
        "ECHO_USER_JWT_SECRET",
        "ECHO_USER_JWT_SECRET_FILE",
        "ECHO_GOVERNANCE_COOKIE_SECRET",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("ECHO_ENVIRONMENT", "production")
    get_settings.cache_clear()
    app.dependency_overrides[get_root] = lambda: root
    try:
        client = TestClient(app)
        public = client.get("/api/canon/candidates/stranger-memory/governance")
        assert public.status_code == 503
        internal = client.get("/api/canon/governance/candidates")
        assert internal.status_code == 503

        monkeypatch.setenv("ECHO_GOVERNANCE_COOKIE_SECRET", "production-cookie-secret")
        get_settings.cache_clear()
        public_with_signing = client.get("/api/canon/candidates/stranger-memory/governance")
        assert public_with_signing.status_code == 200
        internal_stays_closed = client.get("/api/canon/governance/candidates")
        assert internal_stays_closed.status_code == 503
    finally:
        app.dependency_overrides.pop(get_root, None)
        get_settings.cache_clear()


def test_public_governance_api_uses_signed_cookie_and_hides_private_review_data(tmp_path, monkeypatch):
    root = _governance_root(tmp_path)
    monkeypatch.setenv("ECHO_ADMIN_API_KEY", "admin-secret")
    monkeypatch.setenv("ECHO_GOVERNANCE_COOKIE_SECRET", "cookie-secret")
    get_settings.cache_clear()
    app.dependency_overrides[get_root] = lambda: root
    try:
        client = TestClient(app)
        public = client.get("/api/canon/candidates/stranger-memory/governance")
        assert public.status_code == 200
        assert "echo_resonance_id" in public.cookies
        assert "members" not in public.json()["committee"]
        assert "reviewers" not in public.json()["continuity"]

        voted = client.put(
            "/api/canon/candidates/stranger-memory/resonance",
            json={"choice": "support"},
        )
        repeated = client.put(
            "/api/canon/candidates/stranger-memory/resonance",
            json={"choice": "support"},
        )
        assert voted.status_code == 200
        assert repeated.json()["resonance"]["total"] == 1
        assert repeated.json()["resonance"]["viewer_choice"] == "support"

        protected = client.get("/api/canon/governance/candidates")
        assert protected.status_code == 401
        internal = client.get(
            "/api/canon/governance/candidates",
            headers={"Authorization": "Bearer admin-secret"},
        )
        assert internal.status_code == 200
        assert len(internal.json()[0]["committee"]["members"]) == 3
        revision = internal.json()[0]["candidate"]["revision_sha256"]
        first_admin_seat = client.post(
            "/api/canon/governance/candidates/stranger-memory/committee-votes",
            headers={"Authorization": "Bearer admin-secret"},
            json={
                "reviewer": "core_author",
                "decision": "approve",
                "expected_revision_sha256": revision,
            },
        )
        second_admin_seat = client.post(
            "/api/canon/governance/candidates/stranger-memory/committee-votes",
            headers={"Authorization": "Bearer admin-secret"},
            json={
                "reviewer": "world_brain",
                "decision": "approve",
                "expected_revision_sha256": revision,
            },
        )
        assert first_admin_seat.status_code == 200
        assert second_admin_seat.status_code == 403
        assert "multiple committee seats" in second_admin_seat.json()["detail"]
    finally:
        app.dependency_overrides.pop(get_root, None)
        get_settings.cache_clear()
