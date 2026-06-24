from __future__ import annotations

from pathlib import Path
from typing import Any

from echo_engine.journal import JournalEvent, journal
from echo_engine.realms import RealmError, route_realm_review


class RealmEventError(ValueError):
    pass


def submit_realm_event(
    *,
    title: str,
    summary: str,
    scope: str = "personal",
    realm_id: str | None = None,
    submitter: str = "anonymous",
    content: str = "",
    canon_risks: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
    root: Path | None = None,
) -> JournalEvent:
    clean_title = _clean_required(title, "title")
    clean_summary = _clean_required(summary, "summary")
    try:
        route = route_realm_review(scope=scope, realm_id=realm_id, root=root)
    except RealmError as exc:
        raise RealmEventError(str(exc)) from exc
    event_metadata = {
        "submitter": submitter or "anonymous",
        "scope": route.requested_scope,
        "realm_id": route.resolved_realm_id,
        "realm_name": route.resolved_realm_name,
        "canon_tier": route.canon_tier,
        "approval": route.approval,
        "reviewer_group": route.reviewer_group,
        "escalation_path": route.escalation_path,
        **(metadata or {}),
    }
    event = JournalEvent(
        event_type="realm_event",
        mode="realm_event",
        title=clean_title,
        canon_risks=canon_risks or [],
        summary=content.strip() or clean_summary,
        metadata=event_metadata,
    )
    journal(root).append(event)
    return event


def realm_event_queue(
    *,
    reviewer_group: str | None = None,
    realm_id: str | None = None,
    root: Path | None = None,
    limit: int | None = None,
) -> list[JournalEvent]:
    events = journal(root).read_all(event_type="realm_event", limit=limit)
    if reviewer_group:
        events = [event for event in events if event.metadata.get("reviewer_group") == reviewer_group]
    if realm_id:
        events = [event for event in events if event.metadata.get("realm_id") == realm_id]
    return events


def _clean_required(value: str, field: str) -> str:
    clean = (value or "").strip()
    if not clean:
        raise RealmEventError(f"{field} is required")
    return clean
