# Canon Audit: Refund Button Relationships

```yaml
audit_id: "20260824-230155-canon-audit-refund-button-relationships"
reviewed_item: outputs/relationship/20260824-230155-relationship-update-refund-button-waits.md
source_candidates:
  - outputs/story/20260824-180057-story-beat-the-refund-button-waits.md
  - outputs/consistency/20260824-180057-canon-audit-refund-button-waits.md
  - outputs/lore/20260824-130222-lore-entry-dream-network-civic-claims.md
  - outputs/technology/20260824-130222-technology-entry-spill-report-hold-terminal.md
  - outputs/faction/20260824-130222-faction-impact-dream-network-civic-claims.md
agent_lane: RelationshipAgent + ConsistencyAgent
audit_status: passed_as_candidate
canon_promotion: false
promotion_reason: >
  The relationship pass resolves the required 23:00 follow-up and makes the
  civic prelude usable for Episode 5 routing, but primary canon should wait for
  a promotion decision on Dream Network Civic Claims as recurring desk versus
  one-case procedure.
```

## Duplicate Check

- Distinct from `Dream Child`: this relationship map centers public-claims
  pressure before live route review, not the ward case or Luna's first direct
  encounter with the frightened child-pattern question.
- Distinct from `Claim Hold Lullaby`: both use lullaby and claim pressure, but
  this case is a refund purge at a public Dream Network memorial route; `Claim
  Hold Lullaby` is a Season 2 clinic calm routine under Memory Bank claim hold.
- Distinct from `Red Intake Split`: CHASER receives a narrow low-threat notice
  only. No witness restriction, amber travel/work status, carrier-node framing,
  or bundled permission split is introduced.
- Distinct from `Home Layer Mismatch Review`: the family Home Layer remains
  hash-only and is not converted into a clinic or domestic mismatch desk.

## Hard Rule Check

- No magic, supernatural powers, multiverse, time travel, prophecy, or literal
  afterlife mechanics.
- All relationship pressure originates from Dream Network route telemetry,
  refund purge rules, consent ledgers, Home Core grief-texture references,
  Home Layer scope controls, Memory Bank archive objections, CHASER notice
  routing, and White Ghost Team review practice.
- Luna's Dream Dive is delayed and bounded by consent, wake boundary, and
  supervision. It is not treated as proof.
- The disputed route remains ambiguous: archive texture, comfort loop,
  contaminated Home Layer material, harmed participant residue, and early Ghost
  pattern all remain possible.

## Terminology Check

- Story-facing language uses Home Core, Home Layer, Memory Sea, Dream Network,
  Ghost, public route, refund hold, and spill report.
- No product-document phrasing appears in prose.
- The technical term `Spill Report Hold Terminal` is confined to candidate
  infrastructure context.

## Relationship Fit

- Supports `world_centric=true`: the family and civic desk carry the scene
  before White Ghost Team enters.
- Keeps protagonist priority low: Eve, Shion, and Luna provide boundary,
  verification, and restraint instead of solving the case.
- Strengthens Jules Mbeki without making him a hero lead. His action is a
  human signature that preserves proof while delaying compensation.
- Gives Mara and Leina separate pressures: Mara speaks and negotiates; Leina
  protects the child's privacy and signs only after scope is narrowed.
- Keeps Memory Bank procedurally plausible and morally dangerous.

## Decision

Relationship pass accepted as candidate. No canon promotion, timeline update,
relationship YAML update, faction promotion, or technology promotion should be
performed in this run.

## Required Follow-Up

```yaml
next_pipeline_steps:
  promotion_decision:
    required: true
    question: >
      Should Dream Network Civic Claims become a recurring named desk for
      Episode 5 routing, or remain a one-case claims procedure?
  if_promoted:
    relationship_yaml_candidates:
      - Jules_Mbeki -> Eve: consent-scope ally
      - Jules_Mbeki -> Shion: packet-sufficiency reliance
      - Jules_Mbeki -> Luna: useful witness delayed by consent boundary
      - Mara_Elian -> Luna: naming-boundary respect
      - Dream_Network_Civic_Claims -> Memory_Bank: archive-objection corridor
    timeline_update: Episode 5 civic prelude only
    faction_update: limited Dream Network desk note
  asset_tasks:
    - outputs/assets/20260824-130222-asset-task-prop-spill-report-hold-terminal.yaml
    - outputs/assets/20260824-180057-asset-task-scene-refund-button-waits.yaml
```
