from __future__ import annotations

from pathlib import Path

import yaml

from echo_engine.bindings import agent_id_for_character
from echo_engine.models import NPCInteractionRoute, NPCProfile
from echo_engine.realms import RealmError, get_realm, route_realm_review
from echo_engine.store import CanonStore


NPCS_PATH = Path("data/npcs.yaml")


class NPCError(ValueError):
    pass


def list_npcs(
    *,
    realm_id: str | None = None,
    npc_type: str | None = None,
    bindable: bool | None = None,
    root: Path | None = None,
) -> list[NPCProfile]:
    npcs = sorted(_load_npcs(root).values(), key=lambda item: (item.realm_id, item.npc_type, item.id))
    if realm_id:
        npcs = [npc for npc in npcs if npc.realm_id == realm_id]
    if npc_type:
        clean_type = npc_type.strip().lower()
        npcs = [npc for npc in npcs if npc.npc_type == clean_type]
    if bindable is not None:
        npcs = [npc for npc in npcs if npc.bindable is bindable]
    return npcs


def get_npc(npc_id: str, root: Path | None = None) -> NPCProfile:
    clean_id = _clean_required(npc_id, "npc_id")
    npc = _load_npcs(root).get(clean_id)
    if npc is None:
        raise NPCError(f"npc not found: {clean_id}")
    return npc


def route_npc_interaction(
    *,
    npc_id: str,
    action: str,
    root: Path | None = None,
) -> NPCInteractionRoute:
    npc = get_npc(npc_id, root)
    clean_action = _clean_required(action, "action")
    if npc.allowed_actions and clean_action not in npc.allowed_actions:
        raise NPCError(f"action '{clean_action}' is not allowed for npc: {npc.id}")
    try:
        route = route_realm_review(scope=npc.review_scope, realm_id=npc.realm_id, root=root)
    except RealmError as exc:
        raise NPCError(str(exc)) from exc
    reviewer_group = npc.reviewer_group or route.reviewer_group
    return NPCInteractionRoute(
        npc_id=npc.id,
        npc_name=npc.name,
        npc_type=npc.npc_type,
        action=clean_action,
        realm_id=route.resolved_realm_id,
        review_scope=route.requested_scope,
        reviewer_group=reviewer_group,
        approval=route.approval,
        canon_risk=npc.canon_risk,
        relationship_policy=npc.relationship_policy,
        requires_entitlement=npc.unlock_entitlement,
        escalation_path=route.escalation_path,
    )


def _load_npcs(root: Path | None = None) -> dict[str, NPCProfile]:
    path = _npcs_path(root)
    if not path.exists():
        raise NPCError(f"npc catalog not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    raw_npcs = data.get("npcs", {})
    if not isinstance(raw_npcs, dict):
        raise NPCError("npc catalog must contain a 'npcs' mapping")
    character_index = {card.id: card for card in CanonStore(root).load_character_cards()}
    npcs: dict[str, NPCProfile] = {}
    for npc_id, raw in raw_npcs.items():
        if not isinstance(raw, dict):
            continue
        payload = {"id": npc_id, **raw}
        character_id = payload.get("character_id")
        if isinstance(character_id, str) and character_id in character_index:
            card = character_index[character_id]
            payload.setdefault("name", card.name)
            payload.setdefault("codename", card.codename)
            payload.setdefault("faction", card.faction)
            payload.setdefault("agent_id", agent_id_for_character(card))
        npc = NPCProfile.model_validate(payload)
        _validate_npc(npc, root)
        npcs[npc.id] = npc
    return npcs


def _validate_npc(npc: NPCProfile, root: Path | None = None) -> None:
    try:
        get_realm(npc.realm_id, root)
    except RealmError as exc:
        raise NPCError(f"npc {npc.id} references invalid realm: {npc.realm_id}") from exc
    if npc.npc_type not in {"anchor", "realm", "utility", "creator"}:
        raise NPCError(f"npc {npc.id} has unsupported npc_type: {npc.npc_type}")
    if npc.canon_risk not in {"low", "medium", "high"}:
        raise NPCError(f"npc {npc.id} has unsupported canon_risk: {npc.canon_risk}")


def _npcs_path(root: Path | None = None) -> Path:
    base = root or Path.cwd()
    return base / NPCS_PATH


def _clean_required(value: str, field_name: str) -> str:
    clean = str(value or "").strip()
    if not clean:
        raise NPCError(f"{field_name} is required")
    return clean
