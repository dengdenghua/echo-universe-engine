# Lore Entry: Reciprocal Wake Session

## Candidate Canon Entry

A Reciprocal Wake Session is a regulated Dream Network meeting where a living
participant and a Ghost, upload, or self-updating Home Core residue share a
bounded projection room while both sides retain an exit path.

It began as grief therapy. Hospitals, Dream Network clinics, and family courts
used it to let relatives say one more practical thing: a medication warning, a
burial preference, a custody note, a debt denial, an apology. It became
political when Ghosts argued that a session where only the living person could
leave was not therapy. It was visitation inside a cage.

The rule is simple in public and hard in practice:

Both sides must be able to wake from the meeting.

## Historical Event

```yaml
2133:
  event: Reciprocal Wake Session standard adopted by Dream Network clinics
  summary: >
    After several grief sessions trap unstable Ghost patterns in therapeutic
    projection rooms for extended questioning, Dream Network clinics require
    paired exit rights for living participants and digital participants.
  consequence: >
    Ghost Union treats reciprocal waking as a minimal dignity rule, Memory Bank
    demands exceptions for estate interviews, and Abyss settlements warn that a
    legal exit does not equal real freedom when compute access is priced.
```

## Session Requirements

```yaml
reciprocal_wake_session:
  required_participants:
    - living_participant_or_medical_proxy
    - ghost_upload_or_home_core_residue_claimant
    - licensed_sleep_mediator
  required_controls:
    - living_wake_anchor
    - digital_wake_anchor
    - consent_boundary_map
    - session_scope
    - memory_export_limit
    - distress_abort_phrase
  permitted_scopes:
    - grief_closure
    - care_instruction
    - family_contact_rights
    - estate_question
    - ghost_court_pre_interview
    - medical_recovery_contact
  prohibited_defaults:
    - indefinite_questioning
    - forced_emotional_performance
    - full_family_archive_export
    - body_tenancy_negotiation_without_court_presence
```

## Social Function

- Gives families a limited way to speak with the dead without treating every
  projection as proof of legal personhood.
- Gives Ghosts a minimum exit right inside therapeutic, legal, or commercial
  dream rooms.
- Gives Dream Network clinics a defensible procedure when therapy, testimony,
  and memory commerce overlap.
- Gives CHASER a non-combat path for interviewing a frightened pattern before
  threat classification.
- Gives early Season 1 scenes a civic sleep-room problem rather than a mystical
  dream encounter.

## Failure Modes

- Consent drift: a living participant agrees to grief closure, then the session
  becomes estate interrogation or custody pressure.
- Wake asymmetry: the living body wakes cleanly while the digital participant
  remains in a throttled projection loop.
- Therapeutic capture: a clinic extends sessions because grief billing is more
  profitable than release.
- False reciprocity: the Ghost has an exit button but no compute, sanctuary, or
  legal route outside the room.
- Identity bleed: repeated sessions teach a grieving person to prefer the
  projection version over living relationships.
- Abyss spillover: an unstable border route lets outside Ghost clusters enter a
  private session as witnesses, claimants, or predators.

## Story Hooks

- Ilya Sen pauses a session because the Ghost's wake anchor exists on paper but
  routes to a Memory Bank lien hold.
- Luna enters only after the mediator proves both wake anchors are live; her
  Dream Dive remains neural-interface traversal, not supernatural dreaming.
- Eve detects that the room is shaped to make the living participant forgive a
  creditor, not to help either side grieve.
- Shion finds that the digital wake anchor points to an Abyss settlement address
  that was overwritten by an Atlas safety mirror.
- A family wants one more bedtime conversation, but the Home Core residue uses
  its exit phrase first.

## Consistency Notes

- Reciprocal Wake Session is a Dream Network civil procedure using sleep
  scaffolds, Home Core residue, Echo Core interfaces, wake anchors, consent
  boundaries, court limits, and compute routing. It is not magic.
- Distinct from Analog Presence Review: presence review requires observation of
  a physical or high-integrity Home Layer context before irreversible action;
  reciprocal wake governs shared projection contact and exit rights.
- Distinct from Ghost Court projection: Ghost Court adjudicates identity and
  rights; a wake session may feed testimony into court but cannot decide
  personhood alone.
- Distinct from Luna's Dream Dive: Luna is a specialist who can traverse
  projection residue; the session is the civic room and consent structure.
- Story-facing prose should use Home Core, Home Layer, Memory Sea, Second
  Nervous System, Dream Network, Abyss, and Ghost.

## Pipeline State

```yaml
stage: candidate_output
agent: LoreAgent
created_at: "2026-07-13T13:02:55+08:00"
canon_promotion: false
related_candidates:
  - outputs/character/20260711-090215-candidate-character-022-ilya-sen.md
  - outputs/story/20260627-180205-story-beat-dream-child.md
  - outputs/lore/20260712-130048-lore-entry-analog-presence-review.md
requires:
  - TechnologyAgent entry for Wake Anchor Token
  - FactionAgent impact on Dream Network, Ghost Union, Memory Bank, CHASER, Abyss Alliance, Atlas, and Black Zone
  - ConsistencyAgent review against Dream Child, Analog Presence Review, Ghost Court projection, and Luna mechanics
timeline_update: suggested_if_promoted
asset_tasks: blocked_until_promotion
```
