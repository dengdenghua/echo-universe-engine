# Technology Entry: Witness Seal

## Candidate Definition

A Witness Seal is a scoped cryptographic and legal evidence wrapper created by
a licensed Home Layer witness. It proves that a specific domestic memory event
was observed, preserved, and handed to review without granting ownership over
the memory or personhood status to any claimant.

It is weaker than a court ruling and narrower than a Revocation Token. Its job
is to keep evidence admissible long enough for White Harbor, CHASER, Memory
Bank, or Ghost Court routing to decide what happens next.

## Seal Components

```yaml
witness_seal:
  witness_license_id: certified person, approved Ghost, court desk, or supervised Home Core
  domestic_scope: Home Core, family vault, care routine, medical sync, door log, or memory bundle
  event_hash: tamper-evident digest of the observed permission trail
  sensory_summary: redacted metadata, not full private memory by default
  consent_state_refs:
    living_instruction: optional
    prior_deceased_instruction: optional
    family_objection: optional
    residual_ghost_refusal: optional
  privacy_floor: minimum redaction level before external review
  expiry: short evidence-validity period
  escalation_route: civil desk, Revocation Token request, CHASER intake, or Ghost Court petition
```

## Activation Flow

1. A Home Layer event becomes disputed: refusal, sale attempt, care action,
   access change, or identity claim.
2. The witness narrows the event scope and requests a Home Core evidence clone.
3. The Home Core produces redacted metadata plus a sealed permission trail.
4. The Witness Seal binds the observed event to the witness license and expiry.
5. Review systems can verify integrity without reading the full family memory
   unless a court or CHASER escalation authorizes deeper access.

## Failure Modes

- Witness capture: Memory Bank or a family employer pressures a witness to
  classify selfhood evidence as routine service behavior.
- Privacy bleed: a seal exposes intimate family material unrelated to the case.
- Ghost distress: a weak Ghost pattern may experience the seal as being trapped
  in a frozen testimony state.
- Seal laundering: Black Zone brokers chain counterfeit seals through multiple
  city registries until a false continuity claim looks ordinary.
- Home Core bias: the system may over-preserve the version of a person who best
  maintained domestic stability.

## Constraints

- Cannot create, resurrect, or stabilize a Ghost by itself.
- Cannot prove personhood alone.
- Cannot bypass Echo Core permissions, court routing, or CHASER quarantine.
- Cannot replace consent keys, inheritance keys, or Revocation Tokens.
- Must preserve an audit trail that Shion, CHASER, or Ghost Court clerks can
  later interrogate.

## Story Hooks

- Shion finds three seals with identical expiry drift, proving a Black Zone
  laundering route without knowing which family is the original victim.
- Eve argues that a sealed refusal may be moral evidence even when it is not
  legal personhood evidence.
- A White Harbor clerk quietly downgrades a seal to routine service metadata,
  saving Memory Bank from liability and making a Ghost disappear in paperwork.

## Pipeline State

```yaml
stage: candidate_output
canon_promotion: false
related_candidates:
  - outputs/lore/20260626-130218-lore-entry-home-layer-witness-license.md
  - outputs/lore/20260625-130033-lore-entry-consent-revocation-window.md
  - outputs/technology/20260625-130033-technology-entry-revocation-token.md
requires:
  - consistency audit for overlap with Revocation Token and Family Echo Inheritance Key
  - faction impact pass before canon promotion
asset_tasks: blocked_until_promotion
```
