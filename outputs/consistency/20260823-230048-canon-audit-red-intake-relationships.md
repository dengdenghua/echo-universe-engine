# Canon Audit: Red Intake Relationship Pass

```yaml
audit_id: "20260823-230048-canon-audit-red-intake-relationships"
source_candidates:
  - outputs/relationship/20260823-230048-relationship-update-red-intake-split.md
  - outputs/story/20260823-180121-story-beat-the-appeal-notice-prints-twice.md
  - outputs/character/20260823-090208-candidate-character-048-inez-park.md
  - outputs/lore/20260823-130157-lore-entry-red-intake-split.md
  - outputs/technology/20260823-130157-technology-entry-red-intake-split-terminal.md
agent_lane: RelationshipAgent + ConsistencyAgent
audit_status: passed_as_candidate
canon_promotion: false
promotion_reason: >
  The relationship pass fills the 18:00 story validation requirement, but this
  bundle should remain candidate-only until Season 1 placement is chosen and a
  canon promotion pass explicitly accepts Red Intake Split as recurring CHASER
  procedure.
```

## Duplicate Check

- Not a duplicate of `Stranger Memory`: no new rescue is performed, and Lin
  does not repeat the dead-surgeon hand action.
- Not a duplicate of Lian Zhou's triage role: Lian supplies exit criteria and
  propagation thresholds; Inez remains the registrar who signs the split.
- Not a duplicate of Witness Seal: testimony protection is present, but the
  relationship wound includes work badge pause, amber transit clearance, Home
  Core reply review, and liability-note separation.
- Not a duplicate of Civil Exposure Classification: the pass does not create a
  new risk band. It maps a temporary permission split during review.
- Not a duplicate of prior Home Layer residency or municipal reset cases: the
  case centers a living witness's restricted permissions, not Ghost residency,
  care pricing, hidden labor, or room reset delay.

## Hard Rule Check

- No magic, supernatural powers, multiverse, or time travel.
- No mind reading, soul detection, literal possession, resurrection, memory
  erasure, or metaphysical proof.
- All relationship pressure operates through CHASER terminals, sealed
  statements, motor-habit packets, consent scope, Home Core routes, Home Layer
  privacy, access ledgers, work badges, transit gates, appeal notice custody,
  public footage, and liability records.
- Red Intake Split remains limited. It can separate protected testimony from
  temporary restriction, but it cannot certify Ghost personhood, prove intent,
  predict propagation, restore a paused badge, or make CHASER trusted.

## Terminology Check

- Story-facing terms are used: Home Core, Home Layer, Memory Sea, Second
  Nervous System, Ghost, protected witness, red intake split.
- No disallowed product-document phrases appear in the relationship pass.
- The technical phrase `household AI core` is not used.

## Relationship Fit

- Supports `world_centric=true`: the relationship engine is a civic intake
  procedure, an amber transit gate, a paused work badge, and an unsent family
  reply.
- Keeps protagonist priority low. Zero, Eve, Shion, and Lian act as pressure
  points; Lin Qiao and Inez Park carry the social wound.
- Preserves early Season 1 reveal pacing: no Project E-01, Omega, Mother, God
  Fragment, ninth upload, or vessel reveal.
- Keeps CHASER morally mixed. The institution protects a statement and harms
  the witness through the same procedure.
- Keeps the rail contractor as liability pressure, not a villain reveal.
- Keeps Lin's father offscreen and private; the Home Core message is ordinary
  care, not evidence.

## Promotion Gate

Before primary canon promotion, require:

- episode placement decision: Episode 1 aftermath, short interstitial, or later
  CHASER intake reference;
- explicit promotion of Inez Park or a decision to keep her one-off;
- FactionAgent decision on whether CHASER Civil Contamination Intake remains a
  procedural desk or becomes a named subunit;
- TechnologyAgent decision on whether Red Intake Split Terminal becomes a
  reusable technology entry;
- timeline note only if the intake route becomes recurring Season 1 structure;
- relationship YAML merge limited to durable deltas, not the full candidate
  web.

## Decision

Candidate relationship pass accepted. Do not update `bible/`, `characters/`,
`factions/`, `technologies/`, `timeline/`, or `relationships/` in this run.

## Pipeline State

```yaml
stage: consistency_check
candidate_output: true
canon_promotion: held
timeline_update: held
relationship_update: candidate_complete
faction_update: held_until_promotion
technology_update: held_until_promotion
asset_tasks:
  - outputs/assets/20260823-130157-asset-task-prop-red-intake-split-terminal.yaml
  - outputs/assets/20260823-180121-asset-task-scene-red-intake-appeal-notice.yaml
recommended_next_step: >
  At the next CharacterAgent or LoreAgent pass, avoid repeating Red Intake
  validation. The next useful work is either selecting Season 1 placement or
  moving to a new non-duplicate social wound.
```
