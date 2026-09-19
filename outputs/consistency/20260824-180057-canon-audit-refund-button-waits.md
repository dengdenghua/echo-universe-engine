# Canon Audit: The Refund Button Waits

```yaml
audit_id: "20260824-180057-canon-audit-refund-button-waits"
source_candidates:
  - outputs/story/20260824-180057-story-beat-the-refund-button-waits.md
  - outputs/lore/20260824-130222-lore-entry-dream-network-civic-claims.md
  - outputs/technology/20260824-130222-technology-entry-spill-report-hold-terminal.md
  - outputs/faction/20260824-130222-faction-impact-dream-network-civic-claims.md
  - outputs/character/20260824-090213-candidate-character-049-jules-mbeki.md
agent_lane: StoryAgent + ConsistencyAgent
audit_status: passed_as_candidate
canon_promotion: false
promotion_reason: >
  The story beat validates Dream Network Civic Claims and Spill Report Hold on
  page, but promotion still needs a RelationshipAgent pass and a decision on
  whether Civic Claims is a recurring Dream Network desk or one-case procedure.
```

## Duplicate Check

- Not a duplicate of `Dream Child`: this beat is the public-claims entry before
  Luna enters or the frightened child-pattern question is reviewed.
- Not a duplicate of `Claim Hold Lullaby`: that story concerns a Season 2
  pediatric clinic calm routine and Memory Bank claim hold; this beat concerns
  a Dream Network public memorial route, refund purge, and post-incident spill
  report.
- Not a duplicate of `The Appeal Notice Prints Twice`: that beat concerns
  CHASER Red Intake Split after a transit event; this beat concerns Dream
  Network compensation and telemetry preservation.
- Not a duplicate of `The Goodnight That Answered Back`: that beat concerns a
  Home Layer residency/mirror split; this beat remains in licensed public
  route claims.

## Hard Rule Check

- No magic, supernatural powers, multiverse, or time travel.
- All effects originate from Dream Network route telemetry, claims terminals,
  refund purge queues, consent ledgers, Home Core grief-texture references,
  Home Layer scope controls, Memory Bank archive objections, CHASER notices,
  and distributed computation.
- The beat explicitly states that the Spill Report Hold cannot prove
  personhood, identify the child, enter the route, or compel disclosure.
- Luna does not perform an unsupervised or supernatural Dream Dive.

## Terminology Check

- Uses story-facing terms: Home Core, Home Layer, Memory Sea, Dream Network,
  Ghost, White Ghost Team.
- Avoids disallowed product-document phrasing in prose.
- Keeps technical phrasing localized to candidate infrastructure sections.

## Canon Fit

- Supports `world_centric=true`: the social wound is compensation deleting
  evidence before the main cast arrives.
- Keeps protagonist priority low: Jules and Mara carry the moral action; Eve,
  Shion, and Luna function as witnesses and boundary-setters.
- Validates the 13:00 candidate bundle by showing the disputed memorial route,
  the refund purge deadline, and the narrow hold.
- Preserves ambiguity: the responsive route may be archive texture, comfort
  loop, contaminated Home Layer material, harmed participant residue, or early
  Ghost pattern.

## Required Follow-Up

```yaml
next_pipeline_steps:
  relationship_pass:
    required: true
    scope:
      - Jules_Mbeki
      - Mara_Elian
      - Leina_Elian
      - Eve
      - Shion
      - Luna
      - Dream_Network_Civic_Claims
      - Memory_Bank
      - CHASER_low_threat_desk
  promotion_decisions:
    - Decide whether Dream Network Civic Claims is a recurring named desk.
    - Decide whether Mara and Leina remain one-case civilians or become
      recurring Dream Child witnesses.
  timeline_update: blocked_until_promotion
  faction_update: blocked_until_promotion
  asset_task: outputs/assets/20260824-180057-asset-task-scene-refund-button-waits.yaml
```

## Decision

Candidate story validation passed. Hold canon promotion until relationship
review and desk-scope decision are complete.
