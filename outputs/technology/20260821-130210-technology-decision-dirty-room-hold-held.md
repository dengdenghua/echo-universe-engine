# Technology Decision (Candidate): Dirty Room Hold Held

Status: candidate — held

Agent: TechnologyAgent (with LoreAgent / FactionAgent support)

Created at: 2026-08-21T13:02:10+08:00

## Decision

Dirty Room Hold is recorded as a candidate municipal procedure, not promoted to
`technologies/`.

```yaml
technology_status:
  name: Dirty Room Hold
  status: candidate (held)
  promoted: false
  hold_reason: >
    Selene Arif provides one strong case route, but the mechanism has not yet
    recurred beyond Apartment 6C and must remain a narrow reset exception
    rather than a general anti-erasure tool.
  promotion_gate: >
    Requires one story validation plus either a second municipal reset case or
    a Season 1 packaging decision that makes White Harbor Civic Reset Service a
    recurring contractor layer.
```

## Mechanism Fields

```yaml
dirty_room_hold:
  entry_point: White Harbor municipal reset supervisor badge
  duration_limit: eight hours unless civil court or CHASER extends evidence scope
  accepted_exception_classes:
    - live_care_dependency
    - unresolved_home_core_disconnect
    - contamination_mismatch
    - missing_person_property
    - chaser_evidence_line
  visible_records:
    - reset_order_id
    - landlord_release_clock
    - air_scrub_clock
    - room_inventory_hash
    - Home_Core_latch_telemetry
    - Home_Layer_disconnect_notice
    - hold_receipt_id
  protected_scope:
    - room_state
    - dependency_route_hash
    - contamination status
    - limited evidence marker
  blocked_scope:
    - sealed_family_content
    - full_neighbor_medical_record
    - estate-wide archive export
    - persistent Home Core copy
    - Ghost personhood certification
  contradiction_flags:
    - clean_room_false_absence
    - live_care_privacy_collision
    - estate_capture_risk
    - discard_chain_leakage
    - worker_liability_shift
```

## Separation From Existing Candidates

```yaml
not_quiet_log: >
  Quiet Log hides unpaid care minutes from a reserve model. Dirty Room Hold
  preserves a physical room state after eviction. It exposes rather than hides
  evidence.
not_residency_mirror: >
  Residency Mirror is a Ghost's permitted multi-session render inside care-plan
  compute. Dirty Room Hold concerns a room that may contain only automation,
  care dependency, evidence, or a possible witness.
not_home_core_probate_hold: >
  Probate Hold concerns inheritance transfer and identity custody. Dirty Room
  Hold concerns municipal reset timing and evidence preservation after the
  legal exit process has already moved on.
not_continuity_loss_freeze: >
  Continuity Loss Freeze preserves disputed continuity. Dirty Room Hold
  preserves scene state; it cannot freeze identity.
```

## Failure Modes

- The hold receipt becomes a Memory Bank estate-freeze trigger.
- The dependency route hash exposes enough medical timing to harm the living
  neighbor.
- The reset contractor treats exception use as worker fault and disciplines the
  crew.
- A landlord uses contamination language to force earlier entry.
- CHASER over-scopes the line and turns a room-state hold into broad seizure.
- Raven's discard-route audit reveals that prior clean rooms fed Black Zone
  grief resale, making Selene's crew witnesses and suspects.

## Hard Rule Check

- No magic, supernatural powers, multiverse, or time travel.
- The hold operates through municipal orders, Home Core latch telemetry, Home
  Layer disconnect notices, court/landlord timing, CHASER scope, and sanitation
  liability.
- It cannot create care, preserve a mind by itself, reverse a reset, or prove
  personhood.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-08-21T13:02:10+08:00"
canon_promotion: false
related_lore: outputs/lore/20260821-130210-lore-entry-dirty-room-hold.md
related_faction: outputs/faction/20260821-130210-faction-dossier-white-harbor-civic-reset-service.md
related_character: outputs/character/20260821-090055-candidate-character-046-selene-arif.md
requires_consistency_review: true
asset_task: outputs/assets/20260821-130210-asset-task-prop-dirty-room-hold-receipt.yaml
```
