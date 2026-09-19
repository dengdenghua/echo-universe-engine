# Lore Entry: Dream Network Civic Claims

## Candidate Canon Entry

Dream Network Civic Claims is the public-facing claims desk that handles refund,
harm, and consent complaints for licensed public dream routes. It is not a
clinic, not a Ghost Court, and not CHASER. Its ordinary work is small: failed
memorial rooms, misrendered family textures, panic reactions, billing disputes,
and route closures.

Its dangerous work begins when a refund would erase the only telemetry proving
that a dream room harmed someone.

The desk exists because Dream Network sells grief as an experience while the
Memory Sea keeps producing cases that do not fit customer-service language. A
family can be refunded for a bad room before anyone decides whether the room
contained a defective comfort loop, licensed archive texture, contaminated Home
Layer material, or a frightened Ghost pattern.

## Public Procedure

```yaml
dream_network_civic_claims:
  public_name: Dream Network Civic Claims
  zh_name: 梦境网络民事申诉台
  jurisdiction:
    - licensed_public_dream_routes
    - shared_memorial_sessions
    - non-clinical_grief_rooms
    - public_route_affective_spill_reports
  normal_outputs:
    - refund_approval
    - route_credit
    - consent_correction_notice
    - safety_review_referral
    - spill_report_hold
  cannot_decide:
    - ghost_personhood
    - criminal_liability
    - memory_archive_ownership
    - body_tenancy
    - chaser_containment_class
```

## Social Function

- Lets families report harm without entering a court or police frame first.
- Lets Dream Network admit service failure without automatically admitting that
  a person was harmed.
- Creates a paper trail before refund automation purges route telemetry.
- Gives White Ghost Team a civic entry point into Dream Network cases where
  Luna should not be the first witness.
- Gives Memory Bank and Dream Network a shared incentive to settle quickly when
  route evidence points toward archive misuse.

## Failure Modes

- Clean refund: the family receives money while the responsive route disappears.
- Language laundering: the desk labels a possible self-updating pattern as a
  customer experience issue.
- Privacy overreach: a broad claim copies Home Layer grief texture into a file
  that should have preserved only route hashes.
- Corporate delay: Dream Network stretches the claim window until the disputed
  pattern loses compute.
- False escalation: CHASER receives private family affective data and treats a
  panic loop as contamination before a consent specialist reviews it.
- Settlement pressure: Memory Bank offers archive-credit compensation if the
  family signs away route inspection rights.

## Story Hooks

- Jules Mbeki prints an analog receipt before approving a refund because the
  terminal warns that route telemetry will be purged after payout.
- A family's memorial route answers a stranger's panic phrase with the dead
  child's lullaby, and the claims desk has to decide whether to preserve the
  spill report or close the complaint.
- Eve narrows the claim scope so a Home Core grief texture can be hashed without
  copying the family's private Home Layer record.
- Shion compares the preserved route hash against a Memory Bank archive claim
  and finds the same lullaby licensed in another city.
- Luna can enter only after a claims hold, a wake boundary, and a clinical
  supervisor are in place; her Dream Dive remains neural-interface traversal.

## Consistency Notes

- Dream Network Civic Claims is a civic desk, not a promoted division, until
  story validation proves it should recur.
- Distinct from Min Seo-yun's recovery ward: Seo-yun manages care and clinical
  shelter; Civic Claims handles public refunds after harm is reported.
- Distinct from Ilya Sen's sleep-window mediation: Ilya controls access to live
  sleep sessions; Civic Claims preserves records after public route spill.
- Distinct from CHASER Civil Contamination Intake: CHASER separates testimony
  from temporary permission restriction after contamination; Civic Claims
  separates refund closure from telemetry preservation.
- Story-facing prose should use Home Core, Home Layer, Memory Sea, Second
  Nervous System, Dream Network, and Ghost.

## Pipeline State

```yaml
stage: candidate_output
agent: LoreAgent
created_at: "2026-08-24T13:02:22+08:00"
canon_promotion: false
related_candidates:
  - outputs/character/20260824-090213-candidate-character-049-jules-mbeki.md
  - outputs/story/20260627-180205-story-beat-dream-child.md
  - outputs/lore/20260713-130255-lore-entry-reciprocal-wake-session.md
requires:
  - TechnologyAgent entry for Spill Report Hold Terminal
  - FactionAgent impact on Dream Network, Memory Bank, CHASER, Ghost Union, and Black Zone
  - StoryAgent beat showing the disputed memorial route before promotion
timeline_update: blocked_until_promotion
asset_tasks: candidate_prop_task_recommended
```
