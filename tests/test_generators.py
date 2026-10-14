"""generators.py 与 llm.py 的模块级测试。

agents 生成的确定性测试策略:强制 ECHO_MODEL_PROVIDER=stub(stub 直接回传参考稿,
离线无网络),配 get_settings.cache_clear() 防 lru_cache 吃到会话早期的真实配置。
"""

from __future__ import annotations

import pytest

from echo_engine.config import get_settings
from echo_engine.generators import (
    _recent_candidate_events,
    _render_recent_candidates,
    _slugify,
    _write_output,
    run_character_agent,
    run_consistency_agent,
    run_relationship_agent,
    run_story_agent,
)
from echo_engine.journal import journal, record_candidate_output, record_canon_decision
from echo_engine.llm import (
    LLMConfigurationError,
    LLMRequest,
    _extract_openai_content,
    generate_candidate_content,
    llm_enabled,
)


@pytest.fixture(autouse=True)
def _force_stub_llm(monkeypatch):
    """generation 走 stub(回传参考稿),不依赖 .env 或真实模型。"""
    monkeypatch.setenv("ECHO_MODEL_PROVIDER", "stub")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


# ── 纯函数 ────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Story Beat: The Person!", "story-beat-the-person"),
        ("中文标题", "untitled"),  # 无合法字符 → 兜底
        ("--x--", "x"),
    ],
)
def test_slugify(text, expected):
    assert _slugify(text) == expected


def test_write_output_writes_file_and_journal_candidate(tmp_path):
    path = _write_output("story", "My Beat", "content here", tmp_path, canon_risks=["r1"])
    assert path == path.replace("\\", "/")
    assert (tmp_path / path).read_text(encoding="utf-8") == "content here"
    events = journal(tmp_path).read_all(event_type="candidate_output")
    assert len(events) == 1
    assert events[0].title == "My Beat"
    assert events[0].canon_risks == ["r1"]
    assert events[0].metadata == {}


# ── agent 端到端(stub provider,离线) ─────────────────────────


def test_run_story_agent_writes_candidate(tmp_path):
    result = run_story_agent(root=tmp_path)
    assert result.mode == "story"
    assert result.title == "Story Beat: The Person Who Lost Their Body"
    assert result.canon_risks == ["Do not collapse legal identity into soul metaphysics."]
    assert result.output_path and result.output_path.startswith("outputs/story/")
    written = (tmp_path / result.output_path).read_text(encoding="utf-8")
    assert "## Logline" in written  # stub 回传参考稿
    assert journal(tmp_path).read_all(event_type="candidate_output")


def test_run_character_agent_next_id_from_existing_cards(tmp_path):
    (tmp_path / "characters").mkdir()
    (tmp_path / "characters" / "a.md").write_text(
        "# a\n\n```yaml\nid: '001'\nname: Alpha\n```\n", encoding="utf-8"
    )
    (tmp_path / "characters" / "b.md").write_text(
        "# b\n\n```yaml\nid: '002'\nname: Beta\n```\n", encoding="utf-8"
    )
    result = run_character_agent(root=tmp_path)
    assert result.title == "Candidate Character 003: Mira Voss"


def test_run_character_agent_first_id_when_store_empty(tmp_path):
    result = run_character_agent(root=tmp_path)
    assert result.title == "Candidate Character 001: Mira Voss"


def test_run_relationship_agent_dedupe_branch(tmp_path):
    first = run_relationship_agent(root=tmp_path)
    assert first.title == "Relationship Update: Zero / Mother / Luna"

    # 已存在 zero-mother-luna 产物 → 换 Lin Qiao / Ren Vale 线并带 dedupe 元数据
    (tmp_path / "outputs" / "relationship").mkdir(parents=True, exist_ok=True)
    (tmp_path / "outputs" / "relationship" / "20260101-zero-mother-luna.md").write_text(
        "old", encoding="utf-8"
    )
    second = run_relationship_agent(root=tmp_path)
    assert second.title == "Relationship Update: Lin Qiao / Ren Vale / Home Core"


# ── consistency agent ────────────────────────────────────────


def test_recent_candidate_events_filters_consistency_mode(tmp_path):
    record_candidate_output(mode="story", title="s", content="x", output_path=None, root=tmp_path)
    record_candidate_output(
        mode="consistency", title="audit", content="x", output_path=None, root=tmp_path
    )
    events = _recent_candidate_events(tmp_path)
    assert [e.mode for e in events] == ["story"]


def test_render_recent_candidates_empty_and_with_decision(tmp_path):
    assert _render_recent_candidates([], tmp_path) == "- No candidate outputs recorded yet."

    event = record_candidate_output(
        mode="lore", title="L", content="x", output_path="outputs/lore/a.md", root=tmp_path
    )
    plain = _render_recent_candidates([event], tmp_path)
    assert "[lore] L" in plain and "status: candidate" in plain

    record_canon_decision(event_id=str(event.event_id), decision="accepted", reason="ok", root=tmp_path)
    reviewed = _render_recent_candidates([event], tmp_path)
    assert "status: accepted" in reviewed and "review: ok" in reviewed


def test_run_consistency_agent_reports_queue_and_counts(tmp_path):
    record_candidate_output(mode="story", title="Seeded Beat", content="x", output_path=None, root=tmp_path)
    result = run_consistency_agent(root=tmp_path)
    assert result.mode == "consistency"
    assert "Seeded Beat" in result.content  # 候选队列进入 audit 正文
    assert "Bible files:" in result.content
    # 本身作为 consistency 候选落 journal,但 metadata 记录的是排除自身前的审阅数
    assert result.output_path and result.output_path.startswith("outputs/consistency/")


# ── llm.py ───────────────────────────────────────────────────


def test_stub_provider_returns_reference_draft(tmp_path):
    request = LLMRequest(mode="story", title="t", instructions="i", reference_draft="DRAFT", root=tmp_path)
    assert generate_candidate_content(request) == "DRAFT"
    assert llm_enabled() is False


def test_unsupported_provider_raises(monkeypatch):
    monkeypatch.setenv("ECHO_MODEL_PROVIDER", "magic-model")
    get_settings.cache_clear()
    with pytest.raises(LLMConfigurationError, match="Unsupported ECHO_MODEL_PROVIDER"):
        generate_candidate_content(LLMRequest(mode="m", title="t", instructions="i", reference_draft="d"))
    get_settings.cache_clear()


def test_non_stub_provider_requires_base_url(monkeypatch):
    monkeypatch.setenv("ECHO_MODEL_PROVIDER", "relay")
    monkeypatch.delenv("ECHO_MODEL_BASE_URL", raising=False)
    get_settings.cache_clear()
    with pytest.raises(LLMConfigurationError, match="ECHO_MODEL_BASE_URL"):
        generate_candidate_content(LLMRequest(mode="m", title="t", instructions="i", reference_draft="d"))
    get_settings.cache_clear()


@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        ({"choices": [{"message": {"content": " hi "}}]}, " hi "),  # strip 在 generate 层
        ({"choices": [{"text": "legacy"}]}, "legacy"),
        ({"choices": []}, ""),
        ({"choices": [{"message": {"content": 42}}]}, ""),
        ({}, ""),
        ({"choices": ["not-a-dict"]}, ""),
    ],
)
def test_extract_openai_content(payload, expected):
    assert _extract_openai_content(payload) == expected


# ── journal 路径隔离回归(generators → journal 联动) ───────────


def test_written_candidate_round_trips_through_promotion_state(tmp_path):
    result = run_story_agent(root=tmp_path)
    (tmp_path / result.output_path).exists()
    queue = None
    from echo_engine.journal import candidate_queue

    queue = candidate_queue(tmp_path)
    assert len(queue) == 1
    assert queue[0]["event"]["output_path"] == result.output_path
    assert queue[0]["status"] == "candidate"
