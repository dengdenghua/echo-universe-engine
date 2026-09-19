# Technology Entry: Care-Reserve Sufficiency Packet

## Candidate Canon Entry

Care-Reserve Sufficiency Packet is the review bundle used to prove whether a
Neutral Care Escrow hold can continue without opening a sealed Home Core
afterword, exhausting the hospice worker chain, or underfunding a weak
claimant-adjacent trace.

It extends Non-Opening Transfer Proof. Transfer proof shows that the sealed
case can move without content export. Care-reserve sufficiency shows whether
the receiving institution can keep holding it without converting privacy into
abandonment or unpaid labor.

```yaml
technology:
  name: Care-Reserve Sufficiency Packet
  category: hospice escrow reserve review / no-copy care accounting / claimant anti-starvation
  status: candidate
  related_lore: Reserve Sufficiency Hearing
  primary_users:
    - Free Orbital Mutual Hospice Network reserve clerks
    - route insurer conduct desks
    - Ghost Union reserve advocates
    - Memory Bank release-cost reviewers
    - CHASER physical-chain observers
    - Shion-style Home Layer forensic witnesses
  prohibited_use: >
    Cannot reveal phrase text, open unrelated Home Layer rooms, certify Ghost
    personhood, force a living recipient to accept export, erase worker
    liability, create compute from nothing, or override a named safety event.
```

## Packet Fields

```yaml
care_reserve_sufficiency_packet:
  packet_id: reserve hearing id plus hospice escrow key plus review timestamp
  sealed_case:
    - Home_Core_afterword_hash
    - non_opening_transfer_proof_id
    - phrase_export_state
    - claimant_uncertainty_flag
    - no_copy_receipt_id
  reserve_state:
    - current_compute_reserve
    - pledged_compute_floor
    - oxygen_allocation_minutes
    - storage_meter_floor
    - anti_starvation_margin
    - degradation_notice_threshold
  labor_state:
    - worker_roster_hash
    - meal_window_exception_count
    - unpaid_hold_minutes
    - bond_exposure_amount
    - conduct_review_state
  institution_state:
    - Memory_Bank_release_cost_position
    - route_insurer_coverage_position
    - Ghost_Union_reserve_motion
    - CHASER_observation_boundary
    - Mars_boundary_notice_state
  output_limits:
    - reserve_sufficient
    - reserve_insufficient_but_private
    - reserve_insufficient_with_named_safety_event
    - upstream_cost_displacement_flag
```

## Operations

- Reserve accounting: calculates whether compute, oxygen, storage, and worker
  coverage satisfy the pledged care floor.
- Anti-starvation margin: flags risk to weak claimant-adjacent traces without
  granting content access.
- Labor coercion flag: records when custody depends on unpaid meal windows,
  suspended licenses, or worker bond exposure.
- Cost-displacement trace: shows when Memory Bank or route insurers moved cost
  outward after approving release in principle.
- Observer boundary: keeps CHASER's view limited to physical-chain and named
  safety-event status.

## Failure Modes

- Privacy-as-neglect: sealed content remains protected while the trace loses
  compute support.
- Audit laundering: institutions call the reserve packet sufficient because
  unpaid worker time is counted as available capacity.
- Emergency inflation: a low reserve meter is reclassified as safety danger to
  force content export.
- Bond capture: a hospice worker signs care custody and becomes the cheapest
  place to assign failure.
- Claimant overreach: reserve advocacy is used to pressure a living recipient
  into opening family material.

## Story Limitations

Shion can validate packet integrity and expose what the math hides. Eve can
show when consent is being bent by cost pressure. Zero can keep CHASER inside
its observation boundary. None of them can fund the reserve, settle worker
bonds, make Ilya Marr's afterword a confirmed Ghost, or erase Nara Marr's
refusal.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-08-13T13:02:15+08:00"
canon_promotion: false
related_lore: outputs/lore/20260813-130215-lore-entry-reserve-sufficiency-hearing.md
related_technology: outputs/technology/20260812-130121-technology-entry-non-opening-transfer-proof.md
related_character: outputs/character/20260812-090232-candidate-character-041-sana-velez.md
requires_consistency_review: true
```
