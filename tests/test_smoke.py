from echo_engine.generators import run_consistency_agent
from echo_engine.neural.octopus_ecosystem import (
    ecosystem_paths,
    render_octopus_ecosystem_plan,
)
from echo_engine.scheduler import auto_commit, due_task_keys
from echo_engine.store import CanonStore
from datetime import datetime
from fastapi.testclient import TestClient
import json
import os
import subprocess
import sys

from echo_engine.api import app
from echo_engine.config import get_settings
from echo_engine.generators import run_story_agent
from echo_engine.journal import JSONLJournal, JournalEvent, candidate_queue, journal, record_canon_decision
from echo_engine.generators import run_character_agent, run_relationship_agent
from echo_engine.neural.octopus_export import configured_octopus_agents_root, export_octopus_agents
from echo_engine.promotion import PromotionError, promote_candidate
import yaml


def test_canon_status_counts_initial_files():
    status = CanonStore().status()
    assert status.bible_files >= 5
    assert status.characters >= 8


def test_consistency_agent_writes_output(tmp_path):
    result = run_consistency_agent(tmp_path)
    assert result.mode == "consistency"
    assert result.output_path


def test_generation_records_candidate_journal_event(tmp_path):
    result = run_story_agent(tmp_path)
    events = journal(tmp_path).read_all()
    assert len(events) == 1
    assert events[0].event_type == "candidate_output"
    assert events[0].mode == "story"
    assert events[0].title == result.title
    assert events[0].output_path == result.output_path
    assert events[0].canon_status == "candidate"


def test_jsonl_journal_roundtrip(tmp_path):
    path = tmp_path / "events.jsonl"
    j = JSONLJournal(path)
    event = JournalEvent(event_type="candidate_output", mode="story", title="Demo")
    j.append(event)
    reloaded = JSONLJournal(path).read_all()
    assert len(reloaded) == 1
    assert reloaded[0].event_id == event.event_id


def test_record_canon_decision_appends_review_event(tmp_path):
    result = run_story_agent(tmp_path)
    source = journal(tmp_path).read_all()[0]
    decision = record_canon_decision(
        event_id=str(source.event_id),
        decision="rejected",
        reason="Needs stronger legal identity constraints.",
        root=tmp_path,
    )
    events = journal(tmp_path).read_all()
    assert result.output_path
    assert len(events) == 2
    assert decision.event_type == "canon_decision"
    assert decision.metadata["source_event_id"] == str(source.event_id)
    assert decision.canon_status == "rejected"


def test_candidate_queue_merges_review_and_promotion_state(tmp_path):
    run_story_agent(tmp_path)
    source = journal(tmp_path).read_all()[0]
    record_canon_decision(
        event_id=str(source.event_id),
        decision="accepted",
        reason="Canon-safe story seed.",
        root=tmp_path,
    )
    promoted = promote_candidate(str(source.event_id), root=tmp_path, refresh_octopus_agents=False)
    rows = candidate_queue(tmp_path)
    assert len(rows) == 1
    assert rows[0]["status"] == "promoted"
    assert rows[0]["can_promote"] is False
    assert rows[0]["latest_decision"]["canon_status"] == "accepted"
    assert rows[0]["promotion"]["output_path"] == promoted.promoted_path


def test_consistency_agent_reports_reviewed_candidate_status(tmp_path):
    run_story_agent(tmp_path)
    source = journal(tmp_path).read_all()[0]
    record_canon_decision(
        event_id=str(source.event_id),
        decision="rejected",
        reason="Needs stronger legal identity constraints.",
        root=tmp_path,
    )
    audit = run_consistency_agent(tmp_path)
    assert "status: rejected" in audit.content
    assert "Needs stronger legal identity constraints." in audit.content


def test_promote_candidate_requires_acceptance(tmp_path):
    run_story_agent(tmp_path)
    source = journal(tmp_path).read_all()[0]
    try:
        promote_candidate(str(source.event_id), root=tmp_path, refresh_octopus_agents=False)
    except PromotionError as exc:
        assert "accepted" in str(exc)
    else:
        raise AssertionError("expected PromotionError")


def test_promote_candidate_writes_canon_file_and_journal_event(tmp_path):
    run_story_agent(tmp_path)
    source = journal(tmp_path).read_all()[0]
    record_canon_decision(
        event_id=str(source.event_id),
        decision="accepted",
        reason="Canon-safe story seed.",
        root=tmp_path,
    )
    result = promote_candidate(str(source.event_id), root=tmp_path, refresh_octopus_agents=False)
    promoted = tmp_path / result.promoted_path
    assert promoted.exists()
    assert result.promoted_path.startswith("stories/promoted_")
    assert "source_event_id" in promoted.read_text(encoding="utf-8")
    assert journal(tmp_path).read_all()[-1].event_type == "promotion"


def test_promote_candidate_rejects_duplicate_promotion_from_journal(tmp_path):
    run_story_agent(tmp_path)
    source = journal(tmp_path).read_all()[0]
    record_canon_decision(
        event_id=str(source.event_id),
        decision="accepted",
        reason="Canon-safe story seed.",
        root=tmp_path,
    )
    promote_candidate(str(source.event_id), root=tmp_path, refresh_octopus_agents=False)
    try:
        promote_candidate(
            str(source.event_id),
            root=tmp_path,
            filename="different-target.md",
            refresh_octopus_agents=False,
        )
    except PromotionError as exc:
        assert "already promoted" in str(exc)
    else:
        raise AssertionError("expected PromotionError")


def test_promote_character_candidate_writes_character_card(tmp_path):
    run_character_agent(tmp_path)
    source = journal(tmp_path).read_all()[0]
    record_canon_decision(
        event_id=str(source.event_id),
        decision="accepted",
        reason="Approved character seed.",
        root=tmp_path,
    )
    result = promote_candidate(str(source.event_id), root=tmp_path, refresh_octopus_agents=False)
    assert result.promoted_path == "characters/001_mira_voss.md"
    cards = CanonStore(tmp_path).load_character_cards()
    assert cards[0].name == "Mira Voss"
    assert cards[0].abilities == ["Memory Suturing"]


def test_promote_relationship_candidate_writes_yaml(tmp_path):
    run_relationship_agent(tmp_path)
    source = journal(tmp_path).read_all()[0]
    record_canon_decision(
        event_id=str(source.event_id),
        decision="accepted",
        reason="Approved relationship delta.",
        root=tmp_path,
    )
    result = promote_candidate(str(source.event_id), root=tmp_path, refresh_octopus_agents=False)
    promoted = tmp_path / result.promoted_path
    data = yaml.safe_load("\n".join(line for line in promoted.read_text(encoding="utf-8").splitlines() if not line.startswith("#")))
    assert result.promoted_path.endswith(".yaml")
    assert data["Zero"]["Mother"] == "origin threat / possible creator"


def test_character_promotion_refreshes_octopus_agent_pack(tmp_path):
    run_character_agent(tmp_path)
    source = journal(tmp_path).read_all()[0]
    record_canon_decision(
        event_id=str(source.event_id),
        decision="accepted",
        reason="Approved character seed.",
        root=tmp_path,
    )
    promote_candidate(str(source.event_id), root=tmp_path)
    agent_dir = tmp_path / "outputs" / "octopus_agents" / "echo_mira_voss"
    assert (agent_dir / "profile.jsonc").exists()
    assert (agent_dir / "avatar.svg").exists()
    assert (agent_dir / "agent-core" / "SOUL.md").read_text(encoding="utf-8").startswith(
        "# Mira Voss"
    )


def test_octopus_ecosystem_plan_loads():
    plan = render_octopus_ecosystem_plan()
    paths = ecosystem_paths()
    assert "Octopus Ecosystem Integration Plan" in plan
    assert "Architecture codex: workflows/architecture_codex.md" in plan
    assert "AI-native interactive universe" in plan
    assert "bind Ghost" in plan
    assert "character_agents" in plan
    assert "octopus_agent" in paths


def test_scheduler_due_task_keys():
    due = due_task_keys(datetime(2147, 1, 1, 9, 30))
    assert [name for name, _ in due] == ["2147-01-01:daily digital life"]


def test_auto_commit_disabled_does_nothing():
    auto_commit("test")


def test_api_serves_console_and_characters():
    client = TestClient(app)
    assert client.get("/").status_code == 200
    response = client.get("/api/canon/characters")
    assert response.status_code == 200
    assert len(response.json()) >= 8


def test_api_serves_journal_events():
    client = TestClient(app)
    response = client.get("/api/journal/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_api_serves_candidate_queue():
    client = TestClient(app)
    response = client.get("/api/journal/candidates")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_api_reports_octopus_runtime_status(tmp_path, monkeypatch):
    monkeypatch.setenv("ECHO_OCTOPUS_AGENTS_ROOT", str(tmp_path / "agents"))
    monkeypatch.setenv("ECHO_OCTOPUS_RUNTIME_URL", "http://127.0.0.1:18000")
    get_settings.cache_clear()
    client = TestClient(app)
    response = client.get("/api/integrations/octopus/status")
    assert response.status_code == 200
    assert response.json()["agents_root"] == str(tmp_path / "agents")
    assert response.json()["configured"] is True
    assert response.json()["runtime_url"] == "http://127.0.0.1:18000"
    assert response.json()["runtime_configured"] is True
    get_settings.cache_clear()


def test_api_syncs_octopus_runtime_agents_to_configured_root(tmp_path, monkeypatch):
    target = tmp_path / "runtime_agents"
    monkeypatch.setenv("ECHO_OCTOPUS_AGENTS_ROOT", str(target))
    get_settings.cache_clear()
    client = TestClient(app)
    response = client.post("/api/integrations/octopus/sync-agents", json={})
    assert response.status_code == 200
    assert response.json()["ok"] is True
    assert response.json()["reload"] is None
    assert (target / "echo_zero" / "profile.jsonc").exists()
    get_settings.cache_clear()


def test_configured_octopus_agents_root_supports_relative_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("ECHO_OCTOPUS_AGENTS_ROOT", "octopus-agents")
    get_settings.cache_clear()
    assert configured_octopus_agents_root() == tmp_path / "octopus-agents"
    get_settings.cache_clear()


def test_configured_octopus_agents_root_discovers_sibling_runtime(tmp_path, monkeypatch):
    echo_root = tmp_path / "octopus" / "echo-universe-engine"
    agents_root = tmp_path / "octopus" / "octopus-agent" / "agents"
    echo_root.mkdir(parents=True)
    agents_root.mkdir(parents=True)
    monkeypatch.delenv("ECHO_OCTOPUS_AGENTS_ROOT", raising=False)
    get_settings.cache_clear()
    assert configured_octopus_agents_root(echo_root) == agents_root
    get_settings.cache_clear()


def test_api_records_journal_decision(tmp_path, monkeypatch):
    monkeypatch.setenv("ECHO_JOURNAL_PATH", str(tmp_path / "api_journal.jsonl"))
    get_settings.cache_clear()
    client = TestClient(app)
    response = client.post(
        "/api/journal/decisions",
        json={
            "event_id": "missing",
            "decision": "rejected",
            "reason": "No source event in test.",
        },
    )
    assert response.status_code == 200
    assert response.json()["event_type"] == "canon_decision"
    assert response.json()["metadata"]["source_found"] is False
    get_settings.cache_clear()


def test_api_promotion_rejects_unaccepted_candidate(tmp_path, monkeypatch):
    monkeypatch.setenv("ECHO_JOURNAL_PATH", str(tmp_path / "api_promotion_journal.jsonl"))
    get_settings.cache_clear()
    client = TestClient(app)
    response = client.post("/api/canon/promotions", json={"event_id": "missing"})
    assert response.status_code == 400
    assert "candidate event not found" in response.json()["detail"]
    get_settings.cache_clear()


def test_white_ghost_visual_assets_are_copied():
    root = CanonStore().root / "assets" / "characters"
    for folder in [
        "001_zero",
        "002_kane",
        "003_eve",
        "004_leon",
        "005_raven",
        "006_shion",
        "007_noah",
        "008_luna",
    ]:
        refs = root / folder / "octopus_refs"
        for filename in ["avatar.png", "front.png", "side.png", "back.png", "source_profile.jsonc"]:
            assert (refs / filename).exists()


def test_api_serves_character_visual_assets():
    client = TestClient(app)
    response = client.get("/api/assets/characters")
    assert response.status_code == 200
    data = response.json()
    assert len(data["characters"]) >= 8
    assert {"001", "008"}.issubset(data["characters"])
    zero = data["characters"]["001"]
    assert zero["name"] == "Zero"
    assert zero["urls"]["front"].endswith("/assets/characters/001_zero/octopus_refs/front.png")


def test_console_keeps_octopus_runtime_hidden_by_default():
    html = (CanonStore().root / "console" / "index.html").read_text(encoding="utf-8")
    js = (CanonStore().root / "console" / "app.js").read_text(encoding="utf-8")
    assert 'data-window="octopus"' in html
    assert "runtime-only" in html
    assert 'get("runtime") === "1"' in js


def test_console_exposes_candidate_review_controls():
    html = (CanonStore().root / "console" / "index.html").read_text(encoding="utf-8")
    js = (CanonStore().root / "console" / "app.js").read_text(encoding="utf-8")
    assert 'id="candidate-grid"' in html
    assert "/api/journal/candidates?limit=24" in js
    assert "/api/canon/promotions" in js


def test_console_exposes_hidden_octopus_sync_controls():
    html = (CanonStore().root / "console" / "index.html").read_text(encoding="utf-8")
    js = (CanonStore().root / "console" / "app.js").read_text(encoding="utf-8")
    assert 'id="octopus-sync-btn"' in html
    assert "/api/integrations/octopus/status" in js
    assert "/api/integrations/octopus/sync-agents" in js


def test_octopus_export_matches_agent_loader_layout(tmp_path):
    written = export_octopus_agents(output_dir=tmp_path)
    assert tmp_path / "_shared" / "IDENTITY_BANNER.md" in written

    zero = tmp_path / "echo_zero"
    core = zero / "agent-core"
    for path in [
        zero / "profile.jsonc",
        zero / "avatar.png",
        zero / "visuals" / "front.png",
        core / "SOUL.md",
        core / "IDENTITY.md",
        core / "MEMORY.md",
        core / "AGENTS.md",
        core / "BOOTSTRAP.md",
        core / "USER.md",
        core / "tool-registry.jsonc",
        core / ".soul_history",
        core / "diary",
        core / "skills",
        zero / "memory",
        zero / "permissions",
        zero / "project",
        zero / "runtime",
        zero / "sessions",
        zero / "skills",
    ]:
        assert path.exists()

    profile_text = (zero / "profile.jsonc").read_text(encoding="utf-8")
    profile = json.loads("\n".join(line for line in profile_text.splitlines() if not line.startswith("//")))
    assert profile["model"] == {"provider": "auto", "name": "auto"}
    assert profile["avatar"] == "avatar.png"
    assert profile["character_profile"]["zh_name"] == "零"
    assert profile["character_profile"]["visual_assets"]["front_image"] == "visuals/front.png"
    assert profile["systemPrompt"]["includeBootstrapMd"] is True

    tool_registry = (core / "tool-registry.jsonc").read_text(encoding="utf-8")
    assert '"arms": [' in tool_registry
    assert '"web_read"' in tool_registry


def test_cli_export_octopus_agents_accepts_output_dir(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "echo_engine.cli",
            "export-octopus-agents",
            "--output-dir",
            str(tmp_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert str(tmp_path / "echo_zero" / "profile.jsonc") in payload["written"]
    assert (tmp_path / "echo_zero" / "agent-core" / "SOUL.md").exists()


def test_cli_journal_outputs_json(tmp_path):
    env = os.environ.copy()
    env["ECHO_JOURNAL_PATH"] = str(tmp_path / "cli_journal.jsonl")
    result = subprocess.run(
        [sys.executable, "-m", "echo_engine.cli", "journal"],
        check=True,
        capture_output=True,
        env=env,
        text=True,
    )
    assert isinstance(json.loads(result.stdout), list)


def test_cli_review_candidate_outputs_decision_json(tmp_path):
    env = os.environ.copy()
    env["ECHO_JOURNAL_PATH"] = str(tmp_path / "cli_review_journal.jsonl")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "echo_engine.cli",
            "review-candidate",
            "--event-id",
            "missing",
            "--decision",
            "rejected",
            "--reason",
            "No source event in test.",
        ],
        check=True,
        capture_output=True,
        env=env,
        text=True,
    )
    assert json.loads(result.stdout)["event_type"] == "canon_decision"


def test_cli_promote_candidate_requires_accepted_event(tmp_path):
    env = os.environ.copy()
    env["ECHO_JOURNAL_PATH"] = str(tmp_path / "cli_promote_journal.jsonl")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "echo_engine.cli",
            "promote-candidate",
            "--event-id",
            "missing",
        ],
        capture_output=True,
        env=env,
        text=True,
    )
    assert result.returncode != 0
    assert "candidate event not found" in result.stderr
