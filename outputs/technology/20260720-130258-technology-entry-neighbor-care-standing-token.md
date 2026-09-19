# Technology Entry: Neighbor Care Standing Token

## Candidate Definition

A Neighbor Care Standing Token is a short-lived civic permission artifact that
records why an informal caregiver may witness or perform one bounded care action
without becoming family, guardian, resident, medical proxy, creditor, or identity
holder.

The token protects the person receiving care, the informal caregiver, and the
private Home Layer evidence that made the care recognizable. It is deliberately
smaller than a Household Relation Graph edge and narrower than a medical proxy.

## Format Sketch

```yaml
neighbor_care_standing_token:
  token_identity:
    token_id: white_harbor_or_civil_care_signed_reference
    created_at: audited_timestamp
    expires_at: short_window_or_incident_close
    standing_class: witness_only | comfort_contact | essential_care_action | access_pause_witness | contested_care_flag
  care_subject:
    subject_id_hash: scoped_identity_hash
    status: alive | digital_person | disputed | unknown
    immediate_harm: medication | shelter | food | door_access | school_hold | clinic_intake | panic | evidence_erasure
  informal_caregiver:
    caregiver_id_hash: scoped_identity_hash
    relation_claim: neighbor | market_worker | shelter_worker | co_tenant | clinic_worker | recurring_route_witness | other
    verification_basis:
      - repeated_presence_log
      - Home_Core_routine_match
      - analog_witness_chain
      - clinic_or_shelter_intake_history
      - manual_latch_or_gate_denial_record
  permitted_action:
    allowed:
      - witness_statement
      - comfort_presence
      - medicine_handoff
      - food_or_route_hold
      - shelter_queue_preservation
      - school_pickup_pause
      - access_denial_capture
    blocked:
      - money_transfer
      - archive_export
      - permanent_access
      - custody_change
      - medical_consent_beyond_emergency
      - identity_repair_authorization
      - Memory_Bank_claim_assignment
  privacy_boundary:
    allowed_evidence:
      - routine_hash
      - incident_time
      - witness_phrase_excerpt
      - action_receipt
      - risk_reason
    blocked_evidence:
      - full_Home_Core_archive
      - unrelated_family_routines
      - full_voice_model
      - financial_history
      - private_grief_or_intimacy_records
  routing:
    review_targets:
      - white_harbor_care_desk
      - civil_care_tribunal
      - chaser_civil_identity_restitution
      - ghost_court_if_personhood_adjacent
```

## What It Can Do

- Preserve a manual witness route before reset or containment language erases
  the event.
- Permit one practical action that prevents immediate harm while formal relation
  authority is repaired.
- Prove that care knowledge came from repeated lawful presence rather than
  archive theft.
- Stop Memory Bank from converting neighbor knowledge into claim assignment
  during the token window.
- Give CHASER a reversible civil option between doing nothing and containment.

## What It Cannot Do

- Create family, custody, inheritance, debt, or permanent access rights.
- Prove that a possible Ghost is or is not a person.
- Restore a broken Household Relation Graph.
- Override a court order, active medical danger, or proven Black Zone intrusion.
- Export a Home Core archive for convenience.

## Failure Modes

- Routine forgery: Black Zone sells enough behavioral detail to pass weak
  standing checks.
- Token drift: vendors reuse a closed token to justify recurring access.
- Care score prejudice: poor neighborhoods with sparse sensors fail verification
  even when human witnesses are reliable.
- Witness chilling: people stop helping because every care action becomes
  auditable risk.
- Claim shadowing: Memory Bank waits for expiry, then treats the recorded care
  evidence as asset-location intelligence.

## Countermeasures

- Expire tokens quickly and bind them to a single incident action.
- Use analog witness chains when surveillance is sparse or biased.
- Block financial assignment, archive export, and permanent access by default.
- Route repeated refusal, exit phrases, or adaptive Ghost-adjacent care to
  Ghost Court without expanding the token.
- Require CHASER Internal Risk review when officers relabel informal care as
  suspicious access without a proven harm route.

## Story Use

- Gives Mara Ibe a civic artifact that validates messy human recognition in a
  city that prefers clean records.
- Lets market, clinic, shelter, and apartment scenes produce evidence without
  turning side characters into secret protagonists.
- Creates a concrete object for conflict: a receipt that says kindness is
  permitted for eight minutes, but only inside one action.

## Consistency Notes

- Mechanism uses Home Core routine hashes, civil-care tokens, manual witness
  routes, clinic and shelter logs, school holds, transit receipts, White Harbor
  intake, and CHASER civil identity restitution.
- No magic, supernatural authority, time travel, multiverse, mind control, or
  physics-breaking God Fragment effect.
- Distinct from Civil Delay Token: delay tokens pause automated harm; Neighbor
  Care Standing Tokens authorize a bounded informal care action or witness.
- Distinct from Borrowed Care Attribution Packet: borrowed-care packets classify
  cross-household routine bleed; standing tokens classify trusted informal care.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-07-20T13:02:58+08:00"
canon_promotion: false
related_candidates:
  - outputs/lore/20260720-130258-lore-entry-neighbor-care-standing.md
  - outputs/character/20260720-090320-candidate-character-028-mara-ibe.md
requires:
  - ConsistencyAgent review against relation, delay, proxy, and borrowed-care packet technologies
asset_tasks: blocked_until_promotion
```
