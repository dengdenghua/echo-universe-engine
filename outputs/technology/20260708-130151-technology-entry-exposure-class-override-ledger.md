# Technology Entry: Exposure Class Override Ledger

## Candidate Canon Entry

The Exposure Class Override Ledger is the CHASER triage record that lets a
civil classification officer delay, downgrade, or contest a threat label during
personality contamination incidents.

It is not a compassion button and not a hidden superpower. It is a narrow,
auditable ledger attached to CHASER intake stations, Echo Core exposure logs,
Home Layer witness exports, hospital telemetry, Memory Bank continuity flags,
and field reports. Its value is speed with accountability: a human officer can
preserve ambiguity before CHASER Central compacts the case into emergency
command language.

## Format Sketch

```yaml
exposure_class_override_ledger:
  case_id: memory-storm-2147-intake
  officer_id: lian-zhou-or-equivalent
  current_class: E3_unstable_carrier
  requested_class: E2_residue_bearing
  override_type:
    - downgrade
    - delay_escalation
    - require_exit_criteria
    - preserve_raw_fields
  evidence_minimum:
    independent_systems_required: 2
    accepted_sources:
      - Echo Core exposure log
      - Home Layer witness export
      - hospital telemetry
      - Memory Bank continuity flag
      - field-team incident note
      - White Harbor rights notice
  protected_fields:
    - residue_drift
    - self_report_variation
    - consent_anchor_status
    - exit_criteria
    - supervisor_override_log
  automatic_risks:
    - misconduct_review
    - liability_attachment
    - Central_override
    - public_safety_escalation
```

## What It Can Do

- Delay threat conversion long enough for medical, technical, or rights review.
- Require explicit exit criteria before a welfare hold becomes practical
  detention.
- Preserve raw residue drift before emergency compaction smooths away the
  contradiction.
- Attach officer liability so mercy has a name, timestamp, and review trail.
- Give White Harbor, Ghost Court, or White Ghost Team a record to challenge if
  Central later escalates the case.

## What It Cannot Do

- Release a confirmed active vector or command threat by itself.
- Override CHASER Central after emergency command lock.
- Prove Ghost personhood, clear Zero, or explain Memory Storm.
- Inspect raw private memories without consent, warrant, or emergency medical
  order.
- Make contaminated evidence trustworthy if the inputs were forged or too
  broadly exported.

## Activation Conditions

```yaml
activation_condition:
  required:
    - active CHASER civil intake
    - authenticated triage station
    - officer credential with civil contamination authority
    - at least two independent evidence sources
    - entry before Central emergency classification lock
  optional_support:
    - White Ghost field note
    - White Harbor witness-rights notice
    - hospital emergency ethics tag
    - Home Core scope limitation hash
```

## Failure Modes

- Mercy failure: a downgraded E3 case propagates as E4 before review finishes.
- Fear failure: an E2 witness is upgraded to E4 because public panic makes
  ambiguity politically impossible.
- Billing pressure: Memory Bank continuity risk scores push the case toward a
  cleaner label before medical review.
- Data hunger: a Home Core is opened wider than the incident requires, harming a
  family in the name of evidence.
- Supervisor burial: a Central officer treats the override as procedural
  deviation and hides the raw contradiction under emergency confidence.

## Countermeasures

- Dual-hash raw fields with one copy outside the local CHASER bureau.
- Require a named exit criterion for E2 and E3 holds.
- Log every supervisor override separately from the original officer note.
- Scope Home Layer witness export to the disputed edge instead of the whole
  domestic record.
- Mark Memory Bank-derived risk scores as economic evidence, not medical or
  personhood truth.

## Story Use

- Gives Lian Zhou a concrete action in Episode 12: she can buy minutes, not
  save the city.
- Lets Eve, Shion, Kane, and Zero disagree over the same ledger without any one
  of them being obviously right.
- Makes hardliner pressure visible as interface state: a threat lock countdown,
  missing exit criteria, and an override note that can be buried.
- Keeps Memory Storm grounded in infrastructure synchronization, classification,
  permissions, and evidence preservation.
- Foreshadows White Ghost Mutiny because the same classification machinery can
  later be aimed at Zero.

## Consistency Notes

- Distinct from Civil Delay Token: that mechanism slows municipal harm; this
  records CHASER exposure-class contestation during contamination intake.
- Distinct from Witness Seal: that preserves testimony; this preserves the
  classification contradiction around the witness or carrier.
- Distinct from Care Status Classifier: that decides service dependency; this
  decides contamination risk and exit criteria.
- Distinct from Identity Gate Signature Injection: that seeds threat metadata
  into Atlas systems; this contests CHASER's response to possibly contaminated
  people.
- In technical canon, household AI core-derived fields may be referenced. In
  story-facing prose, use Home Core, Home Layer, Memory Sea, and Second Nervous
  System.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: 2026-07-08T13:01:51+08:00
canon_promotion: false
related_candidates:
  - outputs/lore/20260708-130151-lore-entry-civil-exposure-classification.md
  - outputs/character/20260708-090128-candidate-character-020-lian-zhou.md
  - outputs/story/20260704-180101-story-beat-memory-storm.md
  - technologies/ability_constraints.md
  - bible/chaser_organization.md
requires:
  - ConsistencyAgent review for overlap with Civil Delay Token, Witness Seal, and Care Status Classifier
  - RelationshipAgent update if Lian Zhou and Episode 12 Memory Storm are promoted
asset_tasks: blocked_until_promotion
```
