# Lore Entry: Curfew Edge Review

## Candidate Canon Entry

Curfew Edge Review is the civil-release procedure used when an automatic
detention clock, a supervised-release wrist monitor, and a Home Core door record
disagree during the last minutes before enforcement.

It exists because a city that runs punishment through the Second Nervous System
can make poverty look like intent. A person can be late because they chose harm,
because the stairwell gate drifted, because a living complainant needed
protection, or because the Home Layer repeated an old care routine at the worst
possible second. Curfew Edge Review does not forgive the violation. It preserves
the contradiction long enough for a human witness to decide what must be scoped
before detention executes.

Rosa Valen calls the pause a Mercy Hold. The release office calls it a bounded
review. CHASER calls it risk delay. Memory Bank calls it a compliance-risk
event. Families call it the second door.

## Social Mechanism

```yaml
curfew_edge_review:
  function: >
    pauses automatic detention long enough to compare curfew telemetry,
    stairwell access, living-complainant risk, and scoped Home Layer evidence
  public_terms:
    - curfew edge
    - Mercy Hold
    - second door
    - door witness
    - compliance strip
  trigger_conditions:
    - curfew breach within final enforcement margin
    - wrist-monitor location conflict
    - stairwell or building-gate clock drift
    - Home Core door routine relevant to the breach
    - living complainant safety warning
    - CHASER liaison ping before auto-warrant
  required_records:
    - wrist-monitor calibration state
    - geofence beacon confidence
    - stairwell access timestamp
    - scoped Home Core door log
    - complainant safety flag
    - release-desk witness signature
    - audit-exposure note for the officer who paused enforcement
```

## Civic Ethics

- A supervised person is not innocent because a door log disagrees with a
  wrist monitor.
- A living complainant is not cruel because they fear the person at the door.
- A Home Core care routine can be relevant evidence without proving that a dead
  person has become a Ghost.
- CHASER may override the hold when body-line danger is immediate, but must
  preserve the contradiction if the override destroys the only scoped witness.
- Memory Bank may price repeated holds as risk, but cannot attach a mother's
  afterword archive or family Home Layer room to compliance debt without review.
- A release officer who grants a Mercy Hold must name what evidence is being
  protected and what living risk is being delayed.

## Season 1 Use

Curfew Edge Review gives Rosa Valen a civic function distinct from Imani Vale.
Imani names who pays for a warm minute. Rosa names why punishment must wait for
a door witness. The White Ghost Team enters after the stairwell has already
panicked, which keeps the case world-centric: Lu Wen, the neighbor complainant,
Rosa's night desk, and Mei Wen's Home Core routine carry the first pressure.

## Boundaries

- Distinct from Threshold Notice Window: threshold notice warns before CHASER
  entry; Curfew Edge Review pauses release detention after a violation conflict.
- Distinct from Emergency Delay Window: emergency delay protects civil services
  around care and custody; Curfew Edge Review is tied to supervised-release
  geofences, wrist monitors, and auto-warrants.
- Distinct from Home Layer Mismatch Review: mismatch review classifies access
  contradictions; Curfew Edge Review preserves a narrow punishment-timing
  contradiction.
- Distinct from Amber Reserve Boundary: amber reserve governs clinic power
  draw; Curfew Edge Review governs automated detention timing.
- No magic, supernatural preservation, multiverse, or time travel. Effects
  operate through release law, wrist monitors, geofence beacons, stairwell
  clocks, Home Core door logs, audit ledgers, CHASER override queues, and Memory
  Bank compliance-risk classification.

## Pipeline State

```yaml
stage: candidate_output
agent: LoreAgent
created_at: "2026-08-02T13:02:50+08:00"
canon_promotion: false
related_candidates:
  - outputs/character/20260802-090147-candidate-character-037-rosa-valen.md
requires:
  - TechnologyAgent review for a scoped geofence and door-log evidence packet
  - FactionAgent review for White Harbor Civil Release Office pressure
  - RelationshipAgent review for Rosa, Lu Wen, Mei Wen afterword, Kane, Eve, Shion, Memory Bank, and the living complainant
timeline_update: suggested_if_promoted
asset_tasks: not_required
```
