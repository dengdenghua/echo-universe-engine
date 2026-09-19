# Technology Entry: Cold Room Receipt

## Candidate Canon Entry

A Cold Room Receipt is the scoped evidence bundle created when a Home Core,
local mirror, clinic room, shelter node, or apartment access system cannot reach
the live Home Layer during a disputed care or access event. It records what was
known while the room was "cold": unavailable network path, cached household
rules, analog witness testimony, reversible actions taken, delayed replies, and
later reconciliation conflicts.

The receipt prevents institutions from treating a missing Home Layer answer as
clean consent, clean refusal, abandonment, fraud, or permanent authority. It is a
temporary civil evidence object, not a personhood finding.

```yaml
technology:
  name: Cold Room Receipt
  zh_name: 冷室回执
  category: outage evidence / Home Layer availability and analog witness log
  status: candidate
  related_lore: Home Layer Outage Witness Queue
  primary_users:
    - White Harbor shelter desks
    - clinic continuity clerks
    - licensed Home Layer witnesses
    - CHASER evidence monitors
    - Memory Bank care and rent auditors
    - White Ghost Team field investigators
  prohibited_use: >
    Cannot be used alone to prove consent, refusal, caregiver standing,
    household abandonment, Ghost claimant status, rent default, or identity
    transfer.
```

## Inputs

- Home Core availability pings, local mirror freshness, failed Home Layer route
  paths, clock drift, and delayed reconciliation notices.
- Cached access rules, medication routines, child pickup permissions, bedside
  restrictions, household safety blocks, and prior revocation markers.
- Analog witness records: paper notes, clinic desk signatures, shelter worker
  logs, neighbor testimony, body-camera hashes, and manual door seals.
- Reversible action log: medication given, supervised entry, heat or oxygen
  restored, child held in place, eviction delayed, account edit frozen.
- Institutional pressure log: landlord requests, insurer denials, Memory Bank
  audit notices, police desk instructions, CHASER quarantine triggers.

## Classification Fields

```yaml
cold_room_receipt_classes:
  clean_outage:
    meaning: Home Layer unavailable with no evidence of targeted interference
    risk: bureaucracy may still punish families for missing confirmation
  stale_mirror_used:
    meaning: local cache supported reversible action under time pressure
    risk: old permissions may contradict current consent
  analog_witness_action:
    meaning: human witnesses authorized temporary care or access
    risk: witness capture, intimidation, or later liability pressure
  delayed_refusal:
    meaning: Home Layer refusal arrived after emergency action
    risk: care may be reclassified as violation or abuse
  delayed_permission:
    meaning: Home Layer permission arrived after denial or delay
    risk: harm from late care becomes invisible
  targeted_silence:
    meaning: outage pattern maps to rent, debt, custody, labor, or evidence disputes
    risk: infrastructure failure is being used as policy violence
```

## Safeguards

- Marks all action during outage as provisional and reversible where possible.
- Freezes eviction, deletion, sale, transfer, claimant denial, and benefit
  clawback decisions until reconciliation.
- Keeps private Home Layer interiors hidden unless directly relevant to urgent
  care or access.
- Preserves analog witness chains before restored systems overwrite them.
- Requires a visible distinction between cached comfort routines and live Home
  Core answers.
- Routes targeted-silence patterns to CHASER evidence monitors without allowing
  quarantine to erase civil logs.

## Abuse Modes

- Memory Bank classifies missing replies as household noncompliance.
- Landlords trigger or exploit outages before lockout or rent-audit windows.
- Shelter contractors coach witnesses to support throughput rather than family
  safety.
- Black Zone brokers sell fake Cold Room Receipts to bypass access blocks.
- CHASER over-quarantines local mirrors and destroys the only proof of delay.
- Families are pressured to accept stale permissions because urgent care was
  needed.

## Story Limitations

- The receipt cannot restore the Memory Sea, force a Home Core to answer, grant
  permanent caregiver status, forgive debt, or decide Ghost personhood.
- It cannot make bad analog testimony clean; it only prevents machine silence
  from erasing the human choice.
- It should keep the central contradiction intact: a city that trusts homes to
  remember love must also decide what happens when the home goes quiet.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-07-28T13:02:15+08:00"
canon_promotion: false
related_lore: outputs/lore/20260728-130215-lore-entry-home-layer-outage-witness-queue.md
requires_consistency_review: true
```
