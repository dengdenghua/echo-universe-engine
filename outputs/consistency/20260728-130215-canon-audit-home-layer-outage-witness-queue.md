# Canon Audit: Home Layer Outage Witness Queue

## Scope

Reviewed the 2026-07-28 13:02 candidate set:

- outputs/lore/20260728-130215-lore-entry-home-layer-outage-witness-queue.md
- outputs/technology/20260728-130215-technology-entry-cold-room-receipt.md
- outputs/faction/20260728-130215-faction-impact-home-layer-outage-witness-queue.md

## Consistency Result

```yaml
stage: consistency_check
agent: ConsistencyAgent
created_at: "2026-07-28T13:02:15+08:00"
result: pass_with_holds
canon_promotion: false
reason_for_hold: >
  Candidate creates a distinct outage-and-silence procedure, but should not be
  promoted until StoryAgent routes it through a concrete shelter, clinic, or
  apartment-block case and RelationshipAgent maps Eve/Raven/Shion/Memory
  Bank/CHASER pressure.
```

## Duplicate Check

- No existing candidate used the names Home Layer Outage Witness Queue, Cold
  Room Receipt, or 冷室回执.
- The candidate overlaps Neighbor Care Standing only through temporary civilian
  care. It stays distinct by focusing on ordering and evidencing action during
  Home Layer unavailability, not granting standing itself.
- The candidate overlaps Home Layer Mismatch Review only through later
  reconciliation conflict. It stays distinct by beginning when the Home Layer
  cannot answer safely, not when it answers incorrectly.
- The candidate overlaps Analog Presence Review only through licensed witnessing.
  It stays distinct by handling urgent action during outage rather than room
  presence before irreversible change.
- The candidate overlaps Continuity Loss Freeze only through preservation logic.
  It stays distinct by targeting live service silence, not repair work that may
  overwrite grief or identity evidence.

## Hard-Rule Check

- No magic, supernatural powers, multiverse, or time travel mechanisms are used.
- All effects route through Home Core availability, Home Layer route failure,
  local mirrors, access systems, clinic and shelter records, analog witness
  chains, Memory Bank classifications, and CHASER evidence monitors.
- The Cold Room Receipt cannot prove consent, refusal, Ghost personhood, or
  permanent caregiver authority.
- White Ghost Team remains secondary to the social wound and enters through
  investigation, witness protection, and pressure on institutional incentives.

## Terminology Check

- Story-facing terms used: Home Core, Home Layer, Memory Sea, Second Nervous
  System.
- No prose-facing use of forbidden product-document terms.
- Technical phrasing stays within canon boundaries and does not reframe ECHO as
  a generic product network.

## Promotion Requirements

```yaml
before_promotion:
  story_route:
    required: true
    suggested_titles:
      - "The Home Went Quiet"
      - "Eleven Minutes Late"
    opening_viewpoint: "clinic nurse, shelter clerk, neighbor witness, or affected family member; not White Ghost Team"
  relationship_review:
    required: true
    nodes:
      - Eve
      - Raven
      - Shion
      - Memory Bank
      - CHASER
      - White Harbor shelter desks
      - affected family
  canon_updates_if_promoted:
    - timeline/timeline.yaml
    - factions/memory_bank.md
    - factions/white_harbor.md
    - locations/white_harbor.md
    - relationships/relationships.yaml
  asset_tasks:
    status: held
    reason: "No new character or scene asset until StoryAgent selects the concrete outage case."
```
