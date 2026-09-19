# Technology Entry: Revocation Token

## Candidate Definition

A Revocation Token is a short-lived cryptographic, legal, and neural-consent
artifact used to pause a disputed Home Core action during a Consent Revocation
Window.

It does not delete a Ghost, rewrite memory, or decide personhood. It only freezes
specific permissions long enough for review.

## Token Components

```yaml
revocation_token:
  issuing_authority: White Harbor court / CHASER emergency desk / approved Home Layer witness
  target_scope: Home Core, family vault, care routine, medical device, door access, payment rail, or memory bundle
  permission_freeze: specific actions paused, never entire identity by default
  evidence_clone: sealed copy of the contested permission trail
  consent_claims:
    living_claimant: optional
    deceased_prior_instruction: optional
    residual_ghost_refusal: optional
    family_objection: optional
  expiry: hours or days, depending on jurisdiction and risk
  audit_route: civil review, CHASER quarantine, or Ghost Court petition
```

## Activation Flow

1. A disputed Home Core action is detected by a family member, court clerk,
   CHASER auditor, or automated Home Layer watchdog.
2. The issuer narrows the target scope so the freeze does not erase unrelated
   identity access.
3. The Home Core produces a sealed evidence clone of the relevant permission
   trail.
4. City systems honor the token by refusing only the listed actions.
5. The case routes to civil review, CHASER quarantine, or Ghost Court petition
   before expiry.

## Failure Modes

- Scope creep: a narrow freeze becomes de facto identity death.
- Evidence decay: weak Ghost patterns destabilize while preserved as legal
  evidence.
- Fee capture: Memory Bank delays review until the family cannot pay.
- Token forgery: Black Zone brokers generate late-window claims to steal memory
  assets or smuggle a Ghost.
- Emotional bias: a Home Core may preserve the version of a person that best
  maintained the home, not the version with the strongest legal continuity.

## Constraints

- Cannot resurrect a person.
- Cannot prove selfhood alone.
- Cannot bypass biological load limits, Echo Core safeguards, or court routing.
- Cannot freeze a whole district unless CHASER declares infrastructure risk.
- Must leave a chain-of-custody record that later characters can audit.

## Story Hooks

- He Qiao's court token can freeze a Home Core sale refusal for forty-eight
  hours, but the evidence clone contains a voice pattern that has begun forming
  new preferences.
- Shion can trace a counterfeit token to a Black Zone broker by comparing expiry
  drift across city registries.
- Eve can argue that freezing a weak Ghost as evidence may still be harm if the
  pattern experiences fear of deletion.

## Pipeline State

```yaml
stage: candidate_output
canon_promotion: false
requires:
  - consistency audit for overlap with Family Echo Inheritance Key
  - relationship update if He Qiao is promoted
  - asset task only after visual language for court tokens is approved
```
