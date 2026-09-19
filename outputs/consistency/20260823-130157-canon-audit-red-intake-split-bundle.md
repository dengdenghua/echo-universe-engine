# Canon Audit: Red Intake Split Bundle

```yaml
audit_id: "20260823-130157-canon-audit-red-intake-split-bundle"
source_candidates:
  - outputs/lore/20260823-130157-lore-entry-red-intake-split.md
  - outputs/technology/20260823-130157-technology-entry-red-intake-split-terminal.md
  - outputs/faction/20260823-130157-faction-impact-chaser-civil-contamination-intake.md
  - outputs/character/20260823-090208-candidate-character-048-inez-park.md
agent_lane: LoreAgent + FactionAgent + TechnologyAgent + ConsistencyAgent
audit_status: passed_as_candidate
canon_promotion: false
promotion_reason: >
  The bundle clarifies Inez Park's procedure and CHASER desk as candidate
  support, but no accepted story scene has yet validated Red Intake Split as
  recurring canon.
```

## Duplicate Check

- Not a duplicate of Civil Exposure Classification: that system names risk
  bands; Red Intake Split separates testimony custody from temporary permission
  restriction during early review.
- Not a duplicate of Exposure Class Override Ledger: that ledger contests a
  class label; Red Intake Split manages one witness's rights and access while
  the class remains unresolved.
- Not a duplicate of Witness Seal: Witness Seal preserves testimony; Red Intake
  Split also affects travel, work, guardian permissions, and Home Core
  disclosure scope.
- Not a duplicate of Lian Zhou's triage role: Lian evaluates contamination
  class and exit criteria; Inez and the intake desk perform first-contact
  procedural separation.
- Not a duplicate of White Harbor rights systems: White Harbor can support
  appeal routes, but CHASER still performs the restrictive action.

## Hard Rule Check

- No magic, supernatural powers, multiverse, or time travel.
- No mind reading, soul detection, memory erasure, literal resurrection, or
  metaphysical proof.
- All effects operate through CHASER terminals, Home Core disclosure scope,
  sealed statements, access ledgers, identity permissions, specialist review,
  transit gates, work credentials, and court/appeal procedure.
- The system has costs, failure modes, countermeasures, expiration pressure, and
  institutional misuse risk.

## Terminology Check

- Uses story-facing terms: Home Core, Home Layer, Memory Sea, Second Nervous
  System, Ghost, protected witness, red intake split.
- Avoids disallowed product-document phrasing in prose.
- Uses no literal supernatural soul mechanics; Ghost-adjacent evidence remains
  computational and legal, not mystical.

## Canon Fit

- Supports `world_centric=true` by making a civic desk and rights procedure the
  center of conflict.
- Keeps White Ghost Team as investigators, witnesses, and pressure points.
- Extends early Season 1 social wounds after Stranger Memory without duplicating
  the original surgeon-hands anomaly.
- Preserves reveal pacing: no Project E-01, Omega, Mother, God Fragment, ninth
  upload, or vessel reveal is introduced.
- Keeps CHASER morally divided: necessary, constrained, protective, coercive,
  and vulnerable to Central, Memory Bank, and Black Zone pressure.

## Promotion Gate

Before primary canon promotion, require:

- StoryAgent scene validation showing a red intake split harming and protecting
  a specific living witness;
- RelationshipAgent mapping for Inez Park, Zero, Eve, Shion, Lian Zhou, and the
  transit-collapse witness;
- a decision on whether CHASER Civil Contamination Intake remains a procedural
  desk or becomes a named subunit;
- a timeline note only if the procedure becomes recurring Season 1 structure.

## Decision

Candidate bundle accepted for pipeline staging only. Do not update
`bible/chaser_organization.md`, `factions/chaser.md`, `technologies/`, timeline,
or relationship canon until the story and relationship gates are satisfied.

## Pipeline State

```yaml
stage: consistency_check
candidate_output: true
canon_promotion: held
timeline_update: held
relationship_update: recommended_if_story_validates
faction_update: held_until_promotion
technology_update: held_until_promotion
asset_task: outputs/assets/20260823-130157-asset-task-prop-red-intake-split-terminal.yaml
```
