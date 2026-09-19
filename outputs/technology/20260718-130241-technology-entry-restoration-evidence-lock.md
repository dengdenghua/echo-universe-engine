# Technology Entry: Restoration Evidence Lock

## Candidate Canon Entry

A Restoration Evidence Lock is the scoped technical artifact created during a
Continuity Loss Freeze. It marks which damaged Home Layer traces must not be
altered by repair, cleaning, replacement, claim adjustment, or landlord
habitability work until their evidentiary or continuity value is captured.

The lock is not a full archive export. It is a minimal preservation boundary:
what is frozen, why it matters, what repair work is allowed, who can override
the hold, and what must be recorded if the home is repaired anyway.

## Format Sketch

```yaml
restoration_evidence_lock:
  incident:
    incident_id: civil_warning_chaser_insurance_or_court_reference
    home_scope_hash: scoped_home_core_and_room_identifier
    created_at: signed_timestamp
    freeze_state: loss_map_pending | protected_trace | habitability_exception | claim_override | freeze_expired
  assessor:
    assessor_id_hash: licensed_loss_assessor_or_municipal_reviewer
    authority: insurer | white_harbor | court_ordered | municipal_restoration | chaser_civil
    conflict_flags:
      - employer_claim_exposure
      - landlord_contract_pressure
      - memory_bank_collateral_interest
      - family_request_for_fast_repair
  protected_scope:
    trace_types:
      - threshold_receipt_conflict
      - home_core_route_fragment
      - room_sensor_sequence
      - care_routine_dependency
      - refusal_or_self_reference_phrase
      - medical_or_injury_context
    repair_boundary:
      allowed:
        - structural_safety_patch
        - power_isolation
        - water_fire_or_biohazard_mitigation
        - analog_photo_chain
      blocked:
        - speaker_replacement
        - wall_processor_reimage
        - home_core_route_cleanup
        - habit_graph_compaction
        - claim_adjustment_erasure
  integrity_capture:
    before_repair_hashes:
      - room_mesh_snapshot
      - local_speaker_watermark
      - door_sensor_sequence
      - home_core_repair_log_segment
      - claim_map_annotation
    reviewer_routes:
      - shion_level_trace_scan
      - ghost_court_evidence_hold
      - white_harbor_loss_review
      - chaser_internal_risk_packet
  override:
    override_actor: insurer | landlord_court | chaser_command | medical_habitability | family_consent
    override_reason_hash: scoped_text_or_audio_reason
    required_after_action_capture: true
```

## What It Can Do

- Prevent restoration software from treating a contested trace as ordinary
  damage while the freeze is active.
- Tell crews which repairs are safety-critical and which would alter evidence.
- Preserve a narrow before-repair packet without exposing the entire family
  archive.
- Attach forced repair, family consent, or habitability override to the same
  audit trail.
- Give Shion, Ghost Court, White Harbor, or Internal Risk Division a concrete
  target for later review.

## What It Cannot Do

- Prove that a Ghost exists.
- Restore overwritten traces after repair has destroyed their route context.
- Cancel insurance debt, rent exposure, or landlord deadlines.
- Stop emergency safety work when the home is physically dangerous.
- Prevent Memory Bank from pricing a preserved trace as continuity exposure.

## Field Nicknames

Restoration crews call it a `red tape strip`. Loss assessors call it a `repair
hold`. Families usually call it a `room freeze`. Memory Bank models call it
`unpriced continuity exposure`.

## Failure Modes

- A contractor performs a safety patch that also reimages the wall processor.
- An insurer narrows the protected scope until the most expensive trace falls
  outside review.
- A family signs fast-repair consent under displacement pressure.
- A landlord court accepts habitability override without reviewing Home Layer
  evidence risk.
- Black Zone offers a complete illegal copy because the lawful lock is too
  narrow to comfort the family.

## Countermeasures

- Split safety repairs from memory-affecting repairs in the work order.
- Require before-and-after hashes when any exception touches locked hardware.
- Route personhood-adjacent phrases to Ghost Court hold without exporting full
  domestic memory.
- Mark employer, landlord, and Memory Bank conflicts directly in the lock.
- Pair high-risk locks with analog photos and Shion-level trace-integrity scan.

## Story Use

- Gives Nikhil Rao a small technical object that can make him costly to his
  employer without making him a hero.
- Makes restoration crews and landlords active pressure points rather than
  background logistics.
- Lets a quiet apartment wall become the central evidence object in an early
  Season 1 case.
- Lets Memory Bank turn preservation itself into a financial signal.

## Consistency Notes

- Mechanism uses Home Core repair logs, Home Layer room meshes, speaker
  watermarks, sensor sequences, claim ledgers, landlord work orders, CHASER
  timestamps, court holds, and scoped hashes.
- No magic, supernatural powers, multiverse, time travel, or physics-breaking
  God Fragment effects.
- Distinct from Threshold Receipt Packet: threshold receipts document warning
  before entry; restoration evidence locks protect repair boundaries after
  stabilization.
- Distinct from Presence Integrity Packet: presence packets prove a witness
  event; restoration locks constrain repair and capture before/after evidence.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-07-18T13:02:41+08:00"
canon_promotion: false
related_candidates:
  - outputs/lore/20260718-130241-lore-entry-continuity-loss-freeze.md
  - outputs/character/20260718-090109-candidate-character-026-nikhil-rao.md
requires:
  - ConsistencyAgent review against existing packet and hold technologies
asset_tasks: blocked_until_promotion
```
