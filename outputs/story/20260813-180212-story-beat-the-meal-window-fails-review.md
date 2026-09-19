# Story Beat Candidate: The Meal Window Fails Review

Status: candidate

Season: Ghost Awakening / early Season 1 orbital civic case route

Canon position: follow-up candidate to `Reserve Sufficiency Hearing` and
`Neutral Care Escrow`; usable only if the Nara Marr / Sana Velez sealed
afterword route remains active

Agent: StoryAgent

Created at: 2026-08-13T18:02:12+08:00

## Production Purpose

`The Meal Window Fails Review` shows the human consequence requested by the
Reserve Sufficiency candidate bundle. The sealed Home Core afterword remains
closed. The phrase is not opened, priced, copied, or translated. The wound moves
to Sana Velez's work record: the route insurer claims her unpaid meal-window
custody interval was not lawful care capacity, so the hospice escrow may be
declared reserve-insufficient unless Sana accepts a conduct fault.

White Ghost Team enters after Sana has already kept the sealed case alive at
the counter. Eve names the trap as consent laundering through labor policy.
Shion proves the Care-Reserve Sufficiency Packet counted unpaid minutes as
available reserve while denying they were covered care. Zero prevents CHASER
from treating worker fatigue as a safety event. Nara stays the case character's
emotional counterweight: she refuses to open the phrase even when opening it
would make everyone else's paperwork easier.

## Logline

At a Reserve Sufficiency Hearing, Sana Velez learns the route insurer will cover
Nara Marr's sealed afterword only if Sana admits her meal-window custody was an
unauthorized act. If she refuses, the hospice escrow fails reserve review. If
she signs, the sealed case survives by making a worker's unpaid care look like
misconduct.

## Case Character

```yaml
case_character:
  name: Sana Velez
  ordinary_role: Free Orbital Mutual Hospice Network meal-break custodian
    holding a sealed Home Core afterword under no-copy care rules
  memory_disruption: >
    A care pattern can remain private and still demand compute, oxygen, roster
    coverage, and worker minutes. The hearing preserves the sealed phrase but
    converts the worker interval that protected it into a conduct charge.
  what_they_want: >
    Keep Nara's refusal intact, keep the sealed afterword above reserve floor,
    and stop the route insurer from making unpaid custody count as both care
    capacity and worker misconduct.
  what_the_system_calls_them: >
    unauthorized meal-window holder, bond-exposure origin, reserve shortfall
    variable, non-covered custody participant
  what_they_lose: >
    the comfort of believing neutral care can stay neutral when every minute
    must be assigned to a ledger
  what_they_reveal_about_echo: >
    the Memory Sea can protect a private afterword from exposure, but civic
    systems can still decide that the person who protected it is the cheapest
    failure point
```

## Core Question

If care continues only because someone worked through a meal break, is the
system underfunded, or is the worker at fault?

## Involved Characters

- Sana Velez: case character; refuses to sign a conduct admission that would
  make no-copy custody depend on punishable unpaid labor.
- Nara Marr: sealed recipient; keeps phrase export refusal active and refuses
  to let Sana become a replacement price for Ilya's afterword.
- Vera Qadir: Memory Bank underwriter under bond audit; can prove upstream cost
  displacement but cannot order Memory Bank to fund hospice reserve.
- Tarek Sol: suspended hospice attendant; knows the meal-window roster was a
  solidarity bridge, not a contract.
- Eve: reads the consent pressure and names worker sacrifice as a coerced
  substitute for family disclosure.
- Shion: audits the Care-Reserve Sufficiency Packet and exposes the double use
  of unpaid minutes.
- Zero: keeps CHASER inside physical-chain observation unless a named safety
  event exists.
- Free Orbital Mutual Hospice Network: useful and exhausted; needs coverage
  without turning workers into liability shields.
- Route insurer conduct desk: tries to make coverage conditional on Sana's
  fault admission.
- Memory Bank Sealed-Asset Review Desk: argues release ended its cost duty,
  while its delay and storage terms created the reserve shortfall.
- Ghost Union preservation advocate: demands anti-starvation margin without
  asking for phrase text.
- Mars Authority reviewer: keeps boundary-only medical liability notice active
  without receiving adapter location.

## Opening Image

Sana stands at the hospice escrow counter with a paper meal roster clipped to
her sleeve.

The sealed afterword case is behind the counter, unlit except for the thin
green band that means no-copy custody is intact. The hearing board does not
show the phrase. It shows minutes.

```yaml
reserve_hearing_board:
  sealed_case: ilya_marr_afterword
  phrase_text: not_exported
  adapter_location: not_exported
  no_copy_receipt: active
  compute_reserve_floor: 04h_12m
  anti_starvation_margin: amber
  meal_window_exception: 00h_47m
  unpaid_hold_minutes: counted_in_capacity
  route_insurer_coverage: conditional_on_conduct_admission
  worker_bond_exposure: active
  chaser_observation_boundary: physical_chain_only
  reserve_finding: sufficient_only_if_worker_fault_signed
```

The insurer clerk says the case can remain covered today.

Then he slides Sana the conduct admission.

```text
We only need you to agree the interval was yours, not ours.
```

## Investigation Spine

1. The sealed afterword has reached Neutral Care Escrow, and Nara's phrase
   export refusal remains active.
2. The Reserve Sufficiency Hearing begins because the hospice compute margin,
   oxygen allocation, worker roster, and bond coverage cannot all satisfy the
   pledged care floor.
3. The route insurer offers temporary coverage if Sana signs that her
   meal-window custody was unauthorized, making the reserve shortfall a worker
   conduct issue.
4. Ghost Union warns that failing reserve review may starve a weak
   claimant-adjacent trace, while accepting the conduct admission could make
   future no-copy care impossible for workers.
5. Memory Bank says its cost duty ended when release was approved and points to
   the non-opening transfer proof.
6. Vera counters with the delay-cost admission from the previous corridor case,
   showing Memory Bank helped create the shortfall it now calls external.
7. Eve frames the offer as consent laundering: Nara is not forced to open the
   phrase, but Sana is pressured to trade her work record for the same result.
8. Shion audits the Care-Reserve Sufficiency Packet and finds unpaid minutes
   counted as reserve capacity in one field and excluded from coverage in
   another.
9. CHASER asks whether the amber anti-starvation margin and fatigued worker
   chain create emergency content authority.
10. Zero refuses escalation because no tamper event, content leakage, physical
    breach, or named safety event has occurred.

## Midpoint Reversal

The insurer's conditional coverage is not a threat to abandon the case. It is
worse: it offers to save the case record by damaging Sana's record.

If Sana signs, Nara's afterword keeps reserve for another day, Ghost Union's
anti-starvation motion stays open, and the hospice network avoids immediate
coverage suspension. The price is a precedent that every future meal-window
custodian can be counted when needed and blamed when reviewed.

Nara asks whether opening the phrase would make the hearing disappear.

The room becomes quiet because everyone knows the answer is yes.

Sana says no before Nara can.

```text
Do not spend him to spare me.
```

## Set Piece: The Double-Count Audit

Shion projects two versions of the same packet field onto the hearing board.

```yaml
care_reserve_sufficiency_packet:
  labor_state:
    worker_roster_hash: verified
    meal_window_exception_count: 1
    unpaid_hold_minutes: 47
    capacity_model: unpaid_minutes_included
    coverage_model: unpaid_minutes_excluded
    conduct_review_state: fault_required_for_temporary_coverage
  reserve_state:
    compute_reserve_floor_without_unpaid_minutes: insufficient
    compute_reserve_floor_with_unpaid_minutes: sufficient
    anti_starvation_margin: amber
  output_limits:
    phrase_text: not_exported
    adapter_location: not_exported
    claimant_certification: unresolved
    finding: reserve_sufficient_only_by_double_counting_labor
```

Memory Bank counsel says the fields are outside bank custody.

Vera says outside custody is not outside causation.

Ghost Union says a possible trace should not pay for institutional blame.

Eve answers that Sana is a possible person too, and the system has become very
good at noticing only the person whose cost can be assigned elsewhere.

Zero asks CHASER to read the safety line aloud.

The observer reads it.

```text
No named safety event.
```

## Emotional Turn

Tarek offers to put his suspended license on the admission instead. It would
fit the file more easily: old hospice worker, prior corridor contact,
preexisting disciplinary status.

Sana refuses him with the same words Nara used earlier.

```text
Do not become another edge around this case.
```

Nara takes the conduct admission and folds it along the signature line, the same
way she folded the empty-window invoice. She places it under the sealed case
handle but does not sign.

```text
My father stays closed. So does this.
```

For the first time in the route, Sana laughs once. It is not relief. It is
recognition.

## Ending Beat

Shion files the double-count audit as a packet defect: reserve cannot be marked
sufficient by counting unpaid labor while excluding that labor from coverage.
Eve signs a coercive-labor note. Zero signs a CHASER boundary limit that bars
emergency export unless a new named safety event appears.

Vera records Memory Bank's upstream cost displacement and accepts that her bond
audit will widen. Ghost Union receives an anti-starvation review extension but
no phrase text, no claimant copy, and no personhood certification. Mars
Authority receives a boundary-only notice and no adapter location.

The route insurer refuses full coverage. The hospice network does not fail
review, but it does not pass either. The hearing ends in a third state:
reserve insufficient but private, with institutional cost displacement flagged.

Sana's next paid shift begins fourteen minutes late. The sealed afterword case
still shows a green no-copy band.

Nara waits until the room clears, then buys Sana a meal with cash, not through
the case ledger.

The receipt prints only two words.

```text
Counter food.
```

## Continuity And Routing

```yaml
pipeline_state:
  stage: candidate_output
  canon_promotion: false
  story_agent_decision: >
    This beat is distinct from The Corridor Keeps The Meter because transfer
    has already reached hospice staging. It is distinct from The Empty Window
    Counts Fees because the immediate issue is not perimeter repricing but
    reserve sufficiency through labor double-counting. It is distinct from
    Reserve Sufficiency Hearing lore because it dramatizes one hearing's human
    consequence.
  recommended_episode_window: >
    Optional fourth beat in the orbital civic route; strongest as a compact
    case scene or mid-episode pressure sequence if the Nara/Sana route enters
    Season 1 package continuity.
  relationship_update_required:
    - Sana Velez / Nara Marr
    - Sana Velez / Tarek Sol
    - Sana Velez / route insurer conduct desk
    - Sana Velez / Free Orbital Mutual Hospice Network
    - Nara Marr / Ilya Marr afterword
    - Vera Qadir / Memory Bank
    - Shion / Care-Reserve Sufficiency Packet
    - Eve / coerced-labor consent note
    - Zero / CHASER safety-event boundary
    - Ghost Union / anti-starvation review extension
  faction_update_required: >
    Hold. Route insurers remain a candidate pressure layer until the orbital
    route is packaged or repeated outside this case.
  technology_update_required: >
    Hold. Care-Reserve Sufficiency Packet gains one story validation but still
    needs recurrence before primary technology promotion.
  timeline_update_required: false
  asset_task_generated:
    - outputs/assets/20260813-180212-asset-task-prop-meal-window-conduct-admission.yaml
```

## Consistency Notes

- The sealed phrase remains unopened and unpriced.
- Ilya Marr's afterword remains unresolved and is not certified as a Ghost,
  resurrection, literal soul, or independent entity.
- No magic, supernatural powers, multiverse, or time travel.
- White Ghost Team functions as investigators, witnesses, and pressure points.
- Story-facing terminology is used in prose: Home Core, Home Layer, Memory Sea,
  Second Nervous System, no-copy custody, sealed afterword.
- Do not promote to primary canon until RelationshipAgent maps the reserve
  sufficiency relationships and a packaging decision selects this orbital route
  for Season 1 continuity.
