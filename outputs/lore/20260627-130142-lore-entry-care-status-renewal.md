# Lore Entry: Care Status Renewal

## Candidate Canon Entry

Care Status Renewal is the recurring civil review that decides whether a Home
Core care routine remains an essential continuity service, a private family
comfort, a medical support dependency, or a billable memory product.

The process began as eldercare administration. By the Echo Age, it became one
of the quietest forms of identity power: a clerk, insurer, or automated review
desk can decide whether a dead spouse's voice reminders are care, whether a
disabled veteran's apartment remains medically safe, and whether a weak Ghost's
refusal is evidence or noise.

## Timeline Placement

- 2038: Early city health systems subsidize domestic reminder cores for
  medication, fall detection, and family care coordination.
- 2096: Atlas-aligned insurers introduce continuity scoring for long-term Home
  Core care dependencies.
- 2139: White Harbor opens appeal desks after repeated care-status denials lead
  to preventable deaths and Ghost Court petitions.
- 2147: White Ghost Team treats manipulated care-status renewals as a recurring
  route for memory laundering, procedural occupation, and Home Layer coercion.

## Review Categories

```yaml
care_status:
  essential_continuity:
    meaning: required for medical safety, identity stability, or recognized care duty
    protection: subsidy cannot lapse without human or court review
  private_comfort:
    meaning: emotionally meaningful but not recognized as necessary support
    protection: weak; often pushed into paid family archive products
  medical_support_dependency:
    meaning: tied to implants, medication routines, rehabilitation, or assisted living
    protection: strong if biological life is clearly at risk
  contested_selfhood_support:
    meaning: routine may be sustaining an emerging Ghost pattern or refusal behavior
    protection: routes toward Home Layer witness, Revocation Token, or Ghost Court review
  fraudulent_service_behavior:
    meaning: suspected laundering, forged routines, or improper subsidy claim
    protection: account freeze and possible CHASER intake
```

## Social Function

- Keeps aging, disabled, grieving, and low-income families connected to Home
  Core support without making every domestic care action a full identity case.
- Gives Memory Bank and insurers a legal place to reclassify care into products,
  defaults, collateral, or fraud.
- Gives White Harbor a narrow appeal route before families are forced into the
  Black Zone.
- Gives CHASER an early warning signal when a care-status system carries combat
  routines, forged memories, or illegal continuity payloads.

## Failure Modes

- Subsidy cliff: a family loses support because a routine is reclassified from
  essential continuity to private comfort.
- Vendor insertion: rehabilitation updates or benefit renewals carry hidden
  procedural memory packages.
- Grief monetization: Memory Bank sells paid extensions for routines that were
  previously public care.
- Ghost erasure by category: a weak Ghost's refusal is marked as service noise
  before any personhood review can begin.
- False protection: a forged essential-continuity label shields a laundering
  route from ordinary audit.

## Story Hooks

- Tomas Vale's spouse remains stable only while their apartment holds essential
  continuity status, making a benefits hearing more dangerous than a firefight.
- A White Harbor clerk discovers that hundreds of denied renewals share the same
  Memory Bank scoring model.
- Eve argues that calling a routine "private comfort" can still kill a person if
  the Memory Sea is the only place that person remains coherent.
- Shion traces procedural occupation to a rehabilitation vendor update that
  entered through care-status renewal rather than a combat system.

## Consistency Notes

- Care Status Renewal is civil infrastructure, not supernatural judgment.
- It does not decide whether a Ghost is the original person; it decides whether
  a care routine remains funded, protected, reviewable, or frozen.
- It should remain distinct from Consent Revocation Windows, which pause
  disputed actions, and Home Layer Witness Licenses, which certify evidence.
- Use story-facing terms in prose: Home Core, Home Layer, Memory Sea, Second
  Nervous System, 家园核心, 家园层, 记忆海, 第二神经系统.

## Pipeline State

```yaml
stage: candidate_output
canon_promotion: false
fills_gap_from:
  - outputs/consistency/20260626-180234-canon-audit-ten-seconds.md
related_candidates:
  - outputs/story/20260626-180234-story-beat-ten-seconds.md
  - outputs/lore/20260625-130033-lore-entry-consent-revocation-window.md
  - outputs/lore/20260626-130218-lore-entry-home-layer-witness-license.md
requires:
  - ConsistencyAgent review against personhood_and_identity.md
  - TechnologyAgent definition of care-status classifier and audit trace
  - FactionAgent impact pass for White Harbor, Memory Bank, CHASER, and Ghost Union
asset_tasks: blocked_until_promotion
```
