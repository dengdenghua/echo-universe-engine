from __future__ import annotations

from pathlib import Path

import yaml

from echo_engine.models import Realm, RealmReviewRoute


REALMS_PATH = Path("data/realms.yaml")
SCOPE_FALLBACK_REALM = {
    "personal": "personal_instance",
    "instance": "personal_instance",
    "arc": "ghost_court",
    "city": "atlas",
    "nation": "earth",
    "planet": "earth",
    "main": "main",
}
SCOPE_APPROVAL = {
    "personal": "auto_or_light_review",
    "instance": "instance_reviewer_required",
    "arc": "arc_reviewer_required",
    "city": "city_reviewer_required",
    "nation": "nation_board_required",
    "planet": "planet_board_required",
    "main": "world_brain_required",
}


class RealmError(ValueError):
    pass


def list_realms(root: Path | None = None) -> list[Realm]:
    return sorted(_load_realms(root).values(), key=lambda item: (item.canon_tier, item.id))


def get_realm(realm_id: str, root: Path | None = None) -> Realm:
    clean_id = _clean_required(realm_id, "realm_id")
    realms = _load_realms(root)
    realm = realms.get(clean_id)
    if realm is None:
        raise RealmError(f"realm not found: {clean_id}")
    return realm


def route_realm_review(
    *,
    scope: str,
    realm_id: str | None = None,
    root: Path | None = None,
) -> RealmReviewRoute:
    clean_scope = (scope or "").strip().lower()
    if clean_scope not in SCOPE_FALLBACK_REALM:
        raise RealmError(f"unsupported review scope: {scope}")
    realms = _load_realms(root)
    requested_realm_id = realm_id.strip() if isinstance(realm_id, str) and realm_id.strip() else None
    resolved_id = requested_realm_id or SCOPE_FALLBACK_REALM[clean_scope]
    realm = realms.get(resolved_id)
    if realm is None:
        raise RealmError(f"realm not found: {resolved_id}")
    return RealmReviewRoute(
        requested_scope=clean_scope,
        requested_realm_id=requested_realm_id,
        resolved_realm_id=realm.id,
        resolved_realm_name=realm.name,
        canon_tier=realm.canon_tier,
        approval=SCOPE_APPROVAL.get(clean_scope, realm.default_approval),
        reviewer_group=realm.reviewer_group,
        escalation_path=_escalation_path(realm, realms),
    )


def _load_realms(root: Path | None = None) -> dict[str, Realm]:
    path = _realms_path(root)
    if not path.exists():
        raise RealmError(f"realms file not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    raw_realms = data.get("realms", {})
    if not isinstance(raw_realms, dict):
        raise RealmError("realms file must contain a 'realms' mapping")
    realms = {realm_id: Realm.model_validate(raw) for realm_id, raw in raw_realms.items()}
    _validate_parent_links(realms)
    return realms


def _validate_parent_links(realms: dict[str, Realm]) -> None:
    for realm in realms.values():
        if realm.parent_id and realm.parent_id not in realms:
            raise RealmError(f"realm {realm.id} references missing parent {realm.parent_id}")


def _escalation_path(realm: Realm, realms: dict[str, Realm]) -> list[str]:
    path = [realm.id]
    seen = {realm.id}
    parent_id = realm.parent_id
    while parent_id:
        if parent_id in seen:
            raise RealmError(f"realm parent cycle detected at {parent_id}")
        parent = realms.get(parent_id)
        if parent is None:
            break
        path.append(parent.id)
        seen.add(parent.id)
        parent_id = parent.parent_id
    return path


def _realms_path(root: Path | None = None) -> Path:
    base = root or Path.cwd()
    return base / REALMS_PATH


def _clean_required(value: str, field: str) -> str:
    clean = (value or "").strip()
    if not clean:
        raise RealmError(f"{field} is required")
    return clean
