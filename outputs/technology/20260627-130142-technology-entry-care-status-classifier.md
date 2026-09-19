# Technology Entry: Care Status Classifier

## Candidate Definition

A Care Status Classifier is a civil, medical, and financial scoring system used
to determine whether a Home Core routine qualifies as essential continuity,
private comfort, medical support dependency, contested selfhood support, or
fraudulent service behavior.

It is not an intelligence by itself. It is a decision layer that reads Home Core
logs, medical dependencies, benefit records, family instructions, Memory Bank
contracts, and limited Ghost selfhood indicators, then produces a reviewable
classification.

## Classifier Inputs

```yaml
care_status_classifier:
  applicant:
    biological_life: living, deceased, assisted, or unknown
    legal_identity: active, disputed, dead, or reassigned
    benefit_context: veteran, eldercare, disability, child-care, grief-support, or private
  home_core_scope:
    routine_type: medication, mobility, voice reminder, security, assisted speech, archive access, or memory comfort
    dependency_score: low, medium, high, critical
    relationship_context: spouse, child, parent, care worker, approved Ghost, or court desk
  continuity_signals:
    upload_link: none, weak, active, disputed
    ghost_selfhood_indicators: refusal, fear of deletion, preference formation, relationship persistence
    witness_seal_ref: optional
    revocation_token_ref: optional
  risk_signals:
    vendor_update_hash: required
    procedural_memory_payload: none, suspected, confirmed
    memory_bank_contract_pressure: low, medium, high
    black_zone_laundering_score: low, medium, high
  decision:
    classification: essential_continuity, private_comfort, medical_support_dependency, contested_selfhood_support, or fraudulent_service_behavior
    expiry: renewal deadline
    appeal_route: White Harbor desk, civil court, CHASER intake, Ghost Court petition, or Memory Bank review
```

## Activation Flow

1. A family, benefits office, insurer, Home Core, or court desk requests renewal.
2. The classifier scopes only the relevant care routine instead of the whole
   identity.
3. Medical dependencies and Home Layer history are compared with benefit and
   contract records.
4. Vendor update hashes are checked for unauthorized procedural memory payloads.
5. The system issues a classification, expiry, and appeal route.
6. High-risk contradictions route to White Harbor, CHASER, or Ghost Court
   review before subsidy or access is removed.

## Constraints

- Cannot prove personhood alone.
- Cannot delete, merge, or stabilize a Ghost.
- Cannot convert a private memory into public evidence without review.
- Cannot override a recognized digital person's non-deletion protection.
- Cannot treat combat, police, or military procedure as care without a clean
  medical and consent chain.

## Failure Modes

- Model capture: Memory Bank scoring weights make paid products look more
  medically necessary than public support.
- Vendor smuggling: a rehabilitation provider hides procedural occupation code
  inside an ordinary care update.
- Category harm: a routine is technically private comfort but socially essential
  to a survivor's identity stability.
- Evidence starvation: the classifier downgrades a weak Ghost before a Home
  Layer witness can seal refusal behavior.
- Audit drift: city registries produce slightly different scores, giving Black
  Zone brokers a laundering corridor.

## Story Hooks

- Kane recognizes a combat routine because the classifier mislabeled it as
  tremor rehabilitation.
- Shion compares renewal hashes across districts and finds the same vendor
  signature in veteran, eldercare, and grief-support cases.
- Noah predicts that denying one subsidy will trigger three illegal memory sales
  before the appeal window opens.
- A Home Core refuses to submit a renewal because the classifier would expose a
  family secret unrelated to the actual care need.

## Pipeline State

```yaml
stage: candidate_output
canon_promotion: false
related_candidates:
  - outputs/lore/20260627-130142-lore-entry-care-status-renewal.md
  - outputs/story/20260626-180234-story-beat-ten-seconds.md
  - outputs/technology/20260626-130218-technology-entry-witness-seal.md
requires:
  - consistency audit for overlap with Revocation Token and Witness Seal
  - faction impact pass before promotion
asset_tasks: blocked_until_promotion
```
