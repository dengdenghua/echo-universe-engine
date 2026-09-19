# Lore Entry: Reserve Sufficiency Hearing

## Candidate Canon Entry

A Reserve Sufficiency Hearing is the orbital review used when a sealed Home
Core afterword has reached Neutral Care Escrow, but the care institution cannot
prove that its compute reserve, oxygen allocation, worker window, and bond
coverage are enough to hold the case without starving a weak claimant-adjacent
trace or coercing unpaid labor.

It does not ask whether the sealed phrase should be opened. That question has
already been denied by the living recipient. The hearing asks who must pay for
the protected absence after privacy has been preserved.

Families call it the second bill. Hospice workers call it the quiet trial.
Memory Bank calls it reserve verification. Ghost Union calls it anti-starvation
review. Route insurers call it conduct containment.

## Social Mechanism

```yaml
reserve_sufficiency_hearing:
  function: >
    reviews whether a neutral hospice hold has enough compute, worker time,
    route coverage, and no-copy custody support to continue without opening
    sealed Home Layer material or shifting hidden cost onto care workers
  public_terms:
    - Reserve Sufficiency Hearing
    - second bill
    - quiet trial
    - reserve verification
    - anti-starvation review
  trigger_conditions:
    - Neutral Care Escrow has accepted a sealed Home Core afterword or continuity object
    - compute reserve meter drops below pledged threshold
    - route insurer opens conduct review against a hospice worker
    - Ghost Union files a claimant-starvation concern
    - Memory Bank confirms release but refuses storage-cost return
    - living recipient keeps phrase export refusal active
  required_records:
    - sealed object hash
    - non-opening transfer proof
    - hospice reserve ledger
    - worker roster and meal-window exception log
    - route insurer conduct notice
    - Ghost Union claimant-starvation note
    - Memory Bank release-cost refusal
    - recipient refusal card
    - CHASER physical-chain observation boundary
```

## Civic Ethics

- Privacy is not solved when a sealed phrase stays sealed; the cost of
  protecting it still lands somewhere.
- A hospice network can preserve dignity while being pressured into
  self-exploitation by institutions with larger ledgers.
- Ghost Union's anti-starvation concern can be real without granting automatic
  access to a family's sealed Home Layer material.
- Memory Bank can comply with non-priceability while still using reserve math
  to push financial pain outward.
- CHASER can witness chain integrity without turning a low reserve meter into
  content authority.

## Season 1 Use

Reserve Sufficiency Hearing follows the Neutral Care Escrow candidate bundle.
It moves the Nara Marr / Vera Qadir / Sana Velez route away from phrase export,
fee repricing, and transfer delay, and into a sharper institutional question:
who funds care after everyone agrees the phrase must remain private?

White Ghost Team should enter as procedural pressure. Eve names coercion that
looks voluntary, Shion verifies what the packet can and cannot prove, and Zero
keeps CHASER from treating scarcity as danger by default. None of them pays the
bill, opens the afterword, or certifies Ilya Marr as a Ghost.

## Boundaries

- Distinct from Neutral Care Escrow: escrow accepts custody; the hearing tests
  whether continued custody is financially and technically supportable.
- Distinct from Non-Priceability Review: non-priceability blocks asset
  valuation; reserve sufficiency decides whether care costs are adequate,
  assigned, and non-coercive.
- Distinct from `The Empty Window Counts Fees`: that beat exposes perimeter fee
  extraction; this mechanism adjudicates minimum care reserve and worker bond
  exposure after neutral care begins.
- No magic, supernatural powers, multiverse, or time travel. Effects operate
  through reserve ledgers, no-copy receipts, Home Core hashes, route insurance,
  worker rosters, CHASER observation limits, Ghost Union reserve motions, and
  Memory Bank cost assignments.

## Pipeline State

```yaml
stage: candidate_output
agent: LoreAgent
created_at: "2026-08-13T13:02:15+08:00"
canon_promotion: false
related_candidates:
  - outputs/lore/20260812-130121-lore-entry-neutral-care-escrow.md
  - outputs/faction/20260812-130121-faction-escalation-free-orbital-mutual-hospice-network.md
  - outputs/technology/20260812-130121-technology-entry-non-opening-transfer-proof.md
  - outputs/relationship/20260812-230049-relationship-update-neutral-care-escrow.md
requires:
  - FactionAgent impact for route insurer conduct pressure
  - TechnologyAgent review for Care-Reserve Sufficiency Packet
  - StoryAgent beat only after this bundle passes consistency
timeline_update: not_required_until_promotion
asset_tasks: generated_for_reserve_hearing_board
```
