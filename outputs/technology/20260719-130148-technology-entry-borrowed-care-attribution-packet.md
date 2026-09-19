# Technology Entry: Borrowed Care Attribution Packet

## Candidate Definition

A Borrowed Care Attribution Packet is the scoped technical record created during
a Home Layer Mismatch Review. It maps which borrowed routines appeared, where
they likely came from, what immediate actions they affect, and which parts must
be protected from reset, containment, financial claim, or public exposure.

The packet is not a full memory export. It is a boundary object: enough
evidence to classify the mismatch without turning a stranger's home life into a
marketable archive.

## Format Sketch

```yaml
borrowed_care_attribution_packet:
  packet_identity:
    packet_id: signed_white_harbor_or_chaser_civil_reference
    created_at: audited_timestamp
    review_state: intake | source_mapping | access_pause | evidence_hold | claim_conflict | closed
  mismatch_holder:
    holder_type: living_person | Home Core | room_routine | civic_service_node
    holder_id_hash: scoped_identity_hash
    biological_or_civic_status: alive | digital_person | household_system | public_system
    harm_status: none_observed | access_disruption | medical_risk | containment_claim | unknown
  borrowed_routines:
    routine_types:
      - meal_preference
      - medication_reminder
      - school_or_pickup_habit
      - door_or_kitchen_sequence
      - grief_ritual
      - exit_phrase_or_refusal
    source_confidence:
      home_core_match: low | medium | high
      wake_anchor_overlap: absent | partial | strong
      post_bloom_reconciliation_route: absent | suspected | confirmed
      black_zone_or_forgery_signal: absent | suspected | confirmed
  affected_actions:
    pause_or_review:
      - domestic_access_denial
      - forced_home_core_reset
      - medication_route_change
      - custody_or_school_gate_decision
      - memory_bank_asset_notice
      - chaser_carrier_containment_label
    allowed:
      - manual_latch_witness
      - emergency_medical_override
      - scoped_hash_capture
      - consent_based_comfort_silence
  privacy_boundary:
    allowed_evidence:
      - routine_hash
      - source_home_confidence_band
      - affected_action_list
      - witness_phrase_excerpt
      - access_and_medical_risk_flag
    blocked_evidence:
      - full_household_archive
      - unrelated_child_or_partner_records
      - financial_history_unrelated_to_claim
      - complete_voice_model_export
  routing:
    review_targets:
      - white_harbor_mismatch_desk
      - ghost_court_if_personhood_adjacent
      - chaser_internal_risk_if_containment_used
      - memory_bank_claim_hold_if_asset_language_used
```

## What It Can Do

- Show that a mismatch holder is a surface of a distributed Home Layer routing
  error rather than the origin of the event.
- Preserve routine-level evidence before a reset deletes the route.
- Pause specific access, custody, medical, claim, or containment decisions
  while keeping ordinary life moving where possible.
- Give Shion a technical map of post-bloom reconciliation drift without
  exposing full family archives.
- Separate personhood-adjacent traces from ordinary benign echoes.

## What It Cannot Do

- Prove that borrowed care is consented, owned, or alive.
- Restore a person's original domestic profile by itself.
- Stop all CHASER containment if there is an active medical or safety hazard.
- Prevent Memory Bank from filing a claim notice; it can only force claim hold
  routing.
- Identify every source household when wake anchors overlap at city scale.

## Failure Modes

- Overbroad capture: frightened officials demand full domestic exports instead
  of scoped hashes.
- Underclassification: an adaptive exit phrase is dismissed as a benign echo and
  erased during reset.
- Claim laundering: Memory Bank frames the packet as proof of asset location
  before care status is reviewed.
- Carrier stigma: the packet follows a living person across school, market, and
  clinic systems as a risk label.
- Forged attribution: Black Zone sells fake source confidence bands to grieving
  families.

## Countermeasures

- Keep source mapping in confidence bands unless court review requires more.
- Separate immediate safety actions from access restoration, financial claim,
  and personhood review.
- Require a manual witness route when domestic access risk blocks a living
  resident from their own home.
- Route repeated refusal or exit phrases to Ghost Court without exporting the
  full source home.
- Attach CHASER containment language to Internal Risk review when no harm route
  is proven.

## Story Use

- Lets `Borrowed Morning` turn a breakfast stall into infrastructure evidence
  without making Suyin secretly powerful.
- Gives Shion the practical artifact she needs to prove the bleed is citywide.
- Gives Eve and Luna different stakes in the same packet: fear, care, refusal,
  and use are not the same classification.
- Lets Memory Bank become dangerous through one phrase: recoverable continuity
  asset.

## Consistency Notes

- Mechanism uses Home Core habit graphs, Home Layer reconciliation jobs, wake
  anchors, routine hashes, access logs, medical reminders, reset permissions,
  claim notices, and CHASER caution labels.
- No magic, supernatural power, multiverse, time travel, possession, destiny, or
  literal physics-breaking God Fragment effect.
- Distinct from Restoration Evidence Lock: restoration locks constrain
  post-incident repair; borrowed care packets classify cross-household routine
  bleed before reset, access restoration, containment, or asset claim.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-07-19T13:01:48+08:00"
canon_promotion: false
related_candidates:
  - outputs/lore/20260719-130148-lore-entry-home-layer-mismatch-review.md
  - outputs/story/20260718-180218-story-beat-borrowed-morning.md
requires:
  - ConsistencyAgent review against existing packet and hold technologies
asset_tasks: blocked_until_promotion
```
