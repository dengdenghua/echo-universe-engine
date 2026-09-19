# Canon Audit: The Door Waits Eight Minutes

Status: candidate_review

Reviewed item: `outputs/story/20260720-180421-story-beat-the-door-waits-eight-minutes.md`

Agent: StoryAgent + ConsistencyAgent

Created at: 2026-07-20T18:04:21+08:00

## Decision

```yaml
promotion_recommendation: hold
duplicate_detected: false
canon_safe_as_candidate: true
canon_promotion: false
reason: >
  The beat extends the Neighbor Care Standing candidate and Mara Ibe's split
  identity without promoting either. It is distinct from borrowed-care, clinic
  claim-hold, and body-loss plots, but it should remain candidate until Season 2
  routing decides whether Mara enters this early.
```

## Checked Against Canon

- `bible/seasons.md`: Season 2 uses global Memory Storm pressure across cities
  and Home Cores, with God Fragment effects grounded in infrastructure rather
  than physics changes.
- `technologies/god_fragments_mechanics.md`: City, Identity, and Archive
  pressure can operate through locks, identity registries, public records,
  evidence chains, shelter routing, and recognition systems without literal
  reality alteration.
- `outputs/lore/20260720-130258-lore-entry-neighbor-care-standing.md`: defines
  temporary informal-care standing for witness, comfort contact, essential care,
  access-pause witness, and contested care.
- `outputs/technology/20260720-130258-technology-entry-neighbor-care-standing-token.md`:
  supports an incident-scoped token that can permit witness or bounded care
  while blocking permanent access, archive export, money transfer, custody
  change, and claim assignment.
- `outputs/character/20260720-090320-candidate-character-028-mara-ibe.md`:
  establishes Mara's split civic identity, gate denial scar, provisional CHASER
  role, Ghost Claimant M-028, and fear that cleaner records can outrank her
  living body.
- `workflows/world_centric_story_rule.md`: opens with ordinary life,
  impossible memory event, legal and emotional consequence, then White Ghost
  investigation.

## Duplicate Check

No hard duplicate found.

Nearby material:

- `Claim Hold Lullaby`: clinic speaker, pediatric calm protocol, Memory Bank
  claim hold on an adaptive care routine. This candidate uses an apartment
  tower door, access-pause witness, split civic identity, and a neighbor's
  bounded care action.
- `Borrowed Morning`: domestic access denial caused by borrowed-care bleed
  around breakfast markets and landlord reset pressure. This candidate centers
  an identity-route collision and does not make the care routine itself the
  anomaly.
- `The Person Who Lost Their Body`: full legal identity displacement toward a
  Ghost copy. Mara remains living and embodied; the harm is Home Layer and city
  recognition failure.
- `Home Layer Mismatch Review`: defines mismatch review broadly. This story is
  a specific residential access-pause case using a different token pathway.
- `Probability Debt`: unseen cost displacement from prediction routing. This
  candidate does not depend on Noah's probability model.

## Continuity Fit

```yaml
world_centric: pass
case_character_agency: pass
white_ghost_function: pass
technology_grounding: pass
season_2_routing: pass
story_facing_terminology: pass
duplicate_status: clear
promotion_ready: not_yet
```

The strongest fit is the triangle between An Rui's ordinary care, Mara's living
identity harm, and M-028's possible emergent fear. It keeps the case civil and
procedural while making the Second Nervous System feel intimate: a locked door,
a cup of tea, and a city that prefers clean records over real lives.

## Risks Before Promotion

- Decide whether Mara Ibe should be introduced as a Season 1 late case, a
  Season 2 bridge character, or both. This beat assumes the audience can meet
  her while her candidate character file is still unpromoted.
- Avoid overusing door/access-denial beats if `Borrowed Morning` or Home Layer
  Mismatch Review becomes prominent in the Season 2 opening.
- Keep Ghost Claimant M-028 unresolved. The story should preserve evidence
  without proving personhood too early.
- If tower-door pause incidents recur, LoreAgent should define the protocol
  separately instead of leaving the rule embedded only in story text.
- Do not name City, Identity, or Archive Fragment in dialogue until the Season 2
  outline chooses the reveal cadence.

## Hard Rule Review

- No magic: pass.
- No supernatural powers: pass.
- No multiverse: pass.
- No time travel: pass.
- God Fragment effects remain infrastructural: pass.
- Uses story-facing terms: pass.
- Avoids disallowed product-document terms in prose: pass.

## Pipeline State

```yaml
stage: consistency_check
reviewed_at: "2026-07-20T18:04:21+08:00"
promotion: held_for_season_2_route_and_mara_intro_decision
next_agent_recommendation:
  - RelationshipAgent: prepare candidate relationship update only if Mara and
    M-028 remain in the Season 2 route.
  - LoreAgent: define tower-door pause protocol only if additional residential
    access-pause stories are generated.
  - StoryAgent: next route should avoid another care/access case and test a
    different pressure signature such as archive evidence, dream therapy, or
    medical body-control.
asset_tasks: blocked_until_promotion
```
