"""journal.py 与 promotion.py 的模块级测试。

隔离约定：所有读写都显式传 root=tmp_path（journal_path 为相对路径时拼接 root），
不触碰真实 data/，conftest 的泄漏守卫兜底。
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from echo_engine.journal import (
    JournalEvent,
    candidate_promotion_state,
    candidate_queue,
    candidate_review_state,
    journal,
    journal_path,
    record_candidate_output,
    record_canon_decision,
    record_promotion,
)
from echo_engine.promotion import PromotionError, promote_candidate


def _candidate(root: Path, *, title: str = "Test Story", output: str = "outputs/story-1.md") -> JournalEvent:
    (root / output).parent.mkdir(parents=True, exist_ok=True)
    (root / output).write_text("once upon a time", encoding="utf-8")
    return record_candidate_output(
        mode="story",
        title=title,
        content="once upon a time",
        output_path=output,
        root=root,
    )


# ── journal 基础 ──────────────────────────────────────────────


def test_journal_path_joins_root_for_relative_setting(tmp_path):
    assert journal_path(tmp_path) == tmp_path / "data" / "echo_journal.jsonl"


def test_record_candidate_output_roundtrip(tmp_path):
    event = record_candidate_output(
        mode="story",
        title="长标题  带多余空白",
        content="line one\n\nline two",
        output_path="outputs/a.md",
        root=tmp_path,
    )
    loaded = journal(tmp_path).read_all()
    assert len(loaded) == 1
    assert loaded[0].event_id == event.event_id
    assert loaded[0].event_type == "candidate_output"
    assert loaded[0].summary == "line one line two"


def test_summary_truncates_long_content(tmp_path):
    event = record_candidate_output(
        mode="lore",
        title="L",
        content="字" * 500,
        output_path=None,
        root=tmp_path,
    )
    assert len(event.summary) == 360
    assert event.summary.endswith("...")


def test_read_all_skips_malformed_lines_and_filters(tmp_path):
    good = record_candidate_output(mode="lore", title="ok", content="x", output_path=None, root=tmp_path)
    with journal(tmp_path).path.open("a", encoding="utf-8") as handle:
        handle.write("{not json}\n")
        handle.write(json.dumps({"event_type": "unknown_kind"}) + "\n")
    assert journal(tmp_path).read_all(event_type="candidate_output")[0].event_id == good.event_id
    assert journal(tmp_path).read_all(event_type="promotion") == []


def test_read_all_limit_keeps_latest(tmp_path):
    for i in range(5):
        record_candidate_output(mode="lore", title=f"t{i}", content="x", output_path=None, root=tmp_path)
    limited = journal(tmp_path).read_all(limit=2)
    assert [e.title for e in limited] == ["t3", "t4"]
    assert journal(tmp_path).read_all(limit=0) == []


def test_read_all_missing_file_returns_empty(tmp_path):
    assert journal(tmp_path / "void").read_all() == []


# ── 决策与队列状态机 ─────────────────────────────────────────


def test_canon_decision_for_unknown_event(tmp_path):
    decision = record_canon_decision(event_id="nope", decision="rejected", reason="ghost", root=tmp_path)
    assert decision.metadata["source_found"] is False
    assert decision.mode == "unknown"
    assert decision.title == "Unknown candidate"


def test_canon_decision_links_source_and_latest_wins(tmp_path):
    event = _candidate(tmp_path)
    record_canon_decision(event_id=str(event.event_id), decision="rejected", reason="first", root=tmp_path)
    latest = record_canon_decision(event_id=str(event.event_id), decision="accepted", reason="second", root=tmp_path)
    assert latest.metadata["source_found"] is True
    state = candidate_review_state(tmp_path)
    assert state[str(event.event_id)].canon_status == "accepted"
    assert state[str(event.event_id)].summary == "second"


def test_candidate_queue_status_lifecycle(tmp_path):
    event = _candidate(tmp_path)
    queue = candidate_queue(tmp_path)
    assert len(queue) == 1
    assert queue[0]["status"] == "candidate"
    assert queue[0]["can_promote"] is False

    record_canon_decision(event_id=str(event.event_id), decision="accepted", reason="ok", root=tmp_path)
    queue = candidate_queue(tmp_path)
    assert queue[0]["status"] == "accepted"
    assert queue[0]["can_promote"] is True
    assert queue[0]["promotion"] is None

    record_promotion(
        event_id=str(event.event_id),
        mode="story",
        title=event.title,
        source_path="outputs/story-1.md",
        promoted_path="stories/promoted_test-story.md",
        root=tmp_path,
    )
    queue = candidate_queue(tmp_path)
    assert queue[0]["status"] == "promoted"
    assert queue[0]["can_promote"] is False
    assert queue[0]["promotion"] is not None


def test_queue_limit_applies_before_status_join(tmp_path):
    first = _candidate(tmp_path, title="First", output="outputs/a.md")
    _candidate(tmp_path, title="Second", output="outputs/b.md")
    record_canon_decision(event_id=str(first.event_id), decision="accepted", reason="ok", root=tmp_path)
    rows = candidate_queue(tmp_path, limit=1)
    assert len(rows) == 1
    assert rows[0]["event"]["title"] == "Second"


# ── promotion ────────────────────────────────────────────────


def test_promote_requires_existing_candidate(tmp_path):
    with pytest.raises(PromotionError, match="candidate event not found"):
        promote_candidate("missing", root=tmp_path)


def test_promote_requires_accepted_decision(tmp_path):
    event = _candidate(tmp_path)
    with pytest.raises(PromotionError, match="must be accepted"):
        promote_candidate(str(event.event_id), root=tmp_path)
    record_canon_decision(event_id=str(event.event_id), decision="rejected", reason="no", root=tmp_path)
    with pytest.raises(PromotionError, match="must be accepted"):
        promote_candidate(str(event.event_id), root=tmp_path)


def test_promote_requires_existing_output_file(tmp_path):
    event = record_candidate_output(
        mode="story", title="Ghost", content="x", output_path="outputs/gone.md", root=tmp_path
    )
    record_canon_decision(event_id=str(event.event_id), decision="accepted", reason="ok", root=tmp_path)
    with pytest.raises(PromotionError, match="candidate output not found"):
        promote_candidate(str(event.event_id), root=tmp_path)


def test_promote_rejects_escaping_paths(tmp_path):
    event = record_candidate_output(
        mode="story", title="Escape", content="x", output_path="../outside.md", root=tmp_path
    )
    record_canon_decision(event_id=str(event.event_id), decision="accepted", reason="ok", root=tmp_path)
    with pytest.raises(PromotionError, match="escapes its allowed root"):
        promote_candidate(str(event.event_id), root=tmp_path)


def test_promote_story_happy_path_and_double_promotion_guard(tmp_path):
    event = _candidate(tmp_path)
    record_canon_decision(event_id=str(event.event_id), decision="accepted", reason="ship it", root=tmp_path)

    result = promote_candidate(str(event.event_id), root=tmp_path)
    assert result.mode == "story"
    assert result.source_path == "outputs/story-1.md"
    assert result.promoted_path == "stories/promoted_test-story.md"

    promoted = tmp_path / "stories" / "promoted_test-story.md"
    assert promoted.exists()
    text = promoted.read_text(encoding="utf-8")
    assert f"source_event_id: {event.event_id}" in text
    assert "review_reason: ship it" in text
    assert "once upon a time" in text

    assert candidate_promotion_state(tmp_path)[str(event.event_id)].canon_status == "accepted"
    with pytest.raises(PromotionError, match="already promoted"):
        promote_candidate(str(event.event_id), root=tmp_path)


def test_promote_custom_target_and_filename(tmp_path):
    event = _candidate(tmp_path)
    record_canon_decision(event_id=str(event.event_id), decision="accepted", reason="ok", root=tmp_path)
    result = promote_candidate(
        str(event.event_id), root=tmp_path, target_dir="stories/archive", filename="custom.md"
    )
    assert result.promoted_path == "stories/archive/custom.md"
    assert (tmp_path / "stories" / "archive" / "custom.md").exists()


def test_promote_rejects_unknown_mode(tmp_path):
    (root := tmp_path / "outputs").mkdir(parents=True)
    (root / "weird.md").write_text("x", encoding="utf-8")
    event = record_candidate_output(
        mode="unknown_mode", title="Weird", content="x", output_path="outputs/weird.md", root=tmp_path
    )
    record_canon_decision(event_id=str(event.event_id), decision="accepted", reason="ok", root=tmp_path)
    with pytest.raises(PromotionError, match="no promotion target configured for mode: unknown_mode"):
        promote_candidate(str(event.event_id), root=tmp_path)
