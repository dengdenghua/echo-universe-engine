# Canon Audit: Door Waits Eight Minutes Relationships

Status: candidate_review

Reviewed item: `outputs/relationship/20260720-230149-relationship-update-door-waits-eight-minutes.md`

Agent: RelationshipAgent + ConsistencyAgent

Created at: 2026-07-20T23:01:49+08:00

## Decision

```yaml
promotion_recommendation: hold
duplicate_detected: false
canon_safe_as_candidate: true
canon_promotion: false
reason: >
  The relationship update accurately extends the held story candidate and
  Neighbor Care Standing candidate without modifying primary canon. It should
  remain candidate until Season 2 routing decides whether Mara Ibe, An Rui, and
  M-028 become recurring relationship nodes.
```

## Checked Against Canon

- `workflows/world_centric_story_rule.md`: relationship emphasis stays on the
  civilian case wound first, with White Ghost Team as witnesses, investigators,
  and pressure points.
- `outputs/story/20260720-180421-story-beat-the-door-waits-eight-minutes.md`:
  all relationship lines come from the door-access incident, eight-minute
  Neighbor Care Standing Token, and split repair.
- `outputs/consistency/20260720-180421-canon-audit-the-door-waits-eight-minutes.md`:
  prior audit recommends holding promotion and keeping M-028 unresolved.
- `outputs/character/20260720-090320-candidate-character-028-mara-ibe.md`:
  Mara is a living human, not a Ghost, with split municipal records and a
  disputed claimant using her face.
- `outputs/lore/20260720-130258-lore-entry-neighbor-care-standing.md`: informal
  care is temporary, auditable, and explicitly not family authority.
- `outputs/technology/20260720-130258-technology-entry-neighbor-care-standing-token.md`:
  token scope blocks permanent access, archive export, money transfer, custody
  change, medical consent beyond emergency, identity repair authorization, and
  Memory Bank claim assignment.

## Duplicate Check

No hard duplicate found.

Nearby relationship material:

- `Claim Hold Lullaby` uses a clinic, borrowed-care routine, child calm
  protocol, and Memory Bank archive claim hold. This update uses a residential
  door, neighbor witness standing, living-body access repair, and disputed
  shelter claimant preservation.
- `Borrowed Morning` uses care-routine bleed and breakfast-market evidence.
  This update uses civic identity-route collision and a split between a living
  citizen and a cleaner claimant record.
- `The Person Who Lost Their Body` centers identity displacement toward a Ghost
  copy. Mara remains alive, embodied, and procedurally misrecognized.
- `Home Layer Mismatch Review` defines the broad mismatch category. This update
  only adds relationship consequences for one held candidate case.

## Consistency Fit

```yaml
world_centric: pass
case_character_agency: pass
white_ghost_function: pass
technology_grounding: pass
story_facing_terminology: pass
relationship_yaml_promotion: hold
timeline_promotion: hold
asset_task_generation: blocked_until_promotion
```

The strongest relationship addition is An Rui as proof that ordinary care can
be testimony without becoming ownership. Mara and M-028 create useful pressure
because both can be harmed by a clean repair, but neither relationship line
requires confirming M-028 as a full Ghost.

## Conflict Fixes Suggested

```yaml
suggested_fixes:
  - issue: "Mara's character file says she can anchor an early Season 1 case, while the latest story beat routes her to Season 2 / Episode 3."
    fix: >
      Keep Mara as a bridge candidate until the season route is decided. Do not
      promote the Season 1 claim or Season 2 episode number independently.
  - issue: "Multiple recent candidates use Home Layer access denial or care recognition."
    fix: >
      Direct the next StoryAgent run away from door, clinic, medicine, and
      borrowed-care beats. Prefer archive evidence, dream therapy, medical
      body-control, transit adjudication, or public infrastructure pressure.
  - issue: "An Rui's witness phrase could become a reusable unlock trope."
    fix: >
      Treat the phrase as an incident-scoped excerpt sealed inside a token, not
      a general password or permanent access method.
  - issue: "M-028's fear could be read as confirmed personhood."
    fix: >
      Keep all documents using disputed claimant language until Ghost Court or
      later canon makes a separate personhood decision.
```

## Hard Rule Review

- No magic: pass.
- No supernatural powers: pass.
- No multiverse: pass.
- No time travel: pass.
- All effects operate through Home Core, Home Layer, transit, shelter, Memory
  Bank, White Harbor, CHASER, and Ghost Court infrastructure: pass.
- Uses story-facing terms and avoids product-document terms in prose: pass.

## Pipeline State

```yaml
stage: consistency_check
reviewed_at: "2026-07-20T23:01:49+08:00"
promotion: held_for_season_2_route_and_mara_intro_decision
next_agent_recommendation:
  - StoryAgent: avoid another care/access case; change pressure signature.
  - LoreAgent: only define tower-door pause protocol after at least one more non-duplicate residential pause case.
  - RelationshipAgent: do not modify primary relationships.yaml until promotion.
asset_tasks: blocked_until_promotion
```
