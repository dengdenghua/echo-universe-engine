from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from echo_engine.config import get_settings


CURRENT_SCHEMA_VERSION = 1
JournalEventType = Literal["candidate_output", "canon_decision", "promotion", "realm_event"]
CanonDecision = Literal["candidate", "accepted", "rejected", "superseded"]


class JournalEvent(BaseModel):
    schema_version: int = CURRENT_SCHEMA_VERSION
    event_id: UUID = Field(default_factory=uuid4)
    event_type: JournalEventType
    ts: datetime = Field(default_factory=lambda: datetime.now(UTC))
    mode: str
    title: str
    output_path: str | None = None
    canon_status: CanonDecision = "candidate"
    canon_risks: list[str] = Field(default_factory=list)
    summary: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class JSONLJournal:
    def __init__(self, path: Path) -> None:
        self.path = path

    def append(self, event: JournalEvent) -> Path:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(event.model_dump_json() + "\n")
        return self.path

    def read_all(
        self,
        *,
        event_type: JournalEventType | None = None,
        limit: int | None = None,
    ) -> list[JournalEvent]:
        if not self.path.exists():
            return []

        events: list[JournalEvent] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                event = JournalEvent.model_validate(json.loads(line))
            except (json.JSONDecodeError, ValueError, TypeError):
                continue
            if event_type and event.event_type != event_type:
                continue
            events.append(event)

        if limit is not None and limit >= 0:
            return events[-limit:]
        return events


def candidate_review_state(root: Path | None = None) -> dict[str, JournalEvent]:
    decisions: dict[str, JournalEvent] = {}
    for event in journal(root).read_all(event_type="canon_decision"):
        source_event_id = event.metadata.get("source_event_id")
        if isinstance(source_event_id, str):
            decisions[source_event_id] = event
    return decisions


def candidate_promotion_state(root: Path | None = None) -> dict[str, JournalEvent]:
    promotions: dict[str, JournalEvent] = {}
    for event in journal(root).read_all(event_type="promotion"):
        source_event_id = event.metadata.get("source_event_id")
        if isinstance(source_event_id, str):
            promotions[source_event_id] = event
    return promotions


def candidate_queue(root: Path | None = None, limit: int | None = None) -> list[dict[str, Any]]:
    candidates = [
        event
        for event in journal(root).read_all()
        if event.event_type in {"candidate_output", "realm_event"}
    ]
    if limit is not None and limit >= 0:
        candidates = candidates[-limit:]
    decisions = candidate_review_state(root)
    promotions = candidate_promotion_state(root)
    rows: list[dict[str, Any]] = []
    for event in candidates:
        event_id = str(event.event_id)
        decision = decisions.get(event_id)
        promotion = promotions.get(event_id)
        status = "promoted" if promotion else decision.canon_status if decision else event.canon_status
        rows.append(
            {
                "event": event.model_dump(mode="json"),
                "latest_decision": decision.model_dump(mode="json") if decision else None,
                "promotion": promotion.model_dump(mode="json") if promotion else None,
                "status": status,
                "can_promote": bool(decision and decision.canon_status == "accepted" and not promotion),
            }
        )
    return rows


def journal_path(root: Path | None = None) -> Path:
    base = root or Path.cwd()
    configured = get_settings().journal_path
    if configured.is_absolute():
        return configured
    return base / configured


def journal(root: Path | None = None) -> JSONLJournal:
    return JSONLJournal(journal_path(root))


def record_candidate_output(
    *,
    mode: str,
    title: str,
    content: str,
    output_path: str | None,
    root: Path | None = None,
    canon_risks: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> JournalEvent:
    event = JournalEvent(
        event_type="candidate_output",
        mode=mode,
        title=title,
        output_path=output_path,
        canon_risks=canon_risks or [],
        summary=_summary(content),
        metadata=metadata or {},
    )
    journal(root).append(event)
    return event


def record_canon_decision(
    *,
    event_id: str,
    decision: CanonDecision,
    reason: str,
    root: Path | None = None,
    reviewer: str = "human",
) -> JournalEvent:
    source = _find_event(event_id, root)
    reviewer_auth: dict[str, Any] | None = None
    if source is not None and source.event_type == "realm_event":
        from echo_engine.reviewers import require_reviewer_for_event

        reviewer_auth = require_reviewer_for_event(reviewer=reviewer, event=source, root=root).model_dump(
            mode="json"
        )
    event = JournalEvent(
        event_type="canon_decision",
        mode=source.mode if source else "unknown",
        title=source.title if source else "Unknown candidate",
        output_path=source.output_path if source else None,
        canon_status=decision,
        canon_risks=source.canon_risks if source else [],
        summary=reason,
        metadata={
            "source_event_id": event_id,
            "reviewer": reviewer,
            "source_found": source is not None,
            **({"reviewer_authorization": reviewer_auth} if reviewer_auth else {}),
        },
    )
    journal(root).append(event)
    return event


def record_promotion(
    *,
    event_id: str,
    mode: str,
    title: str,
    source_path: str,
    promoted_path: str,
    root: Path | None = None,
) -> JournalEvent:
    event = JournalEvent(
        event_type="promotion",
        mode=mode,
        title=title,
        output_path=promoted_path,
        canon_status="accepted",
        summary=f"Promoted {source_path} to {promoted_path}.",
        metadata={"source_event_id": event_id, "source_path": source_path},
    )
    journal(root).append(event)
    return event


def _find_event(event_id: str, root: Path | None = None) -> JournalEvent | None:
    for event in journal(root).read_all():
        if str(event.event_id) == event_id:
            return event
    return None


def _summary(content: str, size: int = 360) -> str:
    text = " ".join(content.split())
    if len(text) <= size:
        return text
    return text[: size - 3].rstrip() + "..."
