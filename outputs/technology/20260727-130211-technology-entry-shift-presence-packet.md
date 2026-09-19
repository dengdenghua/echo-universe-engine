# Technology Entry: Shift Presence Packet

## Candidate Canon Entry

A Shift Presence Packet is the evidence bundle generated during a Posthumous
Shift Review. It compares worker identity, body presence, equipment behavior,
Home Core habit traces, payroll routing, and safety witness records before a
shift can be classified as living labor, proxy labor, preserved routine,
possible Ghost labor, or employer identity laundering.

The packet is designed for docks, clinics, transit maintenance, orbital
fabrication lines, and other environments where skill residue can remain useful
after death or continuity failure. It does not prove personhood and does not
authorize benefit clawbacks. It preserves contradictions long enough for civil
labor review.

```yaml
technology:
  name: Shift Presence Packet
  zh_name: 班次在场证据包
  category: labor identity evidence / Home Layer work-habit telemetry
  status: candidate
  related_lore: Posthumous Shift Review
  primary_users:
    - White Harbor Dock Safety Board
    - licensed labor witnesses
    - union safety archives
    - CHASER quarantine evidence teams
    - Memory Bank wage and survivor-benefit auditors
    - White Ghost Team field investigators
  prohibited_use: >
    Cannot be used alone to prove Ghost claimant status, wage ownership,
    survivor-benefit fraud, consent to posthumous labor, or employer innocence.
```

## Inputs

- Echo Core worker presence pings, badge handoff records, dock gate scans, and
  manual witness signatures.
- Exosuit motion logs, grip pressure, load path, emergency stop behavior,
  safety gestures, fatigue compensation, and vendor firmware revisions.
- Home Core work-habit metadata: alarm routines, medication timing, commute
  preparation, meal orders, apology loops, and old safety scripts.
- Payroll recipient, survivor benefit status, wage lien, equipment lease, and
  Memory Bank household-income classifications.
- Union ledgers, apprentice testimony, dock-camera hashes, quarantine lane
  delays, and analog shift books.
- Ghost claimant threshold markers when a work routine starts adapting to new
  conditions.

## Classification Fields

```yaml
shift_presence_classes:
  body_present:
    meaning: living worker body and credential match the shift
    risk: ordinary labor harm may still be hidden by clean telemetry
  assisted_living_worker:
    meaning: worker used lawful assistive automation while alive
    risk: vendor or employer may overstate automation contribution
  authorized_proxy:
    meaning: worker or estate authorized bounded proxy performance
    risk: consent term, payment target, or safety liability may be obscured
  routine_only:
    meaning: equipment followed preserved Home Layer habit without adaptive selfhood
    risk: payroll may still price it as household income
  adaptive_residue:
    meaning: the work trace corrected itself under new conditions
    risk: claimant preservation and family benefit protection collide
  forged_presence:
    meaning: employer, vendor, broker, or ledger relay inserted identity markers
    risk: wage theft and continuity fraud can be disguised as productivity
```

## Safeguards

- Freezes payroll and survivor clawback decisions while classification remains
  unresolved.
- Separates private Home Layer content from shift-relevant fatigue and work
  metadata.
- Requires manual labor-witness signature when machine logs and family routines
  disagree.
- Marks vendor firmware changes so automation cannot hide behind a worker's
  motion profile.
- Preserves claimant-threshold evidence without letting Ghost status decide the
  family's immediate food, rent, or benefit access.
- Allows CHASER quarantine seals to protect contamination evidence without
  deleting wage-chain records.

## Abuse Modes

- Memory Bank treats routine-only output as continued household income.
- Employers use adaptive residue to claim a dead worker consented to finish a
  contract.
- Black Zone brokers sell forged presence packets to create pension fraud or
  hide illegal Ghost labor.
- Ghost Union cells leak packets publicly before families consent, turning labor
  evidence into identity spectacle.
- Vendors classify dangerous exosuit autonomy as lawful assistive work.
- Unions over-preserve private fatigue metadata and expose vulnerable families.

## Story Limitations

- The packet cannot restore wages, forgive debt, unlock every dock gate, or
  decide personhood.
- It cannot read a worker's complete thoughts or resurrect consent.
- It cannot classify a shift without equipment, payroll, Home Layer, and manual
  witness evidence.
- It should keep the central contradiction intact: a dead person's duty may help
  the living while still being exploited by systems that price care as labor.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-07-27T13:02:11+08:00"
canon_promotion: false
related_lore: outputs/lore/20260727-130211-lore-entry-posthumous-shift-review.md
related_character_candidate: outputs/character/20260727-090139-candidate-character-032-marisol-keene.md
requires_consistency_review: true
```
