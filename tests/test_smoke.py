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
import re
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


def test_api_serves_public_homepage_local_console_and_characters():
    client = TestClient(app)
    homepage = client.get("/")
    assert homepage.status_code == 200
    assert "THE ECHO AGE" in homepage.text
    assert "ECHO STATION" in homepage.text
    assert "ECHO STUDIO" in homepage.text
    assert "/console/" not in homepage.text
    universe = client.get("/universe/")
    assert universe.status_code == 200
    assert "ECHO UNIVERSE" in universe.text
    assert "ACROSS MEDIA" in universe.text
    console = client.get("/console/")
    assert console.status_code == 200
    assert "ECHO INTERNAL" in console.text
    response = client.get("/api/canon/characters")
    assert response.status_code == 200
    assert len(response.json()) >= 8


def test_delivery_includes_public_sites_and_never_falls_back_to_internal_console(
    tmp_path,
    monkeypatch,
):
    import echo_engine.api as api_module

    dockerfile = (CanonStore().root / "Dockerfile").read_text(encoding="utf-8")
    assert "COPY data ./data" in dockerfile
    assert "COPY homepage ./homepage" in dockerfile
    assert "COPY universe ./universe" in dockerfile
    assert "COPY review ./review" in dockerfile

    monkeypatch.setattr(api_module, "homepage_dir", tmp_path / "missing-homepage")
    assert api_module.homepage_index() == {
        "service": "echo-universe-engine",
        "homepage": "not installed",
    }


def test_reviewer_portal_is_separate_and_requires_a_reviewer_token():
    root = CanonStore().root
    html = (root / "review" / "index.html").read_text(encoding="utf-8")
    javascript = (root / "review" / "app.js").read_text(encoding="utf-8")
    assert 'name="robots" content="noindex,nofollow"' in html
    assert 'id="reviewer-token"' in html
    assert "echo.reviewer.token" in javascript
    assert "/api/canon/governance/candidates" in javascript
    assert "expected_revision_sha256" in javascript


def test_homepage_exposes_bilingual_locale_controls():
    root = CanonStore().root
    html = (root / "homepage" / "index.html").read_text(encoding="utf-8")
    javascript = (root / "homepage" / "app.js").read_text(encoding="utf-8")
    styles = (root / "homepage" / "styles.css").read_text(encoding="utf-8")
    assert 'data-locale="zh"' in html
    assert 'data-locale="en"' in html
    assert 'hreflang="zh-CN"' in html
    assert 'hreflang="en"' in html
    assert "localeMetadata" in javascript
    assert 'localStorage.setItem("echo.locale"' in javascript
    for product in (
        "ECHO OS",
        "ECHO STATION",
        "ECHO MEMORY",
        "ECHO HOME",
        "ECHO STUDIO",
        "ECHO UNIVERSE",
    ):
        assert product in html
    assert html.count('class="product-card system-card') == 6
    assert "<h3>ECHO CORE</h3>" not in html
    assert "<h3>ECHO MOBILE</h3>" not in html
    assert "<h3>ECHO WORKSPACE</h3>" not in html
    assert "<h3>ECHO VAULT</h3>" not in html
    assert "ECHO HEALTH" in html
    assert "THE ECHO AGE" in html
    assert "MEMORY SEA" in html
    assert "echo-age-logo.svg" in html
    assert "action-flow" in html
    assert 'id="cosmos-field"' in html
    assert 'id="hero-motion"' in html
    assert 'id="memory-motion"' in html
    assert '<button class="play-button" id="motion-toggle"' in html
    assert "universe-section" in html
    assert '<a href="/universe/" data-i18n="navUniverse">' in html
    assert "status-concept" in html
    assert "/console/" not in html
    assert "will-reveal" not in javascript
    assert "will-reveal" not in styles
    assert "reducedMotionQuery" in javascript
    assert "strokeEchoArc" in javascript
    assert "echoGapHalfAngle" in javascript
    assert "is-flowing" in javascript
    assert 'motionToggle?.addEventListener("click"' in javascript
    assert "prefers-reduced-motion" in styles
    for key in set(re.findall(r'data-i18n(?:-html|-aria)?="([^"]+)"', html)):
        assert len(re.findall(rf"(?m)^\s*{re.escape(key)}:", javascript)) == 2, key
    assert "roadmapNowBody" in html
    assert "Station" in html


def test_universe_page_exposes_canon_media_and_bilingual_controls():
    root = CanonStore().root
    html = (root / "universe" / "index.html").read_text(encoding="utf-8")
    javascript = (root / "universe" / "app.js").read_text(encoding="utf-8")
    styles = (root / "universe" / "styles.css").read_text(encoding="utf-8")
    assert 'data-locale="zh"' in html
    assert 'data-locale="en"' in html
    assert "Ghost Awakening" in html
    assert "WORLD ATLAS" in html
    assert "ACROSS MEDIA" in html
    assert 'data-media="story"' in html
    assert 'data-media="novel"' in html
    assert 'data-media="community"' in html
    assert 'data-media="comic"' in html
    assert 'data-media="motion"' in html
    assert 'data-media="screen"' in html
    assert "CANON PROTOCOL" in html
    assert "/console/" not in html
    assert "atlasData" in javascript
    assert "mediaData" in javascript
    assert 'production: "IN DEVELOPMENT"' in javascript
    assert 'meta[property="og:locale"]' in javascript
    assert "echo.universe.spoilers" in javascript
    assert "prefers-reduced-motion" in styles


def test_novel_serial_exposes_candidate_preview_reader_and_local_preferences():
    root = CanonStore().root
    catalog = (root / "universe" / "novel" / "index.html").read_text(encoding="utf-8")
    catalog_js = (root / "universe" / "novel" / "app.js").read_text(encoding="utf-8")
    reader = (root / "universe" / "novel" / "stranger-memory" / "index.html").read_text(encoding="utf-8")
    reader_js = (root / "universe" / "novel" / "stranger-memory" / "reader.js").read_text(encoding="utf-8")
    preview = (root / "universe" / "novel" / "content" / "stranger-memory.zh.md").read_text(encoding="utf-8")
    styles = (root / "universe" / "novel" / "styles.css").read_text(encoding="utf-8")

    assert "SERIAL FICTION · CANDIDATE PREVIEW" in catalog
    assert "CANDIDATE ≠ CANON" in catalog
    assert "/universe/novel/stranger-memory/" in catalog
    assert 'data-locale="zh"' in catalog
    assert 'data-locale="en"' in catalog
    assert "echo.novel.following" in catalog_js
    assert "echo.novel.stranger-memory.progress" in catalog_js
    assert "CANDIDATE PREVIEW" in reader
    assert 'id="font-down"' in reader
    assert 'id="theme-toggle"' in reader
    assert "stranger-memory.zh.md" in reader_js
    assert "echo.novel.reader.size" in reader_js
    assert "echo.novel.reader.theme" in reader_js
    assert 'id="governance-protocol"' in catalog
    assert 'data-resonance-choice="support"' in catalog
    assert 'data-resonance-choice="revise"' in catalog
    assert "正典委员会" in catalog
    assert 'id="committee-step-status"' in catalog
    assert "committee.threshold" in catalog_js
    assert "/api/canon/candidates/stranger-memory/governance" in catalog_js
    assert "/api/canon/candidates/stranger-memory/resonance" in catalog_js
    assert "resonanceBoundary" in catalog_js
    illustration_names = [
        "illustration-white-harbor-agnes-v1.png",
        "illustration-l7-collapse-agnes-v1.png",
        "illustration-stranger-hands-agnes-v1.png",
    ]
    for illustration_name in illustration_names:
        illustration = root / "universe" / "novel" / "assets" / illustration_name
        illustration_bytes = illustration.read_bytes()
        assert illustration_name in reader_js
        assert illustration_bytes.startswith(b"\x89PNG\r\n\x1a\n")
        assert len(illustration_bytes) >= 100_000
        assert int.from_bytes(illustration_bytes[16:20], "big") >= 1200
        assert int.from_bytes(illustration_bytes[20:24], "big") >= 800
    assert "白港不是被闹钟叫醒的" in preview
    assert "她哭是因为她不知道怎么停止当一个外科医生" in preview
    assert "Notes For Review" not in preview
    assert "Project E-01" not in preview
    assert "reader-site[data-theme=\"paper\"]" in styles
    assert "chapter-illustration" in styles
    assert "prefers-reduced-motion" in styles


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


def test_console_exposes_bilingual_locale_controls():
    root = CanonStore().root
    html = (root / "console" / "index.html").read_text(encoding="utf-8")
    app_js = (root / "console" / "app.js").read_text(encoding="utf-8")
    i18n_js = (root / "console" / "i18n.js").read_text(encoding="utf-8")
    assert 'data-locale="zh"' in html
    assert 'data-locale="en"' in html
    assert "/console/i18n.js" in html
    assert "EchoI18n" in app_js
    assert 'localStorage.setItem("echo.locale"' in i18n_js
    assert 'hour12: locale !== "zh"' in i18n_js


def test_console_uses_single_window_navigation_without_overlap():
    root = CanonStore().root
    html = (root / "console" / "index.html").read_text(encoding="utf-8")
    app_js = (root / "console" / "app.js").read_text(encoding="utf-8")
    styles = (root / "console" / "styles.css").read_text(encoding="utf-8")
    assert 'window world-window active' in html
    for name in ("characters", "factory", "assets", "memory", "octopus"):
        assert f'window {name}-window active' not in html
    assert 'item.classList.remove("active", "focused")' in app_js
    assert "installDrag" not in app_js
    assert html.count('class="window-close"') == 6
    assert "function closeWindow(panel)" in app_js
    assert "installWindowControls();" in app_js
    assert ".memory-window.active" in styles


def test_console_exposes_internal_canon_governance_controls():
    root = CanonStore().root
    app_js = (root / "console" / "app.js").read_text(encoding="utf-8")
    i18n_js = (root / "console" / "i18n.js").read_text(encoding="utf-8")
    styles = (root / "console" / "styles.css").read_text(encoding="utf-8")
    assert "/api/canon/governance/candidates" in app_js
    assert "committee-votes" in app_js
    assert "continuity-checks" in app_js
    assert "promoteGovernanceCandidate" in app_js
    assert "canonGovernance" in i18n_js
    assert ".governance-card" in styles


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
