from __future__ import annotations

from pydantic import BaseModel, Field


class CharacterCard(BaseModel):
    id: str
    name: str
    zh_name: str | None = None
    codename: str | None = None
    age: str | None = None
    apparent_age: str | None = None
    faction: str | None = None
    rank: str | None = None
    status: str = "Alive"
    role: str | None = None
    theme: str | None = None
    abilities: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    relationships: dict[str, str] = Field(default_factory=dict)
    description: str = ""
    secret: str | None = None
    future: str | None = None
    quote: str | None = None
    visual_design: str | None = None
    illustration_prompt: str | None = None


class GenerationResult(BaseModel):
    mode: str
    title: str
    content: str
    canon_risks: list[str] = Field(default_factory=list)
    output_path: str | None = None


class UserCharacterBinding(BaseModel):
    user_id: str
    character_id: str
    agent_id: str
    character_name: str
    status: str = "active"
    created_at: str
    updated_at: str
    source: str = "mobile"


class UniverseFeed(BaseModel):
    user_id: str
    binding: UserCharacterBinding
    character_id: str
    agent_id: str
    character_name: str
    codename: str
    status: str
    day: int
    current_focus: str
    beliefs: list[str] = Field(default_factory=list)
    goals: list[str] = Field(default_factory=list)
    friends: dict[str, str] = Field(default_factory=dict)
    memory: list[str] = Field(default_factory=list)
    diary: list[dict[str, str]] = Field(default_factory=list)
    growth: list[dict[str, str]] = Field(default_factory=list)
    latest_diary: str | None = None
    latest_growth: str | None = None


class Realm(BaseModel):
    id: str
    name: str
    type: str
    parent_id: str | None = None
    status: str = "active"
    canon_tier: str = "local"
    owner_group: str = "world_brain"
    reviewer_group: str = "world_brain"
    default_approval: str = "world_brain_required"
    description: str = ""
    allowed_child_types: list[str] = Field(default_factory=list)


class RealmReviewRoute(BaseModel):
    requested_scope: str
    requested_realm_id: str | None = None
    resolved_realm_id: str
    resolved_realm_name: str
    canon_tier: str
    approval: str
    reviewer_group: str
    escalation_path: list[str] = Field(default_factory=list)


class NPCProfile(BaseModel):
    id: str
    name: str
    npc_type: str
    realm_id: str = "main"
    status: str = "active"
    character_id: str | None = None
    agent_id: str | None = None
    codename: str | None = None
    faction: str | None = None
    bindable: bool = False
    reviewer_group: str | None = None
    review_scope: str = "personal"
    canon_risk: str = "low"
    unlock_entitlement: str | None = None
    interaction_modes: list[str] = Field(default_factory=list)
    roles: list[str] = Field(default_factory=list)
    allowed_actions: list[str] = Field(default_factory=list)
    relationship_policy: str = "local_only"
    description: str = ""
    metadata: dict[str, object] = Field(default_factory=dict)


class NPCInteractionRoute(BaseModel):
    npc_id: str
    npc_name: str
    npc_type: str
    action: str
    realm_id: str
    review_scope: str
    reviewer_group: str
    approval: str
    canon_risk: str
    relationship_policy: str
    requires_entitlement: str | None = None
    escalation_path: list[str] = Field(default_factory=list)


class IdentityTierPolicy(BaseModel):
    id: str
    name: str
    rank: int
    default: bool = False
    max_review_scope: str = "personal"
    allowed_realms: list[str] = Field(default_factory=list)
    allowed_npc_types: list[str] = Field(default_factory=list)
    allowed_actions: list[str] = Field(default_factory=list)
    can_create_npc_types: list[str] = Field(default_factory=list)
    can_manage_realms: bool = False
    description: str = ""


class UserIdentityAssignment(BaseModel):
    user_id: str
    tier: str
    status: str = "active"
    source: str = "manual"
    created_at: str
    updated_at: str
    realms: list[str] = Field(default_factory=list)
    metadata: dict[str, object] = Field(default_factory=dict)


class UniverseIdentity(BaseModel):
    user_id: str
    tier: str
    tier_name: str
    rank: int
    status: str = "active"
    source: str = "default"
    edge_role: str = "edge_ghost"
    allowed_realms: list[str] = Field(default_factory=list)
    active_entitlements: list[str] = Field(default_factory=list)
    ghost_subscription_active: bool = False
    can_create_npc_types: list[str] = Field(default_factory=list)
    can_manage_realms: bool = False


class AccessDecision(BaseModel):
    user_id: str
    allowed: bool
    reason: str
    identity_tier: str
    requested_action: str
    requested_scope: str | None = None
    realm_id: str | None = None
    npc_id: str | None = None
    required_entitlement: str | None = None
    reviewer_group: str | None = None
    approval: str | None = None
    escalation_path: list[str] = Field(default_factory=list)


class SkinPolicy(BaseModel):
    id: str
    name: str
    skin_type: str
    max_scope: str
    default_realm_id: str = "personal_instance"
    reviewer_group: str | None = None
    requires_entitlement: str | None = None
    allowed_identity_tiers: list[str] = Field(default_factory=list)
    visual_constraints: list[str] = Field(default_factory=list)
    banned_claims: list[str] = Field(default_factory=list)
    description: str = ""


class SkinAccessRequest(BaseModel):
    user_id: str
    skin_type: str = "local_skin"
    requested_scope: str = "personal"
    realm_id: str | None = None
    claims: list[str] = Field(default_factory=list)


class SkinAccessDecision(BaseModel):
    user_id: str
    allowed: bool
    reason: str
    identity_tier: str
    skin_type: str
    requested_scope: str
    resolved_scope: str
    realm_id: str
    reviewer_group: str
    approval: str
    requires_entitlement: str | None = None
    required_downgrade: str | None = None
    visual_constraints: list[str] = Field(default_factory=list)
    banned_claims: list[str] = Field(default_factory=list)
    escalation_path: list[str] = Field(default_factory=list)


class ReviewerGroup(BaseModel):
    id: str
    name: str
    members: list[str] = Field(default_factory=list)
    can_review_groups: list[str] = Field(default_factory=list)
    can_review_realms: list[str] = Field(default_factory=list)
    can_review_scopes: list[str] = Field(default_factory=list)
    description: str = ""


class ReviewerAuthorization(BaseModel):
    reviewer: str
    allowed: bool
    reason: str
    required_group: str | None = None
    matched_group: str | None = None


class EconomyProduct(BaseModel):
    id: str
    name: str
    category: str
    price_credits: int = 0
    scope: str = "personal"
    active: bool = True
    description: str = ""
    grants: dict[str, object] = Field(default_factory=dict)
    metadata: dict[str, object] = Field(default_factory=dict)


class UserEntitlement(BaseModel):
    id: str
    user_id: str
    type: str
    ref_id: str
    status: str = "active"
    source: str = "manual"
    created_at: str
    expires_at: str | None = None
    metadata: dict[str, object] = Field(default_factory=dict)


class WalletLedgerEntry(BaseModel):
    id: str
    user_id: str
    amount: int
    balance_after: int
    reason: str
    ref_id: str | None = None
    created_at: str
    metadata: dict[str, object] = Field(default_factory=dict)


class GhostSubscription(BaseModel):
    user_id: str
    character_id: str
    agent_id: str
    status: str = "active"
    current_period_start: str
    current_period_end: str
    source: str = "manual"
    updated_at: str
    metadata: dict[str, object] = Field(default_factory=dict)


class EconomyAccountSummary(BaseModel):
    user_id: str
    wallet_balance: int
    entitlements: list[UserEntitlement] = Field(default_factory=list)
    ghost_subscription: GhostSubscription | None = None


class CanonStatus(BaseModel):
    bible_files: int
    characters: int
    factions: int
    locations: int
    technologies: int
    stories: int
    relationship_files: int
    timeline_files: int
