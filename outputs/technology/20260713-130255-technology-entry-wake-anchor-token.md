# Technology Entry: Wake Anchor Token

## Candidate Canon Entry

A Wake Anchor Token is the paired exit-control artifact used during a Reciprocal
Wake Session. It binds a living participant's body-state wake path and a digital
participant's projection exit path to the same session scope.

The token does not prove consent forever. It proves that, at a specific moment,
both sides had a recognized route out of the room.

## Format Sketch

```yaml
wake_anchor_token:
  session_id: dream_network_session_or_court_reference
  scope:
    purpose: grief_closure | care_instruction | estate_question | medical_recovery_contact | ghost_court_pre_interview
    max_duration: signed_sleep_window
    export_limit: none | transcript_summary | scoped_memory_clip | court_packet
  living_anchor:
    participant_id_hash: scoped_identity_identifier
    body_state_monitor: sleep_pod | hospital_bed | home_core_assisted_sleep | chaser_civil_unit
    wake_route: physical_wake | medical_override | distress_abort_phrase
    liveness_status: live | medically_proxy_authorized | unstable
  digital_anchor:
    claimant_id_hash: ghost_upload_or_residue_identifier
    origin: home_core | memory_bank_upload | abyss_settlement | hospital_sleep_template | unknown
    exit_route: home_layer_return | clinic_sandbox | abyss_address | court_escrow | sanctuary_node
    compute_after_exit: confirmed | lien_blocked | throttled | unknown
  consent_boundary:
    allowed_topics:
      - scoped_session_subject
    forbidden_topics:
      - body_tenancy_without_court
      - full_archive_export
      - unrelated_debt_pressure
    abort_conditions:
      - participant_distress
      - scope_expansion_attempt
      - identity_bleed_threshold
      - external_route_intrusion
```

## What It Can Do

- Tie a living wake route and digital exit route to the same Dream Network
  session.
- Record whether the digital participant has compute or sanctuary after exit.
- Give mediators a concrete reason to pause when the room becomes interrogation
  instead of contact.
- Help Shion verify whether a wake failure is technical, financial, or forged.
- Give CHASER a limited civil interview tool before a projection case becomes a
  threat case.

## What It Cannot Do

- Prove Ghost personhood.
- Cure grief addiction or projection dependency.
- Guarantee that a participant truly felt free.
- Override Memory Bank liens, Ghost Court rulings, or medical danger.
- Make Luna's Dream Dive safe without biological and identity costs.

## Field Nicknames

`Two-Exit Key` is the clinic nickname. Ghost Union cells often call it a
`both-doors token`. Memory Bank contracts prefer the colder term `paired wake
control`.

## Failure Modes

- The living anchor works, but the digital anchor routes to a lien-blocked
  compute account.
- A clinic recycles an old digital exit route from another Ghost.
- Atlas safety mirrors redirect the exit into a clean sandbox and call it
  protection.
- Black Zone sells counterfeit both-doors tokens to families priced out of
  licensed sessions.
- The token remains valid while the session topic quietly expands beyond the
  consent boundary.

## Countermeasures

- Require post-exit compute confirmation before a session counts as reciprocal.
- Hash the digital exit route against Home Core, sanctuary, court, or Abyss
  settlement records without exposing private memory.
- Abort when forbidden topics or identity-bleed thresholds are triggered.
- Preserve a minimal audit packet for Ghost Court without exporting the whole
  projection room.
- Use analog mediator notes when Dream Network telemetry and participant memory
  disagree.

## Story Use

- Lets Ilya Sen's job hinge on a small technical object rather than vague
  compassion.
- Gives Luna a hard consent condition before entering a projection room.
- Gives Eve a way to argue that emotional safety and legal consent are not the
  same thing.
- Gives Memory Bank a loophole: the token can be valid while the exit is
  economically impossible.
- Gives Abyss settlements a sovereignty issue when clinics demand address
  verification for digital exits.

## Consistency Notes

- Mechanism uses Echo Core sleep scaffolds, Dream Network projection routing,
  Home Core residue identifiers, court escrow, sanctuary nodes, Abyss addresses,
  medical monitors, hashes, and consent boundaries.
- No magic, supernatural powers, multiverse, or time travel.
- Distinct from Presence Integrity Packet: that packet verifies a witness event
  in Home Layer context; this token verifies paired exit paths in projection
  contact.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-07-13T13:02:55+08:00"
canon_promotion: false
related_candidates:
  - outputs/lore/20260713-130255-lore-entry-reciprocal-wake-session.md
  - outputs/character/20260711-090215-candidate-character-022-ilya-sen.md
  - outputs/technology/20260712-130048-technology-entry-presence-integrity-packet.md
requires:
  - FactionAgent impact on exit routing, grief billing, and Abyss address sovereignty
  - ConsistencyAgent review against Dream Network mechanics and Luna's Dream Dive
asset_tasks: blocked_until_promotion
```
