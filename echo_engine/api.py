from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import yaml

from echo_engine.bindings import (
    BindingError,
    bind_user_to_character,
    get_user_binding,
    list_user_bindings,
    release_user_binding,
)
from echo_engine.economy import (
    EconomyError,
    activate_ghost_subscription,
    economy_account_summary,
    list_products,
    purchase_product,
    record_wallet_entry,
)
from echo_engine.generators import (
    run_art_director_agent,
    run_character_agent,
    run_consistency_agent,
    run_faction_agent,
    run_lore_agent,
    run_relationship_agent,
    run_story_agent,
    run_technology_agent,
)
from echo_engine.identities import (
    IdentityError,
    assign_identity,
    check_npc_access,
    check_realm_event_access,
    get_universe_identity,
    list_identity_tiers,
)
from echo_engine.neural.simulator import UniverseEvent, simulate_event
from echo_engine.neural.digital_life import run_daily_life_tick
from echo_engine.neural.octopus_ecosystem import render_octopus_ecosystem_plan
from echo_engine.neural.octopus_export import configured_octopus_agents_root, sync_octopus_runtime_agents
from echo_engine.neural.octopus_runtime import (
    configured_octopus_runtime_url,
    reload_octopus_runtime_agents,
)
from echo_engine.npcs import NPCError, get_npc, list_npcs, route_npc_interaction
from echo_engine.journal import CanonDecision, candidate_queue, journal, record_canon_decision
from echo_engine.promotion import PromotionError, promote_candidate
from echo_engine.realm_events import RealmEventError, realm_event_queue, submit_realm_event
from echo_engine.realms import RealmError, get_realm, list_realms, route_realm_review
from echo_engine.reviewers import (
    ReviewerError,
    authorize_reviewer_for_event,
    get_reviewer_group,
    list_reviewer_groups,
)
from echo_engine.skins import SkinError, check_skin_access, list_skin_policies
from echo_engine.store import CanonStore
from echo_engine.universe_feed import UniverseFeedError, get_universe_feed_for_user

app = FastAPI(title="ECHO Universe Engine", version="0.1.0")
console_dir = Path("console")
if console_dir.exists():
    app.mount("/console", StaticFiles(directory=console_dir), name="console")
assets_dir = Path("assets")
if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
for static_name in ["outputs", "stories", "characters", "relationships", "bible", "factions", "technologies"]:
    static_dir = Path(static_name)
    if static_dir.exists():
        app.mount(f"/{static_name}", StaticFiles(directory=static_dir), name=static_name)


class EventRunRequest(BaseModel):
    title: str = "Ghost Attack on Atlas"
    location: str = "Atlas"
    description: str = (
        "A Ghost contamination wave hits Atlas civic identity gates, causing citizens "
        "to remember lives from dead household AI cores."
    )
    pressure: str = "identity / Ghost personhood"
    stakes: str = "Atlas stability and White Ghost Team trust"


class CanonDecisionRequest(BaseModel):
    event_id: str
    decision: CanonDecision
    reason: str
    reviewer: str = "human"


class PromoteCandidateRequest(BaseModel):
    event_id: str
    target_dir: str | None = None
    filename: str | None = None
    refresh_octopus_agents: bool = True


class OctopusSyncRequest(BaseModel):
    output_dir: str | None = None
    reload_runtime: bool = False


class BindCharacterRequest(BaseModel):
    user_id: str
    character_id: str
    source: str = "mobile"


class RealmReviewRouteRequest(BaseModel):
    scope: str = "personal"
    realm_id: str | None = None


class RealmEventRequest(BaseModel):
    title: str
    summary: str
    scope: str = "personal"
    realm_id: str | None = None
    submitter: str = "anonymous"
    content: str = ""
    canon_risks: list[str] = []
    metadata: dict[str, object] = {}


class ReviewerAuthorizationRequest(BaseModel):
    reviewer: str
    event_id: str


class WalletGrantRequest(BaseModel):
    user_id: str
    amount: int
    reason: str = "manual_grant"
    ref_id: str | None = None
    metadata: dict[str, object] = {}


class ProductPurchaseRequest(BaseModel):
    user_id: str
    product_id: str
    character_id: str | None = None


class GhostSubscriptionRequest(BaseModel):
    user_id: str
    character_id: str | None = None
    duration_days: int = 30
    source: str = "manual"
    metadata: dict[str, object] = {}


class NPCInteractionRouteRequest(BaseModel):
    action: str = "chat"


class IdentityAssignmentRequest(BaseModel):
    user_id: str
    tier: str
    realms: list[str] = []
    source: str = "manual"
    metadata: dict[str, object] = {}


class RealmAccessCheckRequest(BaseModel):
    user_id: str
    scope: str = "personal"
    realm_id: str | None = None


class NPCAccessCheckRequest(BaseModel):
    user_id: str
    npc_id: str
    action: str = "chat"


class SkinAccessCheckRequest(BaseModel):
    user_id: str
    skin_type: str = "local_skin"
    requested_scope: str = "personal"
    realm_id: str | None = None
    claims: list[str] = []


@app.get("/api/health")
def health() -> dict[str, object]:
    status = CanonStore().status()
    return {
        "status": "ok",
        "service": "echo-universe-engine",
        "canon": status.model_dump(),
    }


@app.get("/api/canon/status")
def canon_status():
    return CanonStore().status()


@app.get("/api/canon/characters")
def canon_characters():
    return CanonStore().load_character_cards()


@app.get("/api/journal/events")
def journal_events(limit: int = 50):
    safe_limit = max(0, min(limit, 500))
    return [event.model_dump(mode="json") for event in journal().read_all(limit=safe_limit)]


@app.get("/api/journal/candidates")
def journal_candidates(limit: int = 50):
    safe_limit = max(0, min(limit, 500))
    return candidate_queue(limit=safe_limit)


@app.post("/api/journal/decisions")
def journal_decision(body: CanonDecisionRequest):
    try:
        return record_canon_decision(
            event_id=body.event_id,
            decision=body.decision,
            reason=body.reason,
            reviewer=body.reviewer,
        )
    except ReviewerError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.post("/api/canon/promotions")
def canon_promotion(body: PromoteCandidateRequest):
    try:
        result = promote_candidate(
            body.event_id,
            target_dir=body.target_dir,
            filename=body.filename,
            refresh_octopus_agents=body.refresh_octopus_agents,
        )
    except PromotionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"ok": True, **result.__dict__}


@app.get("/api/bindings")
def user_bindings():
    return [binding.model_dump(mode="json") for binding in list_user_bindings()]


@app.get("/api/bindings/{user_id}")
def user_binding(user_id: str):
    binding = get_user_binding(user_id)
    if binding is None:
        raise HTTPException(status_code=404, detail=f"user binding not found: {user_id}")
    return binding


@app.post("/api/bindings")
def bind_character(body: BindCharacterRequest):
    try:
        return bind_user_to_character(
            user_id=body.user_id,
            character_id=body.character_id,
            source=body.source,
        )
    except BindingError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.delete("/api/bindings/{user_id}")
def release_binding(user_id: str):
    try:
        return release_user_binding(user_id)
    except BindingError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/universe/feed/{user_id}")
def universe_feed(user_id: str):
    try:
        return get_universe_feed_for_user(user_id)
    except UniverseFeedError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/identity/tiers")
def identity_tiers():
    try:
        return [tier.model_dump(mode="json") for tier in list_identity_tiers()]
    except IdentityError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/identity/users/{user_id}")
def identity_user(user_id: str):
    try:
        return get_universe_identity(user_id)
    except IdentityError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/identity/assignments")
def identity_assignment(body: IdentityAssignmentRequest):
    try:
        return assign_identity(
            user_id=body.user_id,
            tier=body.tier,
            realms=body.realms,
            source=body.source,
            metadata=dict(body.metadata),
        )
    except IdentityError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/identity/check-realm")
def identity_check_realm(body: RealmAccessCheckRequest):
    try:
        return check_realm_event_access(
            user_id=body.user_id,
            scope=body.scope,
            realm_id=body.realm_id,
        )
    except IdentityError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/identity/check-npc")
def identity_check_npc(body: NPCAccessCheckRequest):
    try:
        return check_npc_access(user_id=body.user_id, npc_id=body.npc_id, action=body.action)
    except IdentityError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/skins/policies")
def skin_policies():
    try:
        return [policy.model_dump(mode="json") for policy in list_skin_policies()]
    except SkinError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/skins/check")
def skin_check(body: SkinAccessCheckRequest):
    try:
        return check_skin_access(
            user_id=body.user_id,
            skin_type=body.skin_type,
            requested_scope=body.requested_scope,
            realm_id=body.realm_id,
            claims=body.claims,
        )
    except SkinError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/npcs")
def npcs(realm_id: str | None = None, npc_type: str | None = None, bindable: bool | None = None):
    try:
        return [
            npc.model_dump(mode="json")
            for npc in list_npcs(realm_id=realm_id, npc_type=npc_type, bindable=bindable)
        ]
    except NPCError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/npcs/{npc_id}")
def npc(npc_id: str):
    try:
        return get_npc(npc_id)
    except NPCError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/npcs/{npc_id}/route")
def npc_interaction_route(npc_id: str, body: NPCInteractionRouteRequest):
    try:
        return route_npc_interaction(npc_id=npc_id, action=body.action)
    except NPCError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/realms")
def realms():
    try:
        return [realm.model_dump(mode="json") for realm in list_realms()]
    except RealmError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/realms/{realm_id}")
def realm(realm_id: str):
    try:
        return get_realm(realm_id)
    except RealmError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/realms/review-route")
def realm_review_route(body: RealmReviewRouteRequest):
    try:
        return route_realm_review(scope=body.scope, realm_id=body.realm_id)
    except RealmError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/realm-events")
def realm_events(reviewer_group: str | None = None, realm_id: str | None = None, limit: int = 50):
    safe_limit = max(0, min(limit, 500))
    return [
        event.model_dump(mode="json")
        for event in realm_event_queue(
            reviewer_group=reviewer_group,
            realm_id=realm_id,
            limit=safe_limit,
        )
    ]


@app.post("/api/realm-events")
def realm_event_submit(body: RealmEventRequest):
    try:
        return submit_realm_event(
            title=body.title,
            summary=body.summary,
            scope=body.scope,
            realm_id=body.realm_id,
            submitter=body.submitter,
            content=body.content,
            canon_risks=body.canon_risks,
            metadata=dict(body.metadata),
        )
    except RealmEventError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/reviewers/groups")
def reviewer_groups():
    try:
        return [group.model_dump(mode="json") for group in list_reviewer_groups()]
    except ReviewerError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/reviewers/groups/{group_id}")
def reviewer_group(group_id: str):
    try:
        return get_reviewer_group(group_id)
    except ReviewerError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/reviewers/authorize")
def reviewer_authorize(body: ReviewerAuthorizationRequest):
    events = [event for event in journal().read_all() if str(event.event_id) == body.event_id]
    if not events:
        raise HTTPException(status_code=404, detail=f"event not found: {body.event_id}")
    try:
        return authorize_reviewer_for_event(reviewer=body.reviewer, event=events[-1])
    except ReviewerError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/economy/products")
def economy_products():
    try:
        return [product.model_dump(mode="json") for product in list_products()]
    except EconomyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/economy/users/{user_id}/summary")
def economy_summary(user_id: str):
    try:
        return economy_account_summary(user_id)
    except EconomyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/economy/wallet/grant")
def economy_wallet_grant(body: WalletGrantRequest):
    try:
        return record_wallet_entry(
            user_id=body.user_id,
            amount=body.amount,
            reason=body.reason,
            ref_id=body.ref_id,
            metadata=dict(body.metadata),
        )
    except EconomyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/economy/purchases")
def economy_purchase(body: ProductPurchaseRequest):
    try:
        return purchase_product(
            user_id=body.user_id,
            product_id=body.product_id,
            character_id=body.character_id,
        )
    except EconomyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/economy/subscriptions/ghost")
def economy_ghost_subscription(body: GhostSubscriptionRequest):
    try:
        return activate_ghost_subscription(
            user_id=body.user_id,
            character_id=body.character_id,
            duration_days=body.duration_days,
            source=body.source,
            metadata=dict(body.metadata),
        )
    except EconomyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/assets/characters")
def character_visual_assets() -> dict[str, object]:
    index_path = Path("assets/characters/octopus_visual_asset_index.yaml")
    if not index_path.exists():
        return {"schema": "echo_octopus_visual_asset_index_v1", "characters": {}}
    data = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    for character in data.get("characters", {}).values():
        files = character.get("files", {})
        character["urls"] = {
            key: f"/{path}" for key, path in files.items() if path.endswith((".png", ".jpg", ".jpeg", ".webp"))
        }
    return data


@app.post("/api/agents/character/run")
def character_run():
    return run_character_agent()


@app.post("/api/agents/lore/run")
def lore_run():
    return run_lore_agent()


@app.post("/api/agents/story/run")
def story_run():
    return run_story_agent()


@app.post("/api/agents/relationship/run")
def relationship_run():
    return run_relationship_agent()


@app.post("/api/agents/faction/run")
def faction_run():
    return run_faction_agent()


@app.post("/api/agents/technology/run")
def technology_run():
    return run_technology_agent()


@app.post("/api/agents/art-director/run")
def art_director_run():
    return run_art_director_agent()


@app.post("/api/agents/consistency/run")
def consistency_run():
    return run_consistency_agent()


@app.post("/api/neural/event/run")
def neural_event_run(body: EventRunRequest):
    return simulate_event(UniverseEvent(**body.model_dump()))


@app.post("/api/neural/daily-life/run")
def neural_daily_life_run():
    return run_daily_life_tick()


@app.get("/api/integrations/octopus/plan")
def octopus_integration_plan() -> dict[str, str]:
    return {"content": render_octopus_ecosystem_plan()}


@app.get("/api/integrations/octopus/status")
def octopus_integration_status() -> dict[str, object]:
    root = configured_octopus_agents_root()
    runtime_url = configured_octopus_runtime_url()
    return {
        "agents_root": str(root) if root else None,
        "configured": root is not None,
        "exists": root.exists() if root else False,
        "runtime_url": runtime_url,
        "runtime_configured": runtime_url is not None,
    }


@app.post("/api/integrations/octopus/sync-agents")
def octopus_sync_agents(body: OctopusSyncRequest):
    try:
        written = sync_octopus_runtime_agents(
            output_dir=Path(body.output_dir) if body.output_dir else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    reload_result = reload_octopus_runtime_agents() if body.reload_runtime else None
    return {
        "ok": True,
        "written": [str(path) for path in written],
        "reload": reload_result.__dict__ if reload_result else None,
    }


@app.get("/")
def console_index():
    index = console_dir / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"service": "echo-universe-engine", "console": "not installed"}
