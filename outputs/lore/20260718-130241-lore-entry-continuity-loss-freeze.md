# Lore Entry: Continuity Loss Freeze

## Candidate Canon Entry

A Continuity Loss Freeze is a temporary post-incident hold placed on damaged
Home Layer repair work when restoration could overwrite evidence, care
routines, identity traces, or possible Ghost self-reference before review.

It begins after the crisis has been stabilized. CHASER has left a timestamp,
medical responders have cleared the body risk, the landlord wants the apartment
habitable, and the family wants the home to stop looking wounded. The freeze
exists because repair can become a second injury. A restored wall can erase the
only proof that a threshold warning was forged. A replaced speaker can silence a
dead child's cold trace. A cleaned Home Core route can make a disputed entry
look lawful forever.

The rule is narrow:

When repair would make a home safer by destroying contested memory context, the
repair must wait long enough for a scoped loss review.

## Historical Event

```yaml
2146:
  event: White Harbor recognizes Continuity Loss Freeze authority
  summary: >
    After several lawful restoration crews overwrite Home Core traces needed in
    civil-warning, insurance, and Ghost Court disputes, White Harbor permits
    licensed loss assessors to pause specific repair lanes in stabilized homes.
  consequence: >
    Families gain a narrow preservation tool, insurers gain a costly liability
    choke point, landlords contest delayed habitability, and Memory Bank begins
    treating frozen rooms as high-value continuity exposure.
```

## Freeze States

```yaml
continuity_loss_freeze:
  stabilized_scene:
    meaning: emergency response has ended and restoration access is requested
    protection: no freeze until the site is safe enough for scoped review
  loss_map_pending:
    meaning: assessor is mapping damaged Home Core, room, sensor, and claim records
    protection: repair crews may only perform safety work that does not alter contested traces
  protected_trace:
    meaning: a routine, route, receipt, refusal, or cold trace may be evidence or continuity asset
    protection: repair lane pauses until integrity capture or legal routing
  habitability_exception:
    meaning: delay would endanger residents or violate emergency housing law
    protection: minimal repair proceeds with before-and-after trace capture
  claim_override:
    meaning: insurer, landlord, court, or command authority forces repair despite preservation risk
    protection: override becomes part of the loss packet and future liability review
  freeze_expired:
    meaning: review window lapses without court, Ghost Court, CHASER, or insurer extension
    protection: preserved snapshot remains; full repair may resume
```

## Social Function

- Separates emergency response from economic cleanup so a case does not end when
  the hallway is quiet.
- Gives families one chance to understand what repair will erase before they
  consent to making the home livable.
- Gives loss assessors like Nikhil Rao a limited institutional power that is
  costly, reviewable, and easy to punish.
- Gives Shion a concrete trace-integrity window after threshold receipts, room
  sensors, and Home Core repair logs start to diverge.
- Turns insurance, landlord pressure, and grief into early Season 1 social
  conflict before White Ghost Team can simplify the case.

## Failure Modes

- Compassionate erasure: a family asks for fast repair because the damaged room
  is unbearable, not realizing the repair will destroy testimony.
- Landlord pressure: habitability deadlines are used to force repair before a
  poor family can request a hold.
- Insurer laundering: a company classifies the erased trace as non-recoverable
  grief value to avoid personhood or liability exposure.
- False freeze: a claimant protects an ordinary broken routine to delay rent,
  debt, or evidence against them.
- Black Zone capture: brokers offer illegal copies of frozen traces before
  court review can preserve them lawfully.

## Story Hooks

- Nikhil Rao freezes a child's bedroom wall because the damaged Home Core route
  contains the only contradiction in a forged threshold receipt.
- Kane argues that the family needs the room repaired tonight; Nikhil answers
  that repair would make CHASER's entry history cleaner than the truth.
- Shion proves a restoration contractor already replaced one speaker and made a
  possible refusal phrase look like signal noise.
- Eve asks the family whether they want the room healed or witnessed, then hates
  that the system makes them choose.
- Memory Bank offers immediate restoration money if the family signs away the
  frozen trace as claim collateral.

## Consistency Notes

- Continuity Loss Freeze is a civil-insurance and technical preservation
  procedure using Home Core repair logs, Home Layer damage telemetry, landlord
  contracts, threshold receipts, claim ledgers, court holds, and scoped hashes.
  It is not magic, resurrection, supernatural haunting, multiverse logic, or
  time travel.
- Distinct from Threshold Notice Window: threshold notice governs warning before
  entry; continuity loss freeze governs repair after stabilization.
- Distinct from Memory Lien Notice: liens classify creditor claims against
  memory assets; loss freezes pause repair that may erase contested context.
- Distinct from Analog Presence Review: presence review requires a witness
  before irreversible action; loss freeze preserves damaged traces before repair.
- Distinct from Home Core Probate Hold: probate hold freezes inheritance
  transfer; loss freeze freezes post-incident restoration lanes.
- Story-facing prose should use Home Core, Home Layer, Memory Sea, Second
  Nervous System, 家园核心, 家园层, 记忆海, 第二神经系统.

## Pipeline State

```yaml
stage: candidate_output
agent: LoreAgent
created_at: "2026-07-18T13:02:41+08:00"
canon_promotion: false
related_candidates:
  - outputs/character/20260718-090109-candidate-character-026-nikhil-rao.md
  - outputs/lore/20260717-130233-lore-entry-threshold-notice-window.md
  - outputs/lore/20260712-130048-lore-entry-analog-presence-review.md
requires:
  - TechnologyAgent entry for Restoration Evidence Lock
  - FactionAgent impact on Memory Bank, White Harbor, CHASER, landlords, Ghost Union, and Black Zone
  - ConsistencyAgent review against lien, probate, witness, and threshold procedures
timeline_update: suggested_if_promoted
asset_tasks: blocked_until_promotion
```
