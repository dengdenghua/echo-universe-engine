from __future__ import annotations

from pathlib import Path

import yaml

from echo_engine.journal import JournalEvent
from echo_engine.models import ReviewerAuthorization, ReviewerGroup


REVIEWERS_PATH = Path("data/reviewers.yaml")


class ReviewerError(ValueError):
    pass


def list_reviewer_groups(root: Path | None = None) -> list[ReviewerGroup]:
    return sorted(_load_reviewer_groups(root).values(), key=lambda group: group.id)


def get_reviewer_group(group_id: str, root: Path | None = None) -> ReviewerGroup:
    clean_id = _clean_required(group_id, "group_id")
    groups = _load_reviewer_groups(root)
    group = groups.get(clean_id)
    if group is None:
        raise ReviewerError(f"reviewer group not found: {clean_id}")
    return group


def authorize_reviewer_for_event(
    *,
    reviewer: str,
    event: JournalEvent,
    root: Path | None = None,
) -> ReviewerAuthorization:
    clean_reviewer = _clean_required(reviewer, "reviewer")
    if event.event_type != "realm_event":
        return ReviewerAuthorization(
            reviewer=clean_reviewer,
            allowed=True,
            reason="non-realm candidate uses legacy review path",
        )
    required_group = str(event.metadata.get("reviewer_group") or "").strip()
    realm_id = str(event.metadata.get("realm_id") or "").strip()
    scope = str(event.metadata.get("scope") or "").strip()
    if not required_group:
        return ReviewerAuthorization(
            reviewer=clean_reviewer,
            allowed=False,
            reason="realm event has no reviewer_group metadata",
        )
    groups = _load_reviewer_groups(root)
    for group in groups.values():
        if clean_reviewer not in group.members:
            continue
        if _matches(required_group, group.can_review_groups):
            return _allowed(clean_reviewer, required_group, group.id, "matched reviewer group")
        if realm_id and _matches(realm_id, group.can_review_realms):
            return _allowed(clean_reviewer, required_group, group.id, "matched realm permission")
        if scope and _matches(scope, group.can_review_scopes):
            return _allowed(clean_reviewer, required_group, group.id, "matched scope permission")
    return ReviewerAuthorization(
        reviewer=clean_reviewer,
        allowed=False,
        reason=f"reviewer is not authorized for {required_group}",
        required_group=required_group,
    )


def require_reviewer_for_event(
    *,
    reviewer: str,
    event: JournalEvent,
    root: Path | None = None,
) -> ReviewerAuthorization:
    auth = authorize_reviewer_for_event(reviewer=reviewer, event=event, root=root)
    if not auth.allowed:
        raise ReviewerError(auth.reason)
    return auth


def _allowed(
    reviewer: str,
    required_group: str,
    matched_group: str,
    reason: str,
) -> ReviewerAuthorization:
    return ReviewerAuthorization(
        reviewer=reviewer,
        allowed=True,
        reason=reason,
        required_group=required_group,
        matched_group=matched_group,
    )


def _matches(value: str, allowed: list[str]) -> bool:
    return "*" in allowed or value in allowed


def _load_reviewer_groups(root: Path | None = None) -> dict[str, ReviewerGroup]:
    path = _reviewers_path(root)
    if not path.exists():
        raise ReviewerError(f"reviewers file not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    raw_groups = data.get("groups", {})
    if not isinstance(raw_groups, dict):
        raise ReviewerError("reviewers file must contain a 'groups' mapping")
    return {group_id: ReviewerGroup.model_validate(raw) for group_id, raw in raw_groups.items()}


def _reviewers_path(root: Path | None = None) -> Path:
    base = root or Path.cwd()
    return base / REVIEWERS_PATH


def _clean_required(value: str, field: str) -> str:
    clean = (value or "").strip()
    if not clean:
        raise ReviewerError(f"{field} is required")
    return clean
