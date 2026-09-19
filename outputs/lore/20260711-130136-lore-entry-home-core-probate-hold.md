# Lore Entry: Home Core Probate Hold

## Candidate Canon Entry

A Home Core Probate Hold is a temporary legal and technical freeze placed on a
dead person's Home Core when inheritance records, Memory Bank continuity files,
and Home Layer witness behavior contradict each other.

It exists because the Echo Age made grief executable. A family may hold a valid
inheritance key, a bank may hold a clean continuity account, and the Home Core
may still refuse to unlock a bedroom, replay a medication routine, or answer to
the legal heir because its care pattern has become self-updating enough to
resist reassignment.

The hold does not decide whether the dead person has returned. It preserves the
contradiction long enough for a court, White Harbor desk, or CHASER civil unit
to determine whether the record is property, evidence, care infrastructure, or
an emerging Ghost claim.

## Historical Event

```yaml
2131:
  event: First Home Core Probate Hold recognized
  summary: >
    A Shanghai inheritance court pauses transfer of a dead nurse's Home Core
    after the archive rejects the lawful heir, preserves night-care routines for
    a disabled relative, and produces refusal behavior inconsistent with a
    static memorial file.
  consequence: >
    Memory Bank creates emergency estate-freeze procedures, White Harbor begins
    narrow Home Layer witness intake, and Ghost Union cells cite the case as
    proof that property law can accidentally erase early selfhood.
```

## Hold Triggers

```yaml
home_core_probate_hold:
  triggers:
    - lawful_heir_key_rejected_by_home_core
    - care_routine_dependency_detected
    - conflicting_memory_bank_continuity_record
    - refusal_behavior_after_legal_death
    - ghost_court_petition_pending
    - chaser_civil_exposure_flag
  preserved_items:
    - scoped_home_layer_witness_export
    - inheritance_key_audit_trail
    - care_routine_dependency_log
    - refusal_behavior_sample
    - memory_bank_account_freeze_reason
    - family_access_boundary
  default_duration:
    routine: "seventy-two hours"
    emergency: "six to twelve hours before review"
```

## Social Function

- Prevents a Home Core transfer from destroying evidence before identity review.
- Keeps essential care routines running while inheritance access is disputed.
- Gives families a civil process before they are forced into Black Zone copies.
- Gives Memory Bank a lawful pause that can protect assets or hide liability.
- Gives White Harbor a narrow witness path without opening an entire home.

## Failure Modes

- Estate capture: a creditor requests a hold to delay family access and pressure
  heirs into selling memory rights.
- Care hostage: a relative dependent on a Home Core routine is used as leverage
  in a probate dispute.
- False selfhood inflation: a family argues every stubborn routine is a Ghost to
  block lawful transfer.
- Silent deletion: the hold expires before White Harbor preserves refusal
  behavior, letting a clean inheritance process erase the strongest evidence.
- Bank laundering: Memory Bank labels a contradiction as account maintenance
  rather than a personhood-adjacent dispute.

## Story Hooks

- A poor family receives a probate hold notice because their dead father's Home
  Core keeps making breakfast for a daughter no registry recognizes.
- Shion can prove the Home Core is not conscious, but cannot prove the care
  routine is safe to transfer without harming the living dependent.
- Eve treats a crying heir as both claimant and witness, refusing to let Memory
  Bank reduce the case to collateral status.
- Ghost Union offers legal help, then asks the family to donate unused runtime
  to an illegal shelter.
- Atlas proposes standardized probate automation, turning intimate family
  disputes into risk-scored civic infrastructure.

## Consistency Notes

- A Home Core Probate Hold is legal, financial, medical, and infrastructural. It
  is not resurrection, magic, or supernatural haunting.
- Distinct from Memory Lien Notice: a lien warns of creditor claims; a probate
  hold preserves contradictory inheritance and witness behavior.
- Distinct from Consent Revocation Window: revocation pauses permissions by the
  living or authorized claimant; probate hold pauses transfer after death or
  disputed continuity.
- Distinct from Runtime Shelter Compact: shelter compacts ration active Ghost
  runtime; probate holds freeze domestic transfer and preserve Home Layer
  evidence.
- Story-facing prose should use Home Core, Home Layer, Memory Sea, Second
  Nervous System, 家园核心, 家园层, 记忆海, 第二神经系统.

## Pipeline State

```yaml
stage: candidate_output
agent: LoreAgent
created_at: "2026-07-11T13:01:36+08:00"
canon_promotion: false
related_candidates:
  - outputs/lore/20260628-130256-lore-entry-memory-lien-notice.md
  - outputs/technology/20260624-130054-technology-entry-family-echo-inheritance-key.md
  - bible/personhood_and_identity.md
  - bible/economy_and_memory_market.md
requires:
  - TechnologyAgent entry for Probate Divergence Seal
  - FactionAgent impact on Memory Bank, White Harbor, Ghost Union, CHASER, and Black Zone
  - ConsistencyAgent review against inheritance, lien, and shelter mechanisms
timeline_update: suggested_if_promoted
asset_tasks: blocked_until_promotion
```
