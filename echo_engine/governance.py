from __future__ import annotations

import hashlib
import hmac
import json
import os
import sqlite3
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

import yaml
from pydantic import BaseModel, Field, model_validator

from echo_engine.config import get_settings
from echo_engine.reviewers import ReviewerError, get_reviewer_group


ResonanceChoice = Literal["support", "revise"]
CommitteeDecision = Literal["approve", "reject"]
ContinuityVerdict = Literal["pass", "veto"]


class GovernanceError(ValueError):
    pass


class PublicCanonCandidate(BaseModel):
    id: str
    version: str
    mode: str = "story"
    title: dict[str, str]
    work: dict[str, str]
    source_path: str
    public_href: str
    target_path: str
    reviewer_group: str
    required_approvals: int = Field(default=2, ge=1)
    continuity_reviewers: list[str] = Field(min_length=1)
    resonance_enabled: bool = True

    @model_validator(mode="after")
    def validate_localized_copy(self) -> "PublicCanonCandidate":
        for field_name in ("title", "work"):
            value = getattr(self, field_name)
            if not value.get("zh") or not value.get("en"):
                raise ValueError(f"{field_name} requires zh and en values")
        return self


def list_public_candidates(root: Path | None = None) -> list[PublicCanonCandidate]:
    path = _registry_path(root)
    if not path.exists():
        return []
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    candidates = raw.get("candidates", {})
    if not isinstance(candidates, dict):
        raise GovernanceError("public candidate registry must contain a candidates mapping")
    result: list[PublicCanonCandidate] = []
    for candidate_id, value in candidates.items():
        if not isinstance(value, dict):
            raise GovernanceError(f"invalid public candidate: {candidate_id}")
        result.append(PublicCanonCandidate.model_validate({"id": candidate_id, **value}))
    return sorted(result, key=lambda item: item.id)


def get_public_candidate(candidate_id: str, root: Path | None = None) -> PublicCanonCandidate:
    clean_id = _clean_id(candidate_id)
    for candidate in list_public_candidates(root):
        if candidate.id == clean_id:
            return candidate
    raise GovernanceError(f"public candidate not found: {clean_id}")


def voter_key(candidate_id: str, identity: str, secret: str) -> str:
    clean_identity = (identity or "").strip()
    if not clean_identity:
        raise GovernanceError("voter identity is required")
    clean_secret = (secret or "").strip()
    if not clean_secret:
        raise GovernanceError("governance secret is required")
    digest = hmac.new(
        clean_secret.encode("utf-8"),
        f"{_clean_id(candidate_id)}:{clean_identity}".encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"rv1:{digest}"


def set_resonance(
    candidate_id: str,
    *,
    identity: str,
    identity_kind: Literal["registered", "anonymous"],
    choice: ResonanceChoice | None,
    secret: str,
    root: Path | None = None,
) -> dict[str, Any]:
    candidate = get_public_candidate(candidate_id, root)
    if not candidate.resonance_enabled:
        raise GovernanceError("community resonance is closed for this candidate")
    actor_key = voter_key(candidate.id, identity, secret)
    now = _now()
    with _connect(root) as connection:
        previous = connection.execute(
            "SELECT choice FROM canon_resonance_votes WHERE candidate_id = ? AND voter_key = ?",
            (candidate.id, actor_key),
        ).fetchone()
        if choice is None:
            connection.execute(
                "DELETE FROM canon_resonance_votes WHERE candidate_id = ? AND voter_key = ?",
                (candidate.id, actor_key),
            )
            action = "withdraw"
        else:
            connection.execute(
                """
                INSERT INTO canon_resonance_votes
                    (candidate_id, voter_key, identity_kind, choice, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(candidate_id, voter_key) DO UPDATE SET
                    identity_kind = excluded.identity_kind,
                    choice = excluded.choice,
                    updated_at = excluded.updated_at
                """,
                (candidate.id, actor_key, identity_kind, choice, now, now),
            )
            action = "cast" if previous is None else "change"
        _record_event(
            connection,
            event_type="resonance_vote",
            candidate_id=candidate.id,
            revision_sha256=None,
            actor_key=actor_key,
            action=action,
            decision=choice,
            reason="",
            metadata={"identity_kind": identity_kind},
        )
    return get_governance_state(
        candidate.id,
        root=root,
        viewer_identity=identity,
        viewer_secret=secret,
    )


def record_committee_vote(
    candidate_id: str,
    *,
    reviewer: str,
    decision: CommitteeDecision,
    expected_revision_sha256: str,
    actor_identity: str,
    auth_kind: str,
    reason: str,
    root: Path | None = None,
) -> dict[str, Any]:
    candidate = get_public_candidate(candidate_id, root)
    clean_reviewer = _clean_reviewer(reviewer)
    members = _committee_members(candidate, root)
    if clean_reviewer not in members:
        raise GovernanceError(f"reviewer is not a member of {candidate.reviewer_group}")
    revision = _revision_sha256(candidate, members, root)
    _require_expected_revision(revision, expected_revision_sha256)
    now = _now()
    with _connect(root) as connection:
        connection.execute("BEGIN IMMEDIATE")
        actor_conflict = connection.execute(
            """
            SELECT reviewer FROM canon_committee_reviews
            WHERE candidate_id = ? AND revision_sha256 = ?
              AND authenticated_actor = ? AND reviewer != ?
            LIMIT 1
            """,
            (candidate.id, revision, actor_identity, clean_reviewer),
        ).fetchone()
        if actor_conflict:
            raise GovernanceError("one authenticated reviewer cannot occupy multiple committee seats")
        try:
            connection.execute(
                """
                INSERT INTO canon_committee_reviews
                    (candidate_id, revision_sha256, reviewer, authenticated_actor, auth_kind,
                     decision, reason, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(candidate_id, revision_sha256, reviewer) DO UPDATE SET
                    authenticated_actor = excluded.authenticated_actor,
                    auth_kind = excluded.auth_kind,
                    decision = excluded.decision,
                    reason = excluded.reason,
                    updated_at = excluded.updated_at
                """,
                (
                    candidate.id,
                    revision,
                    clean_reviewer,
                    actor_identity,
                    auth_kind,
                    decision,
                    reason.strip(),
                    now,
                    now,
                ),
            )
        except sqlite3.IntegrityError as exc:
            raise GovernanceError(
                "one authenticated reviewer cannot occupy multiple committee seats"
            ) from exc
        _record_event(
            connection,
            event_type="committee_vote",
            candidate_id=candidate.id,
            revision_sha256=revision,
            actor_key=clean_reviewer,
            action="review",
            decision=decision,
            reason=reason,
            metadata={
                "reviewer_group": candidate.reviewer_group,
                "authenticated_actor": actor_identity,
                "auth_kind": auth_kind,
            },
        )
    return get_governance_state(candidate.id, root=root, include_private=True)


def record_continuity_check(
    candidate_id: str,
    *,
    reviewer: str,
    verdict: ContinuityVerdict,
    expected_revision_sha256: str,
    actor_identity: str,
    auth_kind: str,
    reason: str,
    issues: list[str] | None = None,
    root: Path | None = None,
) -> dict[str, Any]:
    candidate = get_public_candidate(candidate_id, root)
    clean_reviewer = _clean_reviewer(reviewer)
    if clean_reviewer not in candidate.continuity_reviewers:
        raise GovernanceError("reviewer is not authorized for continuity checks")
    members = _committee_members(candidate, root)
    revision = _revision_sha256(candidate, members, root)
    _require_expected_revision(revision, expected_revision_sha256)
    clean_issues = sorted({item.strip() for item in issues or [] if item.strip()})
    now = _now()
    with _connect(root) as connection:
        connection.execute("BEGIN IMMEDIATE")
        actor_conflict = connection.execute(
            """
            SELECT reviewer FROM canon_continuity_checks
            WHERE candidate_id = ? AND revision_sha256 = ?
              AND authenticated_actor = ? AND reviewer != ?
            LIMIT 1
            """,
            (candidate.id, revision, actor_identity, clean_reviewer),
        ).fetchone()
        if actor_conflict:
            raise GovernanceError(
                "one authenticated reviewer cannot occupy multiple continuity seats"
            )
        existing = connection.execute(
            """
            SELECT verdict FROM canon_continuity_checks
            WHERE candidate_id = ? AND revision_sha256 = ? AND reviewer = ?
            """,
            (candidate.id, revision, clean_reviewer),
        ).fetchone()
        if existing and existing["verdict"] == "veto" and verdict == "pass":
            raise GovernanceError("a continuity veto requires a new content revision")
        try:
            connection.execute(
                """
                INSERT INTO canon_continuity_checks
                    (candidate_id, revision_sha256, reviewer, authenticated_actor, auth_kind,
                     verdict, reason, issues_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(candidate_id, revision_sha256, reviewer) DO UPDATE SET
                    authenticated_actor = excluded.authenticated_actor,
                    auth_kind = excluded.auth_kind,
                    verdict = excluded.verdict,
                    reason = excluded.reason,
                    issues_json = excluded.issues_json,
                    updated_at = excluded.updated_at
                """,
                (
                    candidate.id,
                    revision,
                    clean_reviewer,
                    actor_identity,
                    auth_kind,
                    verdict,
                    reason.strip(),
                    json.dumps(clean_issues),
                    now,
                    now,
                ),
            )
        except sqlite3.IntegrityError as exc:
            raise GovernanceError(
                "one authenticated reviewer cannot occupy multiple continuity seats"
            ) from exc
        _record_event(
            connection,
            event_type="continuity_check",
            candidate_id=candidate.id,
            revision_sha256=revision,
            actor_key=clean_reviewer,
            action="check",
            decision=verdict,
            reason=reason,
            metadata={
                "issues": clean_issues,
                "authenticated_actor": actor_identity,
                "auth_kind": auth_kind,
            },
        )
    return get_governance_state(candidate.id, root=root, include_private=True)


def get_governance_state(
    candidate_id: str,
    *,
    root: Path | None = None,
    viewer_identity: str | None = None,
    viewer_secret: str | None = None,
    include_private: bool = False,
) -> dict[str, Any]:
    candidate = get_public_candidate(candidate_id, root)
    members = _committee_members(candidate, root)
    revision = _revision_sha256(candidate, members, root)
    if candidate.required_approvals > len(members):
        raise GovernanceError("required approvals exceed committee size")
    viewer = None
    if viewer_identity and viewer_secret:
        viewer = voter_key(candidate.id, viewer_identity, viewer_secret)
    base = root or get_settings().root
    with _connect(root) as connection:
        return _state_from_connection(
            connection,
            candidate,
            revision,
            members,
            base_root=base,
            viewer_key=viewer,
            include_private=include_private,
        )


def list_governance_states(
    *,
    root: Path | None = None,
    include_private: bool = False,
) -> list[dict[str, Any]]:
    return [
        get_governance_state(candidate.id, root=root, include_private=include_private)
        for candidate in list_public_candidates(root)
    ]


def promote_public_candidate(
    candidate_id: str,
    *,
    expected_revision_sha256: str,
    root: Path | None = None,
) -> dict[str, Any]:
    candidate = get_public_candidate(candidate_id, root)
    members = _committee_members(candidate, root)
    base = root or get_settings().root
    source = _inside(base, candidate.source_path)
    target = _inside(base, candidate.target_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with _connect(root) as connection:
        connection.execute("BEGIN IMMEDIATE")
        content = source.read_bytes()
        revision = _revision_sha256_from_bytes(candidate, members, content)
        _require_expected_revision(revision, expected_revision_sha256)
        state = _state_from_connection(
            connection,
            candidate,
            revision,
            members,
            base_root=base,
            viewer_key=None,
            include_private=True,
        )
        if state["promotion"]["promoted"]:
            raise GovernanceError("candidate is already promoted")
        if not state["promotion_gate"]["can_promote"]:
            blockers = ", ".join(state["promotion_gate"]["blockers"])
            raise GovernanceError(f"promotion gate blocked: {blockers}")
        header = (
            "<!--\n"
            "Promoted through ECHO canon governance.\n"
            f"candidate_id: {candidate.id}\n"
            f"candidate_version: {candidate.version}\n"
            f"revision_sha256: {revision}\n"
            f"committee_rule: {candidate.required_approvals}/{len(members)}\n"
            "-->\n\n"
        ).encode("utf-8")
        promoted_bytes = header + content
        if target.exists():
            if target.read_bytes() != promoted_bytes:
                raise GovernanceError(f"promotion target already exists: {candidate.target_path}")
        else:
            _atomic_write_bytes(target, promoted_bytes)
        promoted_at = _now()
        output_sha256 = hashlib.sha256(promoted_bytes).hexdigest()
        connection.execute(
            """
            INSERT INTO canon_governance_promotions
                (candidate_id, revision_sha256, output_path, output_sha256, promoted_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (candidate.id, revision, candidate.target_path, output_sha256, promoted_at),
        )
        _record_event(
            connection,
            event_type="promotion",
            candidate_id=candidate.id,
            revision_sha256=revision,
            actor_key="system",
            action="promote",
            decision="accepted",
            reason="Promotion gate satisfied.",
            metadata={
                "output_path": candidate.target_path,
                "output_sha256": output_sha256,
            },
        )
    return {
        "ok": True,
        "candidate_id": candidate.id,
        "revision_sha256": revision,
        "output_path": candidate.target_path,
    }


def _state_from_connection(
    connection: sqlite3.Connection,
    candidate: PublicCanonCandidate,
    revision: str,
    members: list[str],
    *,
    base_root: Path,
    viewer_key: str | None,
    include_private: bool,
) -> dict[str, Any]:
    resonance_rows = connection.execute(
        """
        SELECT identity_kind, choice, COUNT(*) AS count
        FROM canon_resonance_votes
        WHERE candidate_id = ?
        GROUP BY identity_kind, choice
        """,
        (candidate.id,),
    ).fetchall()
    resonance = {
        "registered": {"support": 0, "revise": 0, "total": 0},
        "anonymous": {"support": 0, "revise": 0, "total": 0},
    }
    for row in resonance_rows:
        bucket = resonance[row["identity_kind"]]
        bucket[row["choice"]] = int(row["count"])
        bucket["total"] += int(row["count"])
    total_support = resonance["registered"]["support"] + resonance["anonymous"]["support"]
    total_revise = resonance["registered"]["revise"] + resonance["anonymous"]["revise"]
    total_votes = total_support + total_revise
    viewer_choice = None
    if viewer_key:
        row = connection.execute(
            "SELECT choice, identity_kind FROM canon_resonance_votes WHERE candidate_id = ? AND voter_key = ?",
            (candidate.id, viewer_key),
        ).fetchone()
        if row:
            viewer_choice = row["choice"]

    review_rows = connection.execute(
        """
        SELECT reviewer, decision, reason, authenticated_actor, auth_kind, updated_at
        FROM canon_committee_reviews
        WHERE candidate_id = ? AND revision_sha256 = ?
        """,
        (candidate.id, revision),
    ).fetchall()
    review_by_member = {
        row["reviewer"]: row
        for row in review_rows
        if row["reviewer"] in members and _is_authenticated_review(row)
    }
    approvals = sum(row["decision"] == "approve" for row in review_by_member.values())
    rejections = sum(row["decision"] == "reject" for row in review_by_member.values())
    pending = max(0, len(members) - len(review_by_member))

    continuity_rows = connection.execute(
        """
        SELECT reviewer, verdict, reason, issues_json, authenticated_actor, auth_kind, updated_at
        FROM canon_continuity_checks
        WHERE candidate_id = ? AND revision_sha256 = ?
        """,
        (candidate.id, revision),
    ).fetchall()
    current_continuity = [
        row
        for row in continuity_rows
        if row["reviewer"] in candidate.continuity_reviewers and _is_authenticated_review(row)
    ]
    continuity_veto = any(row["verdict"] == "veto" for row in current_continuity)
    continuity_passed = bool(current_continuity) and not continuity_veto and any(
        row["verdict"] == "pass" for row in current_continuity
    )
    continuity_status = "vetoed" if continuity_veto else "passed" if continuity_passed else "pending"
    stale_reviews = connection.execute(
        "SELECT COUNT(*) FROM canon_committee_reviews WHERE candidate_id = ? AND revision_sha256 != ?",
        (candidate.id, revision),
    ).fetchone()[0]
    stale_continuity = connection.execute(
        "SELECT COUNT(*) FROM canon_continuity_checks WHERE candidate_id = ? AND revision_sha256 != ?",
        (candidate.id, revision),
    ).fetchone()[0]

    promotion_row = connection.execute(
        """
        SELECT revision_sha256, output_path, output_sha256, promoted_at
        FROM canon_governance_promotions
        WHERE candidate_id = ? AND revision_sha256 = ?
        ORDER BY promoted_at DESC LIMIT 1
        """,
        (candidate.id, revision),
    ).fetchone()
    promotion_history_count = int(
        connection.execute(
            "SELECT COUNT(*) FROM canon_governance_promotions WHERE candidate_id = ?",
            (candidate.id,),
        ).fetchone()[0]
    )
    promotion_integrity = "none"
    promotion_is_current = False
    if promotion_row:
        output_path = _inside(base_root, promotion_row["output_path"])
        expected_output_sha = str(promotion_row["output_sha256"] or "")
        if not output_path.is_file():
            promotion_integrity = "missing"
        elif not _is_sha256(expected_output_sha):
            promotion_integrity = "unverified"
        else:
            actual_output_sha = hashlib.sha256(output_path.read_bytes()).hexdigest()
            if hmac.compare_digest(actual_output_sha, expected_output_sha):
                promotion_integrity = "valid"
                promotion_is_current = True
            else:
                promotion_integrity = "mismatch"
    blockers: list[str] = []
    if promotion_is_current:
        blockers.append("already_promoted")
    elif promotion_row:
        blockers.append("promotion_output_integrity")
    elif promotion_history_count:
        blockers.append("promoted_revision_changed")
    if continuity_veto:
        blockers.append("continuity_veto")
    elif not continuity_passed:
        blockers.append("continuity_pending")
    if approvals < candidate.required_approvals:
        blockers.append("committee_quorum")
    can_promote = not blockers
    if promotion_is_current:
        gate_state = "promoted"
    elif promotion_row:
        gate_state = "blocked"
    elif promotion_history_count:
        gate_state = "blocked"
    elif continuity_veto:
        gate_state = "blocked"
    elif can_promote:
        gate_state = "ready"
    elif continuity_passed:
        gate_state = "committee_review"
    else:
        gate_state = "continuity_review"

    committee: dict[str, Any] = {
        "group_id": candidate.reviewer_group,
        "size": len(members),
        "threshold": candidate.required_approvals,
        "approvals": approvals,
        "rejections": rejections,
        "pending": pending,
        "status": "approved" if approvals >= candidate.required_approvals else "in_review" if review_by_member else "pending",
        "stale_reviews": int(stale_reviews),
    }
    continuity: dict[str, Any] = {
        "status": continuity_status,
        "hard_veto": continuity_veto,
        "stale_checks": int(stale_continuity),
    }
    if include_private:
        committee["members"] = [
            {
                "id": member,
                "decision": review_by_member[member]["decision"] if member in review_by_member else None,
                "reason": review_by_member[member]["reason"] if member in review_by_member else "",
                "auth_kind": review_by_member[member]["auth_kind"] if member in review_by_member else None,
                "updated_at": review_by_member[member]["updated_at"] if member in review_by_member else None,
            }
            for member in members
        ]
        continuity["reviewers"] = [
            {
                "id": reviewer,
                "verdict": next((row["verdict"] for row in current_continuity if row["reviewer"] == reviewer), None),
                "reason": next((row["reason"] for row in current_continuity if row["reviewer"] == reviewer), ""),
                "issues": next((json.loads(row["issues_json"]) for row in current_continuity if row["reviewer"] == reviewer), []),
            }
            for reviewer in candidate.continuity_reviewers
        ]

    return {
        "schema_version": 1,
        "candidate": {
            "id": candidate.id,
            "version": candidate.version,
            "mode": candidate.mode,
            "title": candidate.title,
            "work": candidate.work,
            "public_href": candidate.public_href,
            "revision_sha256": revision,
            "status": gate_state,
        },
        "resonance": {
            **resonance,
            "support": total_support,
            "revise": total_revise,
            "total": total_votes,
            "support_ratio": round(total_support / total_votes, 4) if total_votes else 0,
            "viewer_choice": viewer_choice,
            "advisory_only": True,
            "open": candidate.resonance_enabled,
        },
        "continuity": continuity,
        "committee": committee,
        "promotion_gate": {
            "state": gate_state,
            "can_promote": can_promote,
            "blockers": blockers,
        },
        "promotion": {
            "promoted": promotion_is_current,
            "recorded": bool(promotion_row),
            "integrity": promotion_integrity,
            "revision_sha256": promotion_row["revision_sha256"] if promotion_row else None,
            "output_path": promotion_row["output_path"] if promotion_row else None,
            "promoted_at": promotion_row["promoted_at"] if promotion_row else None,
            "history_count": promotion_history_count,
        },
    }


def _committee_members(candidate: PublicCanonCandidate, root: Path | None) -> list[str]:
    try:
        group = get_reviewer_group(candidate.reviewer_group, root=root or get_settings().root)
    except ReviewerError as exc:
        raise GovernanceError(str(exc)) from exc
    members = [member.strip() for member in group.members if member.strip()]
    if not members:
        raise GovernanceError(f"reviewer group has no members: {candidate.reviewer_group}")
    return members


def _revision_sha256(
    candidate: PublicCanonCandidate,
    members: list[str],
    root: Path | None,
) -> str:
    base = root or get_settings().root
    source = _inside(base, candidate.source_path)
    if not source.is_file():
        raise GovernanceError(f"candidate source not found: {candidate.source_path}")
    return _revision_sha256_from_bytes(candidate, members, source.read_bytes())


def _revision_sha256_from_bytes(
    candidate: PublicCanonCandidate,
    members: list[str],
    content: bytes,
) -> str:
    policy = {
        **candidate.model_dump(mode="json"),
        "committee_members": members,
        "governance_schema": 1,
    }
    policy_bytes = json.dumps(
        policy,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(policy_bytes + b"\x00" + content).hexdigest()


def _require_expected_revision(current: str, expected: str) -> None:
    clean_expected = (expected or "").strip().lower()
    if not _is_sha256(clean_expected) or not hmac.compare_digest(current, clean_expected):
        raise GovernanceError("candidate revision changed; refresh before reviewing")


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(character in "0123456789abcdef" for character in value)


def _registry_path(root: Path | None) -> Path:
    base = root or get_settings().root
    configured = get_settings().governance_registry_path
    return configured if configured.is_absolute() else base / configured


def _database_path(root: Path | None) -> Path:
    base = root or get_settings().root
    configured = get_settings().database_path
    return configured if configured.is_absolute() else base / configured


def _connect(root: Path | None) -> sqlite3.Connection:
    path = _database_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode = WAL")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS canon_resonance_votes (
            candidate_id TEXT NOT NULL,
            voter_key TEXT NOT NULL,
            identity_kind TEXT NOT NULL CHECK(identity_kind IN ('registered', 'anonymous')),
            choice TEXT NOT NULL CHECK(choice IN ('support', 'revise')),
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY(candidate_id, voter_key)
        );
        CREATE TABLE IF NOT EXISTS canon_committee_reviews (
            candidate_id TEXT NOT NULL,
            revision_sha256 TEXT NOT NULL,
            reviewer TEXT NOT NULL,
            authenticated_actor TEXT NOT NULL DEFAULT '',
            auth_kind TEXT NOT NULL DEFAULT '',
            decision TEXT NOT NULL CHECK(decision IN ('approve', 'reject')),
            reason TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY(candidate_id, revision_sha256, reviewer)
        );
        CREATE TABLE IF NOT EXISTS canon_continuity_checks (
            candidate_id TEXT NOT NULL,
            revision_sha256 TEXT NOT NULL,
            reviewer TEXT NOT NULL,
            authenticated_actor TEXT NOT NULL DEFAULT '',
            auth_kind TEXT NOT NULL DEFAULT '',
            verdict TEXT NOT NULL CHECK(verdict IN ('pass', 'veto')),
            reason TEXT NOT NULL DEFAULT '',
            issues_json TEXT NOT NULL DEFAULT '[]',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            PRIMARY KEY(candidate_id, revision_sha256, reviewer)
        );
        CREATE TABLE IF NOT EXISTS canon_governance_promotions (
            candidate_id TEXT NOT NULL,
            revision_sha256 TEXT NOT NULL,
            output_path TEXT NOT NULL,
            output_sha256 TEXT NOT NULL DEFAULT '',
            promoted_at TEXT NOT NULL,
            PRIMARY KEY(candidate_id, revision_sha256)
        );
        CREATE TABLE IF NOT EXISTS canon_governance_events (
            event_id TEXT PRIMARY KEY,
            event_type TEXT NOT NULL,
            candidate_id TEXT NOT NULL,
            revision_sha256 TEXT,
            actor_key TEXT NOT NULL,
            action TEXT NOT NULL,
            decision TEXT,
            reason TEXT NOT NULL DEFAULT '',
            metadata_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_governance_events_candidate
            ON canon_governance_events(candidate_id, created_at);
        """
    )
    _ensure_column(
        connection,
        "canon_governance_promotions",
        "output_sha256",
        "TEXT NOT NULL DEFAULT ''",
    )
    _ensure_column(
        connection,
        "canon_committee_reviews",
        "authenticated_actor",
        "TEXT NOT NULL DEFAULT ''",
    )
    _ensure_column(
        connection,
        "canon_committee_reviews",
        "auth_kind",
        "TEXT NOT NULL DEFAULT ''",
    )
    _ensure_column(
        connection,
        "canon_continuity_checks",
        "authenticated_actor",
        "TEXT NOT NULL DEFAULT ''",
    )
    _ensure_column(
        connection,
        "canon_continuity_checks",
        "auth_kind",
        "TEXT NOT NULL DEFAULT ''",
    )
    _invalidate_legacy_or_duplicate_actors(connection, "canon_committee_reviews")
    _invalidate_legacy_or_duplicate_actors(connection, "canon_continuity_checks")
    connection.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_committee_one_actor_per_revision
        ON canon_committee_reviews(candidate_id, revision_sha256, authenticated_actor)
        WHERE authenticated_actor != ''
        """
    )
    connection.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_continuity_one_actor_per_revision
        ON canon_continuity_checks(candidate_id, revision_sha256, authenticated_actor)
        WHERE authenticated_actor != ''
        """
    )
    connection.commit()
    return connection


def _is_authenticated_review(row: sqlite3.Row) -> bool:
    actor = str(row["authenticated_actor"] or "").strip()
    auth_kind = str(row["auth_kind"] or "").strip()
    return bool(actor and auth_kind and not auth_kind.startswith("invalidated_"))


def _invalidate_legacy_or_duplicate_actors(
    connection: sqlite3.Connection,
    table: str,
) -> None:
    connection.execute(
        f"""
        UPDATE {table}
        SET authenticated_actor = '', auth_kind = 'invalidated_legacy_identity'
        WHERE auth_kind = ''
           OR (authenticated_actor = '' AND auth_kind NOT LIKE 'invalidated_%')
        """
    )
    duplicates = connection.execute(
        f"""
        SELECT candidate_id, revision_sha256, authenticated_actor
        FROM {table}
        WHERE authenticated_actor != ''
        GROUP BY candidate_id, revision_sha256, authenticated_actor
        HAVING COUNT(*) > 1
        """
    ).fetchall()
    for row in duplicates:
        connection.execute(
            f"""
            UPDATE {table}
            SET authenticated_actor = '', auth_kind = 'invalidated_duplicate_actor'
            WHERE candidate_id = ? AND revision_sha256 = ? AND authenticated_actor = ?
            """,
            (row["candidate_id"], row["revision_sha256"], row["authenticated_actor"]),
        )


def _ensure_column(
    connection: sqlite3.Connection,
    table: str,
    column: str,
    definition: str,
) -> None:
    columns = {row[1] for row in connection.execute(f"PRAGMA table_info({table})")}
    if column not in columns:
        connection.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def _record_event(
    connection: sqlite3.Connection,
    *,
    event_type: str,
    candidate_id: str,
    revision_sha256: str | None,
    actor_key: str,
    action: str,
    decision: str | None,
    reason: str,
    metadata: dict[str, Any],
) -> None:
    connection.execute(
        """
        INSERT INTO canon_governance_events
            (event_id, event_type, candidate_id, revision_sha256, actor_key, action,
             decision, reason, metadata_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            str(uuid4()),
            event_type,
            candidate_id,
            revision_sha256,
            actor_key,
            action,
            decision,
            reason.strip(),
            json.dumps(metadata, ensure_ascii=False, sort_keys=True),
            _now(),
        ),
    )


def _inside(base: Path, relative: str) -> Path:
    root = base.resolve()
    candidate = (root / relative).resolve()
    if candidate == root or root not in candidate.parents:
        raise GovernanceError(f"path escapes ECHO root: {relative}")
    return candidate


def _atomic_write_bytes(target: Path, content: bytes) -> None:
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=target.parent,
            prefix=f".{target.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _clean_id(value: str) -> str:
    clean = (value or "").strip().lower()
    if not clean or any(character not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for character in clean):
        raise GovernanceError("invalid candidate id")
    return clean


def _clean_reviewer(value: str) -> str:
    clean = (value or "").strip()
    if not clean:
        raise GovernanceError("reviewer is required")
    return clean


def _now() -> str:
    return datetime.now(UTC).isoformat()
