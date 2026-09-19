# Canon Audit: Posthumous Shift Review

## Scope

Reviewed the 2026-07-27 13:02 candidate set:

- outputs/lore/20260727-130211-lore-entry-posthumous-shift-review.md
- outputs/technology/20260727-130211-technology-entry-shift-presence-packet.md
- outputs/faction/20260727-130211-faction-impact-posthumous-shift-review.md
- outputs/character/20260727-090139-candidate-character-032-marisol-keene.md

## Consistency Result

```yaml
stage: consistency_check
agent: ConsistencyAgent
created_at: "2026-07-27T13:02:11+08:00"
result: pass_with_holds
canon_promotion: false
reason_for_hold: >
  Candidate cleanly extends Marisol Keene's dock-labor case, but should not be
  promoted until StoryAgent routes the case and RelationshipAgent reviews the
  Marisol/Eve/Shion/Raven/Memory Bank/Ghost Union pressure map.
```

## Duplicate Check

- No existing candidate used the names Posthumous Shift Review, Shift Presence
  Packet, or 班次在场证据包.
- The candidate overlaps Memory Lien Notice only through finance pressure; it
  stays distinct by focusing on wage, survivor benefit, and labor identity.
- The candidate overlaps Neighbor Care Standing only through scoped civil
  authority; it stays distinct by focusing on work performance and payment.
- The candidate overlaps Breath Right Deposition only through labor-linked
  survival systems; it stays distinct by using exosuit and payroll evidence.

## Hard-Rule Check

- No magic, supernatural powers, multiverse, or time travel mechanisms are used.
- All effects route through Home Core routines, Home Layer work metadata, Echo
  Core presence pings, exosuit telemetry, payroll ledgers, Memory Bank
  classifications, CHASER quarantine seals, and union witness archives.
- Ghost personhood remains unresolved and cannot be proven by the evidence
  packet alone.
- White Ghost Team remains secondary to the social wound and enters through
  investigation, evidence preservation, and faction pressure.

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
    suggested_title: "The Shift That Would Not End"
    opening_viewpoint: "widow or dock-shift witness, not White Ghost Team"
  relationship_review:
    required: true
    nodes:
      - Marisol Keene
      - Eve
      - Shion
      - Raven
      - Memory Bank
      - Ghost Union
      - CHASER
      - White Harbor Dock Safety Board
  canon_updates_if_promoted:
    - timeline/timeline.yaml
    - factions/memory_bank.md
    - locations/white_harbor.md
    - relationships/relationships.yaml
  asset_tasks:
    status: blocked
    reason: "Marisol asset task already exists; case-specific dock/exosuit assets should wait for story route."
```
