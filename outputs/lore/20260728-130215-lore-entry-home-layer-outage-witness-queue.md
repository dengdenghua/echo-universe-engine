# Lore Entry: Home Layer Outage Witness Queue

## Candidate Canon Entry

A Home Layer Outage Witness Queue is a White Harbor civil procedure used when a
neighborhood, shelter block, clinic floor, or transit dorm loses reliable Home
Layer service and living people still need doors opened, medication schedules
confirmed, care routines honored, or family access disputed. It does not treat
silence from a Home Core as consent. It treats silence as an evidence problem
with a clock.

The queue exists because ECHO cities learned to let homes remember too much.
When the Memory Sea is available, a Home Core can confirm who usually gives
medicine, who is not allowed inside, whose voice calms a child, and which old
routine is only grief. During an outage, those confirmations disappear or arrive
late. Landlords, clinics, shelters, police desks, and Memory Bank auditors then
try to convert missing confirmation into denial, permission, fraud, abandonment,
or emergency authority.

The queue gives witnesses a narrow order of operations: preserve the outage,
protect bodies first, record analog testimony, defer irreversible account and
identity decisions, and wait for the Home Layer to reconcile before institutions
price the silence.

## Timeline Placement

- 2098: White Harbor shelters begin using local Home Core mirrors to coordinate
  medication, access, and child pickup during typhoon-blackout seasons.
- 2121: Memory Bank insurers add "nonresponsive household witness" clauses to
  care, rent, and survivor-support audits.
- 2139: A clinic outage causes three families to be denied bedside access
  because their Home Cores cannot answer standing requests.
- 2148: Early White Ghost Team cases expose how Home Layer silence can be used
  as consent by institutions that benefit from delay.

## Queue States

```yaml
home_layer_outage_witness_queue:
  body_risk_first:
    meaning: immediate medical, shelter, heat, oxygen, or child-safety risk
    protection: analog caregiver testimony may authorize reversible care
  access_dispute_hold:
    meaning: door, bedside, pickup, or shelter-entry authority is contested
    protection: entry may be supervised but account changes are frozen
  silence_is_not_consent:
    meaning: Home Core cannot respond, answer is delayed, or local mirror is stale
    protection: no irreversible sale, eviction, transfer, deletion, or consent event
  delayed_home_layer_reply:
    meaning: cached Home Layer answer arrives after manual action
    protection: logs both human choice and machine reply without erasing either
  witness_capture_risk:
    meaning: landlord, employer, clinic, or family faction pressures the witness
    protection: routes to White Harbor desk and CHASER evidence monitor
  reconciliation_conflict:
    meaning: restored Home Layer record contradicts analog testimony
    protection: moves to Home Layer Mismatch Review or Ghost Court intake
```

## Social Function

- Prevents outages from becoming automatic eviction, denial of care, asset
  transfer, or consent to continuity handling.
- Lets poor neighborhoods use analog witness chains without pretending they are
  as clean as live Home Layer records.
- Gives shelters and clinics a humane route for urgent care while keeping the
  record narrow enough for later review.
- Makes Memory Bank prove abuse rather than treating outage silence as household
  noncompliance.
- Gives White Ghost Team a way to enter cases as witnesses and pressure points
  after civilians have already made the hard choice.

## Failure Modes

- Silence laundering: a landlord treats a dead Home Core line as permission to
  clear an apartment.
- Care denial: a clinic refuses medication or bedside entry because the Home
  Layer cannot verify a caregiver.
- Proxy inflation: a neighbor's reversible help is later priced as permanent
  standing, debt, or household authority.
- Witness capture: the only analog witness is a shelter worker paid by the same
  contractor accused of abuse.
- Reconciliation overwrite: restored Home Layer data deletes the human decision
  made during the outage.
- False comfort: a cached voice model calms someone while hiding that the
  current Home Core answer is unavailable.

## Story Hooks

- A clinic nurse gives a child medicine based on a paper note and a neighbor's
  testimony, then the restored Home Layer says the mother revoked that neighbor
  last winter.
- Raven finds that an outage was localized to apartments with rent disputes,
  but the ledger classifies every missing reply as "tenant absent."
- Eve hears a stale Home Core lullaby replayed as consent and asks who benefits
  when a home cannot say no.
- Shion separates a cached comfort routine from a live refusal signal that
  arrived eleven minutes too late.
- Memory Bank offers emergency benefits only if the family accepts the outage as
  evidence of household noncompliance.
- CHASER wants to quarantine the local mirror before analog witness logs can be
  sealed.

## Boundaries

- Home Layer Outage Witness Queue is not Neighbor Care Standing. Standing grants
  scoped temporary authority; the queue ranks and records disputed action during
  infrastructure silence.
- It is not Home Layer Mismatch Review. Mismatch begins when the Home Layer
  answers wrongly; this procedure begins when it cannot answer safely.
- It is not Analog Presence Review. Presence review protects a witnessed room or
  relationship before change; this queue protects urgent action during service
  failure.
- It is not magic, intuition, or spiritual testimony. Effects operate through
  Home Core availability, local mirrors, shelter logs, clinic records, analog
  witness chains, access ledgers, Memory Bank classifications, and CHASER
  evidence monitors.
- Story-facing prose should use Home Core, Home Layer, Memory Sea, Second
  Nervous System, 家园核心, 家园层, 记忆海, 第二神经系统.

## Pipeline State

```yaml
stage: candidate_output
agent: LoreAgent
created_at: "2026-07-28T13:02:15+08:00"
canon_promotion: false
related_candidates:
  - outputs/technology/20260728-130215-technology-entry-cold-room-receipt.md
  - outputs/faction/20260728-130215-faction-impact-home-layer-outage-witness-queue.md
requires:
  - StoryAgent route through a shelter, clinic, or apartment-block outage before promotion
  - RelationshipAgent review for Eve, Raven, Shion, Memory Bank, CHASER, White Harbor shelters, and affected families
  - ConsistencyAgent review against Neighbor Care Standing, Home Layer Mismatch Review, Analog Presence Review, and Continuity Loss Freeze
timeline_update: suggested_if_promoted
asset_tasks: none_until_story_route
```
