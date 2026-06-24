from __future__ import annotations

from pathlib import Path

import yaml

from echo_engine.identities import get_universe_identity
from echo_engine.models import SkinAccessDecision, SkinPolicy
from echo_engine.realms import RealmError, route_realm_review


SKIN_POLICY_PATH = Path("data/skin_policy.yaml")


class SkinError(ValueError):
    pass


def list_skin_policies(root: Path | None = None) -> list[SkinPolicy]:
    return sorted(_load_skin_policies(root).values(), key=lambda item: item.id)


def get_skin_policy(skin_type: str, root: Path | None = None) -> SkinPolicy:
    clean_type = _clean_required(skin_type, "skin_type")
    policy = _load_skin_policies(root).get(clean_type)
    if policy is None:
        raise SkinError(f"skin policy not found: {clean_type}")
    return policy


def check_skin_access(
    *,
    user_id: str,
    skin_type: str = "local_skin",
    requested_scope: str = "personal",
    realm_id: str | None = None,
    claims: list[str] | None = None,
    root: Path | None = None,
) -> SkinAccessDecision:
    identity = get_universe_identity(user_id, root)
    policy = get_skin_policy(skin_type, root)
    clean_scope = _clean_required(requested_scope, "requested_scope")
    resolved_realm_id = realm_id or policy.default_realm_id
    if policy.skin_type == "local_skin" and clean_scope != "personal":
        return _decision(
            identity_tier=identity.tier,
            user_id=user_id,
            policy=policy,
            allowed=False,
            reason="local skins are private projections and cannot enter shared Realm or main canon",
            requested_scope=clean_scope,
            resolved_scope="personal",
            realm_id="personal_instance",
            required_downgrade="realm_skin_or_uniform_skin",
            claims=claims or [],
            root=root,
        )
    if not _scope_allowed(clean_scope, policy.max_scope, root):
        return _decision(
            identity_tier=identity.tier,
            user_id=user_id,
            policy=policy,
            allowed=False,
            reason=f"{policy.skin_type} cannot be used at {clean_scope} scope",
            requested_scope=clean_scope,
            resolved_scope=policy.max_scope,
            realm_id=resolved_realm_id,
            required_downgrade=_downgrade_for_scope(clean_scope),
            claims=claims or [],
            root=root,
        )
    if policy.allowed_identity_tiers and identity.tier not in policy.allowed_identity_tiers:
        return _decision(
            identity_tier=identity.tier,
            user_id=user_id,
            policy=policy,
            allowed=False,
            reason=f"identity tier '{identity.tier}' cannot publish {policy.skin_type}",
            requested_scope=clean_scope,
            resolved_scope=clean_scope,
            realm_id=resolved_realm_id,
            required_downgrade="local_skin",
            claims=claims or [],
            root=root,
        )
    required_entitlement = _required_entitlement(policy, resolved_realm_id)
    if required_entitlement and required_entitlement not in identity.active_entitlements:
        return _decision(
            identity_tier=identity.tier,
            user_id=user_id,
            policy=policy,
            allowed=False,
            reason=f"missing entitlement: {required_entitlement}",
            requested_scope=clean_scope,
            resolved_scope=clean_scope,
            realm_id=resolved_realm_id,
            required_entitlement=required_entitlement,
            claims=claims or [],
            root=root,
        )
    blocked_claim = _first_blocked_claim(claims or [], policy.banned_claims)
    if blocked_claim:
        return _decision(
            identity_tier=identity.tier,
            user_id=user_id,
            policy=policy,
            allowed=False,
            reason=f"skin claim is not allowed at this layer: {blocked_claim}",
            requested_scope=clean_scope,
            resolved_scope=clean_scope,
            realm_id=resolved_realm_id,
            required_downgrade="remove_claim_or_submit_visual_review",
            claims=claims or [],
            root=root,
        )
    return _decision(
        identity_tier=identity.tier,
        user_id=user_id,
        policy=policy,
        allowed=True,
        reason="allowed by visual canon policy",
        requested_scope=clean_scope,
        resolved_scope=clean_scope,
        realm_id=resolved_realm_id,
        required_entitlement=required_entitlement,
        claims=claims or [],
        root=root,
    )


def _load_skin_policies(root: Path | None = None) -> dict[str, SkinPolicy]:
    path = _policy_path(root)
    if not path.exists():
        raise SkinError(f"skin policy not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    raw_types = data.get("skin_types", {})
    if not isinstance(raw_types, dict):
        raise SkinError("skin policy must contain a 'skin_types' mapping")
    return {
        skin_type: SkinPolicy.model_validate({"id": skin_type, **raw})
        for skin_type, raw in raw_types.items()
        if isinstance(raw, dict)
    }


def _decision(
    *,
    identity_tier: str,
    user_id: str,
    policy: SkinPolicy,
    allowed: bool,
    reason: str,
    requested_scope: str,
    resolved_scope: str,
    realm_id: str,
    claims: list[str],
    root: Path | None,
    required_entitlement: str | None = None,
    required_downgrade: str | None = None,
) -> SkinAccessDecision:
    try:
        route = route_realm_review(scope=resolved_scope, realm_id=realm_id, root=root)
        reviewer_group = policy.reviewer_group or route.reviewer_group
        approval = route.approval
        escalation_path = route.escalation_path
        resolved_realm_id = route.resolved_realm_id
    except RealmError:
        reviewer_group = policy.reviewer_group or "world_brain"
        approval = "visual_review_required"
        escalation_path = [realm_id]
        resolved_realm_id = realm_id
    return SkinAccessDecision(
        user_id=user_id,
        allowed=allowed,
        reason=reason,
        identity_tier=identity_tier,
        skin_type=policy.skin_type,
        requested_scope=requested_scope,
        resolved_scope=resolved_scope,
        realm_id=resolved_realm_id,
        reviewer_group=reviewer_group,
        approval=approval,
        requires_entitlement=required_entitlement,
        required_downgrade=required_downgrade,
        visual_constraints=policy.visual_constraints,
        banned_claims=policy.banned_claims,
        escalation_path=escalation_path,
    )


def _required_entitlement(policy: SkinPolicy, realm_id: str) -> str | None:
    if not policy.requires_entitlement:
        return None
    if policy.requires_entitlement == "realm_access":
        return f"realm_access:{realm_id}"
    return policy.requires_entitlement


def _first_blocked_claim(claims: list[str], banned_claims: list[str]) -> str | None:
    normalized = {claim.strip().lower() for claim in claims}
    for banned in banned_claims:
        if banned.strip().lower() in normalized:
            return banned
    return None


def _scope_allowed(requested_scope: str, max_scope: str, root: Path | None = None) -> bool:
    ranks = _scope_ranks(root)
    return ranks.get(requested_scope, 999) <= ranks.get(max_scope, -1)


def _scope_ranks(root: Path | None = None) -> dict[str, int]:
    path = Path(root or Path.cwd()) / "data/access_policy.yaml"
    if not path.exists():
        return {"personal": 0, "instance": 1, "arc": 2, "city": 3, "nation": 4, "planet": 5, "main": 6}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    raw = data.get("scope_rank", {})
    if not isinstance(raw, dict):
        return {"personal": 0, "instance": 1, "arc": 2, "city": 3, "nation": 4, "planet": 5, "main": 6}
    return {str(key): int(value) for key, value in raw.items()}


def _downgrade_for_scope(scope: str) -> str:
    if scope in {"main", "planet", "nation"}:
        return "realm_skin_or_canon_skin_review"
    if scope in {"city", "arc"}:
        return "realm_skin_or_uniform_skin"
    return "local_skin"


def _policy_path(root: Path | None = None) -> Path:
    base = root or Path.cwd()
    return base / SKIN_POLICY_PATH


def _clean_required(value: str, field_name: str) -> str:
    clean = str(value or "").strip()
    if not clean:
        raise SkinError(f"{field_name} is required")
    return clean
