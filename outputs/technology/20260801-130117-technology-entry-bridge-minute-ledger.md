# Technology Entry: Bridge Minute Ledger

## Candidate Canon Entry

The Bridge Minute Ledger is the record system used when clinic reserve is
temporarily bridged into warm-cache runtime, Home Layer witness preservation, or
CHASER evidence handoff.

It does not decide personhood. It records the cost and custody state of each
minute so later factions cannot pretend the warmth was free, stolen, or lawful
without evidence.

```yaml
technology:
  name: Bridge Minute Ledger
  zh_name: 桥接分钟账
  category: clinic reserve governance / Ghost witness preservation / Home Layer evidence
  status: candidate
  related_lore: Amber Reserve Boundary
  primary_users:
    - neighborhood clinic battery stewards
    - White Harbor witness officers
    - CHASER evidence teams
    - housing block night committees
    - Ghost Union observers under consent limits
  prohibited_use: >
    Cannot certify selfhood, hide living medical risk, sell route history,
    attach Home Core locations to debt, or extend a bridge after red reserve
    without named emergency authority.
```

## Ledger Fields

```yaml
bridge_minute_ledger:
  bridge_id: local clinic identifier plus sealed timestamp
  source_reserve:
    - clinic battery
    - respiratory reserve
    - housing heat buffer
    - donated visit minute
  recipient_state:
    - living_patient
    - weak_ghost_claimant
    - analog_witness_strip
    - seizure_handoff_buffer
  reserve_floor:
    green: routine care
    amber: named bridge allowed with consent record
    red: bridge closes unless emergency exception is signed
  required_signals:
    - battery draw
    - medical device safety margin
    - claimant runtime floor
    - Home Layer strip scope
    - CHASER sweep clock
    - guarantor consent state
  custody_outputs:
    - analog strip hash
    - redacted current route state
    - named-payer note
    - refused-payment note
    - living-patient injury warning
```

## Operations

- Bridge start: records why the warm minute is being opened and who is already
  below safe floor.
- Amber count: tracks each minute after routine reserve becomes contested.
- Red closure: forces bridge shutdown or signed emergency exception.
- Witness seal: preserves a claimant response without exposing unrelated Home
  Core rooms.
- Payer naming: records whether the minute came from a patient margin, block
  heat buffer, guarantor debt, clinic battery, or CHASER evidence exception.
- Lien firewall: blocks Memory Bank from converting emergency reserve records
  into route-history collateral without later review.

## Failure Modes

- Mercy laundering: a steward hides living-patient draw because the claimant's
  need feels urgent.
- Clean seizure harm: CHASER closes the bridge before the witness strip is
  sealed, then treats missing testimony as absence of claim.
- Debt capture: Memory Bank finances replacement charge in exchange for route
  telemetry or Home Core location data.
- Movement capture: Ghost Union pressures a clinic to publish bridge records as
  proof while exposing patient privacy and resident refusal.
- False balance: a ledger records both needs but pretends the steward had enough
  reserve to satisfy them.

## Story Limitations

Imani can use a Bridge Minute Ledger to force the room to name the cost. She
cannot make the cost fair, generate power, certify Tuesday, erase Lio's risk, or
protect the corridor if the records prove hidden harm.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-08-01T13:01:17+08:00"
canon_promotion: false
related_lore: outputs/lore/20260801-130117-lore-entry-amber-reserve-boundary.md
related_character: outputs/character/20260801-090302-candidate-character-036-imani-vale.md
requires_consistency_review: true
```
