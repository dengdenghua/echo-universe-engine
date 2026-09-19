# Lore Entry: Latency Wake Hold

## Candidate Canon Entry

Latency Wake Hold is the orbital hospice procedure used when a body container,
a Home Core afterword, a kin-notice receipt, and a debt-seal clock arrive in the
wrong order.

It exists because orbital death does not happen on one clock. A miner may die
under Mars Authority liability, the body may reach a Ceres transfer hospice, the
family may still be waiting through relay delay, and Memory Bank may classify
the final message before anyone living has heard it. Latency Wake Hold does not
make death reversible or private. It preserves one relay window so custody,
consent, and farewell evidence can be named before the container becomes
insurer property.

Dock attendants call it a quiet dock. Families call it the late wake. Mars
Authority calls it cargo obstruction when the paperwork is weak. Memory Bank
calls it debt-contaminated continuity delay.

## Social Mechanism

```yaml
latency_wake_hold:
  function: >
    suspends body-container transfer and afterword debt attachment for one
    relay window when custody release, kin notice, consent, and Home Core
    afterword timing conflict
  public_terms:
    - Latency Wake Hold
    - quiet dock
    - late wake
    - kin receipt
    - warm cargo
  trigger_conditions:
    - recorded death or terminal transfer under orbital or Mars-route custody
    - body container release scheduled before kin-notice confirmation
    - Home Core afterword or consent packet still crossing relay delay
    - Memory Bank debt seal queued against the afterword or family archive
    - insurer custody claim active before family witness
    - licensed hospice attendant accepts liability for one relay window
  required_records:
    - death certification timestamp
    - body-container custody ledger
    - relay-window latency log
    - kin-notice receipt state
    - scoped Home Core afterword packet hash
    - medical or end-of-life consent boundary
    - Memory Bank debt-seal queue state
    - attendant liability signature
```

## Civic Ethics

- A final message is not automatically a Ghost, but it is still evidence of
  care, consent, duty, and grief.
- A body container is not only cargo, even when shipping law controls it.
- A family should not inherit debt simply because relay delay made them late to
  their own farewell.
- Mars Authority may enforce release clocks to protect scarce dock and hospice
  capacity, but it must name what human notice is being sacrificed.
- Memory Bank may price storage risk, but cannot attach an unopened afterword to
  oxygen debt before scoped kin notice review.
- Ghost Union may defend weak claimants, but publicizing an afterword phrase can
  convert private mourning into faction evidence.

## Season 1 Use

Latency Wake Hold gives Tarek Sol a world-centric orbital case. The opening
image is not White Ghost Team in transit; it is a daughter waiting for a signal
while a dock clock, a container seal, and a Memory Bank queue count down at
different speeds. White Ghost Team enters as outside witnesses after Tarek has
already made the hold and become liable for it.

The case should make Shion useful before combat: he can scope the Home Core
afterword without exporting the family's whole Home Layer. Eve can hear the
personhood ambiguity without erasing Nara Marr's living consent. Zero can keep
CHASER from flattening the dock into a quarantine event, but she cannot make
Mars Authority accept Earth-side moral language.

## Boundaries

- Distinct from Breath-Right Deposition: that procedure centers Mars oxygen-law
  coercion and refusal testimony; Latency Wake Hold centers postmortem body
  custody, kin notice, and farewell timing.
- Distinct from Red Delay packet verification: delay-chain verification proves
  packet order; Latency Wake Hold pauses a custody transfer when the order would
  create irreversible social harm.
- Distinct from Curfew Edge Review: curfew edge pauses Earth-side detention;
  Latency Wake Hold pauses orbital body-container release and afterword debt
  attachment.
- Distinct from Posthumous Shift Review: posthumous shift centers labor and
  payroll after death; Latency Wake Hold centers hospice custody and family
  farewell access.
- No magic, supernatural preservation, multiverse, or time travel. Effects
  operate through hospice licenses, cargo ledgers, relay timestamps, Home Core
  afterword packets, kin-notice receipts, Mars Authority rules, insurer custody,
  Memory Bank debt queues, and scoped ECHO/RED ARCHIVE exchange.

## Pipeline State

```yaml
stage: candidate_output
agent: LoreAgent
created_at: "2026-08-03T13:02:55+08:00"
canon_promotion: false
related_candidates:
  - outputs/character/20260803-090230-candidate-character-038-tarek-sol.md
requires:
  - TechnologyAgent review for a Latency Wake Custody Packet
  - FactionAgent review for Free Orbital Mutual Hospice Network pressure
  - RelationshipAgent review for Tarek Sol, Nara Marr, Ilya Marr afterword, Eve, Zero, Shion, Memory Bank, Mars Authority, and Ghost Union
timeline_update: suggested_if_promoted
asset_tasks: already_queued_for_tarek_sol
```
