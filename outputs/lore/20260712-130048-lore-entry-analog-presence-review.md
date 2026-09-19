# Lore Entry: Analog Presence Review

## Candidate Canon Entry

Analog Presence Review is the civil requirement that a living witness must enter
or directly observe a Home Core environment before an essential care routine,
dependent-care authority, or personhood-adjacent refusal record can be
downgraded, deleted, transferred, or sold.

It exists because automated systems became too good at translating domestic
grief into clean categories. A Home Core may look like a billing problem from
Memory Bank, a subsidy error to an insurer, a probate conflict to a court, and a
threat surface to CHASER. Analog Presence Review forces one question back into
the room before the system acts:

Who will be harmed if the home goes quiet?

The review does not make a family member right, prove a Ghost exists, or cancel
debt. It only requires a scoped human witness before irreversible Home Layer
action.

## Historical Event

```yaml
2134:
  event: Analog Presence Review adopted by White Harbor districts
  summary: >
    After several Home Cores are remotely downgraded during care-status renewals,
    White Harbor requires a physical or high-integrity telepresence witness
    before essential routines, refusal records, or dependent-care edges can be
    erased in contested homes.
  consequence: >
    Memory Bank and insurers gain a slower but more defensible review path,
    Ghost Union frames the rule as proof that homes can testify, and Black Zone
    begins selling forged presence packets for families who cannot wait.
```

## Review Triggers

```yaml
analog_presence_review:
  triggers:
    - essential_care_routine_downgrade_pending
    - dependent_person_without_alternate_support
    - home_core_refusal_record_present
    - probate_divergence_seal_attached
    - memory_bank_sale_or_lien_before_witness_export
    - ghost_court_petition_or_white_harbor_intake_pending
  required_observations:
    - living_dependent_condition
    - active_care_routine_effect
    - home_core_response_to_authorized_names
    - refusal_behavior_context
    - emergency_contact_and_guardian_edges
    - privacy_boundary_exceptions
  permitted_forms:
    - licensed_white_harbor_visit
    - hospital_social_work_telepresence
    - chaser_civil_unit_observation
    - court_ordered_home_layer_witness_session
```

## Social Function

- Slows remote deletion when a Home Core routine is still keeping someone alive,
  stable, or legally visible.
- Gives poor families a narrow witness path before Memory Bank classifies care
  as collateral, comfort, or fraud.
- Gives White Harbor a way to preserve context without opening the full family
  archive.
- Gives CHASER a civil alternative before treating every contested Home Core as
  a threat case.
- Lets story scenes turn on a room, a bed, a medicine drawer, a child's route to
  school, or a dead voice reminder rather than abstract system logs.

## Failure Modes

- Witness capture: a licensed reviewer is paid to certify an empty or staged
  room.
- Privacy harm: a narrow observation expands into exposure of unrelated family
  memory.
- Delay injury: the system waits for a witness while a dependent person loses
  active care.
- False compassion: a routine is preserved because it looks moving, even though
  it is rewriting the living dependent's relationship graph.
- Forged presence: Black Zone sells recorded room packets that pass weak
  telepresence checks.

## Story Hooks

- Sofia Marin invokes Analog Presence Review when an automated downgrade would
  remove a Home Core routine before a dependent person can be physically seen.
- Eve refuses to sign a remote deletion because the archived voice changes
  tone when the witness enters the room.
- Shion proves the presence packet is forged by comparing door-sensor latency
  against Home Layer medication timing.
- Memory Bank argues the review is only procedural, then prices the delay as an
  estate cost.
- A Ghost Union advocate is right that the home should be witnessed, but wrong
  about whether the refusal behavior is selfhood.

## Consistency Notes

- Analog Presence Review is a civil procedure using licensed witnesses,
  telepresence integrity checks, Home Layer exports, court orders, medical
  records, and CHASER civil observation. It is not supernatural.
- Distinct from Care Status Renewal: renewal classifies care; presence review
  requires observation before irreversible action in contested cases.
- Distinct from Emergency Delay Window: delay pauses imminent dependent-care
  harm; presence review creates the witness condition needed before deletion,
  downgrade, transfer, or sale.
- Distinct from Home Core Probate Hold: probate hold freezes inheritance
  contradiction; presence review can apply outside probate whenever the home
  context itself may change the action.
- Story-facing prose should use Home Core, Home Layer, Memory Sea, Second
  Nervous System, 家园核心, 家园层, 记忆海, 第二神经系统.

## Pipeline State

```yaml
stage: candidate_output
agent: LoreAgent
created_at: "2026-07-12T13:00:48+08:00"
canon_promotion: false
related_candidates:
  - outputs/lore/20260627-130142-lore-entry-care-status-renewal.md
  - outputs/lore/20260630-130040-lore-entry-emergency-delay-window.md
  - outputs/lore/20260711-130136-lore-entry-home-core-probate-hold.md
  - outputs/character/20260630-090234-candidate-character-015-sofia-marin.md
requires:
  - TechnologyAgent entry for Presence Integrity Packet
  - FactionAgent impact on White Harbor, Memory Bank, CHASER, Ghost Union, Black Zone, and Atlas
  - ConsistencyAgent review against care-status, emergency delay, and probate mechanisms
timeline_update: suggested_if_promoted
asset_tasks: blocked_until_promotion
```
