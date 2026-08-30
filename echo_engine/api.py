from __future__ import annotations

import base64
import hashlib
import hmac
from pathlib import Path
import re
import secrets
from typing import Literal

from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import yaml

from echo_engine.config import get_settings
from echo_engine.auth import JWTError, decode_hs256
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
    fulfill_external_purchase,
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
from echo_engine.governance import (
    GovernanceError,
    get_governance_state,
    list_governance_states,
    promote_public_candidate,
    record_committee_vote,
    record_continuity_check,
    set_resonance,
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

# 前端 CSS/JS 均为数十 KB 的纯文本，未压缩传输浪费明显。放在应用层是为了
# 让直连 uvicorn（本地开发、容器健康检查）也能受益，不依赖前置 nginx。
app.add_middleware(GZipMiddleware, minimum_size=1024, compresslevel=6)

_PUBLIC_EXACT_PATHS = {
    "/",
    "/universe",
    "/docs",
    "/docs/oauth2-redirect",
    "/openapi.json",
    "/redoc",
    "/api/health",
    "/api/canon/status",
    "/api/canon/characters",
    "/api/journal/events",
    "/api/assets/characters",
    "/api/economy/products",
    "/api/identity/tiers",
    "/api/skins/policies",
    "/api/npcs",
    "/api/realms",
    "/developers",
}
_PUBLIC_PATH_PREFIXES = (
    "/home/",
    "/universe/",
    "/developers/",
    "/review/",
    "/assets/characters/",
    "/characters/",
    "/api/npcs/",
    "/api/realms/",
)

_USER_ROUTE_PATTERNS = (
    ("GET", re.compile(r"^/api/bindings/[^/]+$")),
    ("POST", re.compile(r"^/api/bindings$")),
    ("DELETE", re.compile(r"^/api/bindings/[^/]+$")),
    ("GET", re.compile(r"^/api/universe/feed/[^/]+$")),
    ("GET", re.compile(r"^/api/identity/users/[^/]+$")),
    ("GET", re.compile(r"^/api/economy/users/[^/]+/summary$")),
    ("POST", re.compile(r"^/api/identity/check-(realm|npc)$")),
    ("POST", re.compile(r"^/api/skins/check$")),
    ("POST", re.compile(r"^/api/realm-events$")),
    ("POST", re.compile(r"^/api/npcs/[^/]+/route$")),
    ("POST", re.compile(r"^/api/realms/review-route$")),
    (
        "POST",
        re.compile(
            r"^/api/canon/governance/candidates/[a-z0-9_-]+/(committee-votes|continuity-checks)$"
        ),
    ),
    ("GET", re.compile(r"^/api/canon/governance/candidates$")),
)

_PUBLIC_READ_PATTERNS = (
    re.compile(r"^/api/canon/candidates/[a-z0-9_-]+/governance$"),
)

_PUBLIC_MUTATION_PATTERNS = (
    ("PUT", re.compile(r"^/api/canon/candidates/[a-z0-9_-]+/resonance$")),
)

_RESONANCE_COOKIE = "echo_resonance_id"


def _admin_api_key() -> str:
    settings = get_settings()
    if settings.admin_api_key:
        return settings.admin_api_key.strip()
    if settings.admin_api_key_file:
        try:
            return settings.admin_api_key_file.read_text(encoding="utf-8").strip()
        except OSError:
            return ""
    return ""


def _user_jwt_secret() -> str:
    settings = get_settings()
    if settings.user_jwt_secret:
        return settings.user_jwt_secret.strip()
    if settings.user_jwt_secret_file:
        try:
            return settings.user_jwt_secret_file.read_text(encoding="utf-8").strip()
        except OSError:
            return ""
    return ""


def _governance_secret() -> str:
    settings = get_settings()
    secret = (
        (settings.governance_cookie_secret or "").strip()
        or _user_jwt_secret()
        or _admin_api_key()
    )
    if secret:
        return secret
    if settings.environment.strip().lower() == "production":
        raise HTTPException(
            status_code=503,
            detail="ECHO production governance signing is not configured",
        )
    return "echo-local-governance-only"


def _sign_resonance_token(token: str) -> str:
    digest = hmac.new(
        _governance_secret().encode("utf-8"),
        token.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def _valid_resonance_token(value: str) -> str | None:
    try:
        token, signature = value.rsplit(".", 1)
    except ValueError:
        return None
    if len(token) < 24 or len(token) > 128 or not re.fullmatch(r"[A-Za-z0-9_-]+", token):
        return None
    if not secrets.compare_digest(signature, _sign_resonance_token(token)):
        return None
    return token


def _request_voter_identity(request: Request, *, create: bool) -> tuple[str | None, str | None, str | None]:
    authorization = request.headers.get("authorization", "")
    bearer = authorization[7:].strip() if authorization.lower().startswith("bearer ") else ""
    jwt_secret = _user_jwt_secret()
    if bearer and jwt_secret:
        try:
            claims = decode_hs256(bearer, jwt_secret)
        except JWTError:
            claims = None
        if claims is not None:
            return f"user:{claims['sub']}", "registered", None

    raw_cookie = request.cookies.get(_RESONANCE_COOKIE, "")
    token = _valid_resonance_token(raw_cookie) if raw_cookie else None
    if token:
        return f"device:{token}", "anonymous", None
    if not create:
        return None, None, None
    token = secrets.token_urlsafe(32)
    signed = f"{token}.{_sign_resonance_token(token)}"
    return f"device:{token}", "anonymous", signed


def _request_reviewer_identity(
    request: Request,
    requested_reviewer: str | None,
) -> tuple[str, str, str]:
    authenticated_user = getattr(request.state, "echo_user_id", None)
    if authenticated_user:
        claims = getattr(request.state, "echo_user_claims", {})
        reviewer = str(claims.get("reviewer_id") or "").strip()
        roles_value = claims.get("roles", [])
        roles = (
            {item.strip() for item in roles_value if isinstance(item, str) and item.strip()}
            if isinstance(roles_value, list)
            else {item for item in str(roles_value).split() if item}
        )
        if not reviewer or "canon_reviewer" not in roles:
            raise HTTPException(
                status_code=403,
                detail="a canon reviewer claim is required",
            )
        if requested_reviewer and requested_reviewer.strip() != reviewer:
            raise HTTPException(status_code=403, detail="reviewer must match the authenticated identity")
        return reviewer, f"user:{authenticated_user}", "reviewer_jwt"

    requested = (requested_reviewer or "").strip()
    if not requested:
        raise HTTPException(status_code=400, detail="reviewer is required")
    if getattr(request.state, "echo_is_admin", False):
        admin_fingerprint = hashlib.sha256(_admin_api_key().encode("utf-8")).hexdigest()[:24]
        return requested, f"admin:{admin_fingerprint}", "admin_override"
    if not _admin_api_key() and get_settings().environment.strip().lower() != "production":
        return requested, f"local:{requested}", "local_development"
    raise HTTPException(status_code=401, detail="a reviewer session is required")


def _governance_json_response(payload: dict[str, object], request: Request, new_cookie: str | None) -> JSONResponse:
    response = JSONResponse(payload)
    response.headers["Cache-Control"] = "no-store"
    if new_cookie:
        response.set_cookie(
            _RESONANCE_COOKIE,
            new_cookie,
            max_age=365 * 24 * 60 * 60,
            httponly=True,
            secure=request.url.scheme == "https",
            samesite="lax",
            path="/",
        )
    return response


def _is_user_route(request: Request) -> bool:
    return any(
        request.method == method and pattern.fullmatch(request.url.path)
        for method, pattern in _USER_ROUTE_PATTERNS
    )


def _require_self(request: Request, user_id: str) -> None:
    if not _admin_api_key() or getattr(request.state, "echo_is_admin", False):
        return
    authenticated_user = getattr(request.state, "echo_user_id", None)
    if not authenticated_user or not secrets.compare_digest(authenticated_user, user_id):
        raise HTTPException(status_code=403, detail="cannot access another user's universe data")


def _is_public_read(request: Request) -> bool:
    if request.method not in {"GET", "HEAD", "OPTIONS"}:
        return False
    path = request.url.path
    return (
        path in _PUBLIC_EXACT_PATHS
        or path.startswith(_PUBLIC_PATH_PREFIXES)
        or any(pattern.fullmatch(path) for pattern in _PUBLIC_READ_PATTERNS)
    )


def _is_public_mutation(request: Request) -> bool:
    return any(
        request.method == method and pattern.fullmatch(request.url.path)
        for method, pattern in _PUBLIC_MUTATION_PATTERNS
    )


_STATIC_PREFIXES = ("/home/", "/universe/", "/developers/", "/console/", "/review/", "/assets/")
_IMMUTABLE_SUFFIXES = (".woff2", ".woff", ".ttf")
# 爬虫协议与站点地图没有 ?v= 指纹，改动后要能较快生效，因此单独给一个短周期。
_CRAWLER_FILES = ("/robots.txt", "/sitemap.xml")


@app.middleware("http")
async def static_cache_headers(request: Request, call_next):
    """给静态资源补 Cache-Control。

    StaticFiles 只发 ETag，浏览器每次仍要回源验证。HTML 保持 no-cache 以便
    发版即生效，带 ?v= 指纹的 CSS/JS 与字体则可长期缓存。
    """
    response = await call_next(request)
    if response.status_code >= 400 or "cache-control" in response.headers:
        return response
    path = request.url.path
    if path in _CRAWLER_FILES:
        response.headers["Cache-Control"] = "public, max-age=3600"
        return response
    if not (path == "/" or path.startswith(_STATIC_PREFIXES)):
        return response
    if path.endswith(_IMMUTABLE_SUFFIXES):
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    elif path == "/" or path.endswith((".html", "/")):
        response.headers["Cache-Control"] = "no-cache"
    elif request.url.query.startswith("v=") or "&v=" in request.url.query:
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    else:
        response.headers["Cache-Control"] = "public, max-age=3600"
    return response


@app.middleware("http")
async def production_api_guard(request: Request, call_next):
    """Protect user state and all mutations when a production admin key is configured."""
    expected = _admin_api_key()
    if _is_public_read(request) or _is_public_mutation(request):
        return await call_next(request)
    if not expected:
        if get_settings().environment.strip().lower() == "production":
            return JSONResponse(
                status_code=503,
                content={"detail": "ECHO production administration is not configured"},
            )
        return await call_next(request)
    authorization = request.headers.get("authorization", "")
    bearer = authorization[7:].strip() if authorization.lower().startswith("bearer ") else ""
    supplied = bearer or request.headers.get("x-echo-api-key", "").strip()
    if supplied and secrets.compare_digest(supplied, expected):
        request.state.echo_is_admin = True
        return await call_next(request)

    jwt_secret = _user_jwt_secret()
    if bearer and jwt_secret:
        try:
            claims = decode_hs256(bearer, jwt_secret)
        except JWTError:
            claims = None
        if claims is not None:
            if not _is_user_route(request):
                return JSONResponse(
                    status_code=403,
                    content={"detail": "this operation requires an ECHO Universe administrator"},
                )
            request.state.echo_user_id = str(claims["sub"])
            request.state.echo_user_claims = claims
            return await call_next(request)

    return JSONResponse(
        status_code=401,
        content={"detail": "ECHO Universe authorization required"},
        headers={"WWW-Authenticate": "Bearer"},
    )

console_dir = Path("console")
if console_dir.exists():
    app.mount("/console", StaticFiles(directory=console_dir, html=True), name="console")
homepage_dir = Path("homepage")
if homepage_dir.exists():
    app.mount("/home", StaticFiles(directory=homepage_dir, html=True), name="homepage")
universe_dir = Path("universe")
if universe_dir.exists():
    app.mount("/universe", StaticFiles(directory=universe_dir, html=True), name="universe")
developers_dir = Path("developers")
if developers_dir.exists():
    app.mount("/developers", StaticFiles(directory=developers_dir, html=True), name="developers")
review_dir = Path("review")
if review_dir.exists():
    app.mount("/review", StaticFiles(directory=review_dir, html=True), name="review")
assets_dir = Path("assets")
if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
for static_name in ["outputs", "stories", "characters", "relationships", "bible", "factions", "technologies"]:
    static_dir = Path(static_name)
    if static_dir.exists():
        app.mount(f"/{static_name}", StaticFiles(directory=static_dir), name=static_name)


def get_root() -> Path:
    """FastAPI 依赖：返回引擎读写状态用的根目录。

    端点据此解析 data/ 路径，而不是在写盘的那一刻才调用 Path.cwd()，从而避免请求
    处理线程（尤其是 Starlette TestClient 的工作线程）落在错误的工作目录上把状态
    写进真实项目 data/。测试可用 app.dependency_overrides[get_root] 注入隔离根目录。
    """
    return get_settings().root


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


class ResonanceRequest(BaseModel):
    choice: Literal["support", "revise"] | None = None


class CommitteeVoteRequest(BaseModel):
    reviewer: str | None = None
    decision: Literal["approve", "reject"]
    expected_revision_sha256: str
    reason: str = ""


class ContinuityCheckRequest(BaseModel):
    reviewer: str | None = None
    verdict: Literal["pass", "veto"]
    expected_revision_sha256: str
    reason: str = ""
    issues: list[str] = []


class GovernancePromotionRequest(BaseModel):
    expected_revision_sha256: str


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


class ExternalFulfillmentRequest(BaseModel):
    user_id: str
    product_id: str
    purchase_ref: str
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


@app.get("/api/canon/candidates/{candidate_id}/governance")
def public_candidate_governance(
    candidate_id: str,
    request: Request,
    root: Path = Depends(get_root),
):
    identity, _, new_cookie = _request_voter_identity(request, create=True)
    try:
        payload = get_governance_state(
            candidate_id,
            root=root,
            viewer_identity=identity,
            viewer_secret=_governance_secret(),
        )
    except GovernanceError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _governance_json_response(payload, request, new_cookie)


@app.put("/api/canon/candidates/{candidate_id}/resonance")
def update_candidate_resonance(
    candidate_id: str,
    body: ResonanceRequest,
    request: Request,
    root: Path = Depends(get_root),
):
    identity, identity_kind, new_cookie = _request_voter_identity(request, create=False)
    if not identity or identity_kind not in {"registered", "anonymous"}:
        raise HTTPException(status_code=401, detail="a verified account or signed device is required")
    try:
        payload = set_resonance(
            candidate_id,
            identity=identity,
            identity_kind=identity_kind,
            choice=body.choice,
            secret=_governance_secret(),
            root=root,
        )
    except GovernanceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _governance_json_response(payload, request, new_cookie)


@app.get("/api/canon/governance/candidates")
def internal_governance_candidates(
    request: Request,
    root: Path = Depends(get_root),
):
    if not getattr(request.state, "echo_is_admin", False):
        if getattr(request.state, "echo_user_id", None):
            _request_reviewer_identity(request, None)
        elif _admin_api_key() or get_settings().environment.strip().lower() == "production":
            raise HTTPException(status_code=401, detail="a reviewer session is required")
    try:
        return list_governance_states(root=root, include_private=True)
    except GovernanceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/canon/governance/candidates/{candidate_id}/committee-votes")
def committee_vote(
    candidate_id: str,
    body: CommitteeVoteRequest,
    request: Request,
    root: Path = Depends(get_root),
):
    reviewer, actor_identity, auth_kind = _request_reviewer_identity(request, body.reviewer)
    try:
        return record_committee_vote(
            candidate_id,
            reviewer=reviewer,
            decision=body.decision,
            expected_revision_sha256=body.expected_revision_sha256,
            actor_identity=actor_identity,
            auth_kind=auth_kind,
            reason=body.reason,
            root=root,
        )
    except GovernanceError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.post("/api/canon/governance/candidates/{candidate_id}/continuity-checks")
def continuity_check(
    candidate_id: str,
    body: ContinuityCheckRequest,
    request: Request,
    root: Path = Depends(get_root),
):
    reviewer, actor_identity, auth_kind = _request_reviewer_identity(request, body.reviewer)
    try:
        return record_continuity_check(
            candidate_id,
            reviewer=reviewer,
            verdict=body.verdict,
            expected_revision_sha256=body.expected_revision_sha256,
            actor_identity=actor_identity,
            auth_kind=auth_kind,
            reason=body.reason,
            issues=body.issues,
            root=root,
        )
    except GovernanceError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@app.post("/api/canon/governance/candidates/{candidate_id}/promotions")
def governance_promotion(
    candidate_id: str,
    body: GovernancePromotionRequest,
    root: Path = Depends(get_root),
):
    try:
        return promote_public_candidate(
            candidate_id,
            expected_revision_sha256=body.expected_revision_sha256,
            root=root,
        )
    except GovernanceError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


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
def user_bindings(root: Path = Depends(get_root)):
    return [binding.model_dump(mode="json") for binding in list_user_bindings(root=root)]


@app.get("/api/bindings/{user_id}")
def user_binding(user_id: str, request: Request, root: Path = Depends(get_root)):
    _require_self(request, user_id)
    binding = get_user_binding(user_id, root=root)
    if binding is None:
        raise HTTPException(status_code=404, detail=f"user binding not found: {user_id}")
    return binding


@app.post("/api/bindings")
def bind_character(body: BindCharacterRequest, request: Request, root: Path = Depends(get_root)):
    _require_self(request, body.user_id)
    try:
        return bind_user_to_character(
            user_id=body.user_id,
            character_id=body.character_id,
            source=body.source,
            root=root,
        )
    except BindingError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.delete("/api/bindings/{user_id}")
def release_binding(user_id: str, request: Request, root: Path = Depends(get_root)):
    _require_self(request, user_id)
    try:
        return release_user_binding(user_id, root=root)
    except BindingError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/universe/feed/{user_id}")
def universe_feed(user_id: str, request: Request, root: Path = Depends(get_root)):
    _require_self(request, user_id)
    try:
        return get_universe_feed_for_user(user_id, root=root)
    except UniverseFeedError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/identity/tiers")
def identity_tiers(root: Path = Depends(get_root)):
    try:
        return [tier.model_dump(mode="json") for tier in list_identity_tiers(root=root)]
    except IdentityError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/identity/users/{user_id}")
def identity_user(user_id: str, request: Request, root: Path = Depends(get_root)):
    _require_self(request, user_id)
    try:
        return get_universe_identity(user_id, root=root)
    except IdentityError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/identity/assignments")
def identity_assignment(body: IdentityAssignmentRequest, root: Path = Depends(get_root)):
    try:
        return assign_identity(
            user_id=body.user_id,
            tier=body.tier,
            realms=body.realms,
            source=body.source,
            metadata=dict(body.metadata),
            root=root,
        )
    except IdentityError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/identity/check-realm")
def identity_check_realm(body: RealmAccessCheckRequest, request: Request, root: Path = Depends(get_root)):
    _require_self(request, body.user_id)
    try:
        return check_realm_event_access(
            user_id=body.user_id,
            scope=body.scope,
            realm_id=body.realm_id,
            root=root,
        )
    except IdentityError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/identity/check-npc")
def identity_check_npc(body: NPCAccessCheckRequest, request: Request, root: Path = Depends(get_root)):
    _require_self(request, body.user_id)
    try:
        return check_npc_access(
            user_id=body.user_id, npc_id=body.npc_id, action=body.action, root=root
        )
    except IdentityError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/skins/policies")
def skin_policies():
    try:
        return [policy.model_dump(mode="json") for policy in list_skin_policies()]
    except SkinError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/skins/check")
def skin_check(body: SkinAccessCheckRequest, request: Request):
    _require_self(request, body.user_id)
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
def realm_event_submit(body: RealmEventRequest, request: Request):
    submitter = body.submitter
    if _admin_api_key() and not getattr(request.state, "echo_is_admin", False):
        submitter = getattr(request.state, "echo_user_id", "")
    try:
        return submit_realm_event(
            title=body.title,
            summary=body.summary,
            scope=body.scope,
            realm_id=body.realm_id,
            submitter=submitter,
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
def economy_products(root: Path = Depends(get_root)):
    try:
        return [product.model_dump(mode="json") for product in list_products(root=root)]
    except EconomyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/economy/users/{user_id}/summary")
def economy_summary(user_id: str, request: Request, root: Path = Depends(get_root)):
    _require_self(request, user_id)
    try:
        return economy_account_summary(user_id, root=root)
    except EconomyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/economy/wallet/grant")
def economy_wallet_grant(body: WalletGrantRequest, root: Path = Depends(get_root)):
    try:
        return record_wallet_entry(
            user_id=body.user_id,
            amount=body.amount,
            reason=body.reason,
            ref_id=body.ref_id,
            metadata=dict(body.metadata),
            root=root,
        )
    except EconomyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/economy/purchases")
def economy_purchase(body: ProductPurchaseRequest, root: Path = Depends(get_root)):
    try:
        return purchase_product(
            user_id=body.user_id,
            product_id=body.product_id,
            character_id=body.character_id,
            root=root,
        )
    except EconomyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/economy/fulfillments")
def economy_fulfillment(body: ExternalFulfillmentRequest, root: Path = Depends(get_root)):
    try:
        return fulfill_external_purchase(
            user_id=body.user_id,
            product_id=body.product_id,
            purchase_ref=body.purchase_ref,
            character_id=body.character_id,
            root=root,
        )
    except EconomyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/economy/subscriptions/ghost")
def economy_ghost_subscription(body: GhostSubscriptionRequest, root: Path = Depends(get_root)):
    try:
        return activate_ghost_subscription(
            user_id=body.user_id,
            character_id=body.character_id,
            duration_days=body.duration_days,
            source=body.source,
            metadata=dict(body.metadata),
            root=root,
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
def neural_daily_life_run(root: Path = Depends(get_root)):
    return run_daily_life_tick(root=root)


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
def homepage_index():
    index = homepage_dir / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"service": "echo-universe-engine", "homepage": "not installed"}


@app.get("/robots.txt", include_in_schema=False)
def robots_txt():
    """爬虫协议必须位于站点根路径，因此不能只靠 /home 静态挂载提供。"""
    path = homepage_dir / "robots.txt"
    if path.exists():
        return FileResponse(path, media_type="text/plain; charset=utf-8")
    raise HTTPException(status_code=404, detail="robots.txt not installed")


@app.get("/sitemap.xml", include_in_schema=False)
def sitemap_xml():
    """站点地图同样要求根路径，robots.txt 中的 Sitemap 指向这里。"""
    path = homepage_dir / "sitemap.xml"
    if path.exists():
        return FileResponse(path, media_type="application/xml")
    raise HTTPException(status_code=404, detail="sitemap.xml not installed")
