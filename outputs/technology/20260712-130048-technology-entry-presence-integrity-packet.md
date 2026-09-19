# Technology Entry: Presence Integrity Packet

## Candidate Canon Entry

A Presence Integrity Packet is the audit bundle used during Analog Presence
Review. It proves that a licensed witness directly observed the relevant Home
Layer context before a contested routine, edge, refusal record, or archive asset
was changed.

The packet is not a truth machine. It only makes the witness event harder to
fake, easier to scope, and reviewable by White Harbor, courts, Memory Bank, or a
CHASER civil unit.

## Format Sketch

```yaml
presence_integrity_packet:
  review_id: civil_review_or_court_order_reference
  home_core_id_hash: scoped_domestic_core_identifier
  witness:
    license_type: white_harbor | hospital_social_work | chaser_civil | court_ordered
    identity_hash: scoped_witness_identifier
    conflict_disclosure: none | family_tie | creditor_tie | vendor_tie | unknown
  observation_window:
    start_time: signed_timestamp
    end_time: signed_timestamp
    mode: physical_visit | high_integrity_telepresence
    room_scope: medication | bedroom | kitchen | entry | care_station | other
  integrity_signals:
    - door_sensor_sequence
    - local_audio_watermark
    - medication_timer_alignment
    - home_core_response_hash
    - witness_biometric_liveness
    - network_route_latency_profile
  protected_context:
    care_routine: continue | downgrade_pending | transfer_pending | delete_pending
    dependent_person: absent | present | medically_vulnerable | legally_vulnerable
    refusal_record: absent | present | preserved_for_review
    privacy_boundary: minimal | expanded_by_order | breached
  risk_flags:
    - forged_presence
    - staged_room
    - witness_capture
    - overbroad_export
    - delay_harm
    - relationship_graph_rewrite
```

## What It Can Do

- Bind a witness observation to local Home Core sensor timing and scoped room
  context.
- Preserve the minimum refusal, care, and dependent-condition records needed for
  review.
- Detect weak telepresence forgeries by comparing route latency, door events,
  medication timing, and Home Core response hashes.
- Expose reviewer conflicts of interest when a creditor, vendor, or family
  member funded the visit.
- Give Memory Bank a procedural basis for delaying sale, lien enforcement, or
  account closure without seeing the full home archive.

## What It Cannot Do

- Prove that a Ghost exists.
- Decide who owns the Home Core or family archive.
- Replace medical judgment for a living dependent.
- Override a valid Ghost Court ruling.
- Guarantee that the room was emotionally understood by the witness.

## Field Nickname

`Room Pulse` is the White Harbor nickname for a Presence Integrity Packet. The
term refers to door sensors, timer drift, liveness checks, local response hashes,
and witness route signatures. It is not a spiritual sign.

## Failure Modes

- A forged packet replays old door and medication signals with a fresh witness
  identity.
- A valid packet scopes the wrong room and misses the care routine that matters.
- A reviewer preserves too much memory, turning a witness visit into a privacy
  breach.
- A creditor uses review delay to pressure a family into selling archive rights.
- A Home Core changes behavior because it recognizes the witness as hostile,
  making observation alter the evidence.

## Countermeasures

- Compare local sensor timing against city infrastructure clocks and Home Core
  medication timers.
- Require conflict disclosure before Memory Bank can rely on a packet.
- Limit export to the room, routine, and relationship edge named in the review.
- Permit emergency CHASER or hospital social-work observation when delay itself
  creates dependent-care harm.
- Preserve an analog family interview when automated labels contradict lived
  care.

## Story Use

- Gives Shion a small, concrete technical artifact to inspect during a domestic
  case.
- Gives Sofia Marin a procedural lever that is not combat, rescue fantasy, or
  full system control.
- Lets Memory Bank be legally correct while still pricing delay and witness work
  against the family.
- Lets Black Zone sell forged compassion: a packet that feels merciful until it
  erases the only real room.
- Makes a home visit narratively important without implying magic or haunting.

## Consistency Notes

- Distinct from Witness Seal: Witness Seal protects testimony after capture;
  Presence Integrity Packet proves the contested home context was directly
  observed before action.
- Distinct from Civil Delay Token: delay token pauses imminent harm; this packet
  records and scopes the witness event.
- Distinct from Probate Divergence Seal: divergence seal preserves inheritance
  contradiction; presence packet verifies room-level observation in any
  contested Home Layer action.
- The mechanism uses sensor timing, cryptographic hashes, liveness checks,
  telepresence routes, court orders, medical records, and scoped exports. No
  magic, supernatural powers, multiverse, or time travel.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-07-12T13:00:48+08:00"
canon_promotion: false
related_candidates:
  - outputs/lore/20260712-130048-lore-entry-analog-presence-review.md
  - outputs/technology/20260626-130218-technology-entry-witness-seal.md
  - outputs/technology/20260630-130040-technology-entry-civil-delay-token.md
  - outputs/technology/20260711-130136-technology-entry-probate-divergence-seal.md
requires:
  - FactionAgent impact on witness access and packet abuse
  - ConsistencyAgent review against witness, delay, and probate mechanisms
asset_tasks: blocked_until_promotion
```
