# Lore Entry: Dirty Room Hold

Status: candidate

Agent: LoreAgent (with TechnologyAgent / FactionAgent support)

Created at: 2026-08-21T13:02:10+08:00

## Candidate Canon Entry

Dirty Room Hold is a White Harbor municipal reset exception that pauses an
automated post-eviction apartment reset for eight hours when the room may still
be performing live care, preserving evidence, or routing an unresolved Home Core
dependency through the Home Layer.

It is not a Ghost certification, anti-erasure power, property freeze, CHASER
seizure, or Memory Bank archive claim. Its force comes from reset orders,
biohazard routing, landlord release clocks, Home Core latch telemetry, Home
Layer disconnect notices, municipal supervisor liability, and limited CHASER
evidence lines.

```yaml
lore:
  name: Dirty Room Hold
  status: candidate
  social_function: >
    Lets a municipal reset supervisor leave a room dirty long enough to
    distinguish waste, evidence, property, live-care dependency, and possible
    Ghost witness without letting any one institution capture the whole room.
  primary_case: Apartment 6C / Selene Arif
  story_terms:
    - Home Core
    - Home Layer
    - Memory Sea
  prohibited_use: >
    Cannot certify personhood, reveal sealed Home Layer content, expose a full
    medical record, stop eviction permanently, erase debt, create a Ghost, or
    make a room immune to cleanup.
```

## Civil Procedure Shape

The hold starts when a reset crew reaches a room that the landlord, estate, or
court already considers ready to clear, but one room-level signal contradicts
that status.

Accepted exception classes:

- live-care dependency still routing through the room's Home Core
- unresolved Home Core disconnect or latch mismatch
- contamination mismatch between air-scrub and landlord release clocks
- missing-person property inventory that affects living dependency
- active or requested CHASER evidence line

The hold keeps the room state intact. It does not decide what the room means.

## Why It Matters

ECHO's Home Layer makes ordinary rooms socially dangerous after eviction. A
dead tenant's Home Core may still run a stove routine, medication reminder,
neighbor check-in, or grief habit that looks like waste until it is gone. A
clean room can erase the last proof that care remained active.

Dirty Room Hold gives early Season 1 a municipal underside: after the court,
landlord, Memory Bank, and family leave, someone still has to bag the objects.
That worker may be the last person who can keep the Memory Sea from receiving a
clean but false absence.

## Failure Modes

- Evidence collapse: the hold expires before CHASER or civil review arrives.
- Estate capture: Memory Bank files an estate-freeze request because preserved
  evidence makes the whole room newly valuable.
- Privacy exposure: the same dialysis reminder that proves live care exposes a
  living neighbor's medical dependency.
- Worker liability: if the room is later unsafe or commercially recoverable,
  the reset crew absorbs injury, delay, and turnover risk.
- Black Zone leakage: discarded Home Core latches, door tags, and voice chips
  move from clean rooms into grief resale chains.

## Story Limitations

Selene Arif can file the hold and protect the room state. Shion can test the
Home Core latch path. Eve can separate consent from exposure. Zero can narrow
the CHASER evidence line. Raven can trace the discard route.

None of them can use the hold to certify Apartment 6C as a Ghost, open sealed
family content, guarantee the neighbor's medical privacy, stop the landlord
release indefinitely, block Memory Bank pricing attempts, or solve the discard
market in the first case.

## Pipeline State

```yaml
stage: candidate_output
agent: LoreAgent
created_at: "2026-08-21T13:02:10+08:00"
canon_promotion: false
related_character: outputs/character/20260821-090055-candidate-character-046-selene-arif.md
related_technology: outputs/technology/20260821-130210-technology-decision-dirty-room-hold-held.md
related_faction: outputs/faction/20260821-130210-faction-dossier-white-harbor-civic-reset-service.md
requires_consistency_review: true
next_story_route: 18:00 StoryAgent can use Apartment 6C only if it avoids repeating An Lan's residency-mirror beat
```
