# Lore Entry: Wake-Gait Authorship Review

## Candidate Canon Entry

Wake-Gait Authorship Review is a Dream Network medical procedure for contested
rehabilitation cases where a recovering body moves, improves, or refuses in ways
that cannot be cleanly attributed to the living patient.

It exists because medical recovery became harder to judge after the Home Layer
began preserving practical care. A spouse's Home Core routine may know how a
patient turns when afraid. A clinic gait mirror may replay a successful step
until the body relearns it. A prosthetic patch may smooth tremor without asking
whether the person wanted that motion. A frightened Ghost may help because love
was the only job it still understood.

The review does not ask whether a movement was useful. It asks who authored it,
who could stop it, and whether help remained revocable.

## Public Rule

```yaml
wake_gait_authorship_review:
  public_name: Wake-Gait Authorship Review
  clinical_shorthand: soft-lock review
  status: candidate
  jurisdiction: Dream Network licensed rehabilitation wards and White Harbor tribunals
  trigger: >
    A patient, clinician, family proxy, Ghost claimant, prosthetic safety board,
    or CHASER body-occupation desk disputes the authorship of therapeutic
    movement.
  core_question: >
    Did the living patient author, accept, refuse, or merely endure the motion?
```

## Required Evidence

- Patient testimony while awake, including hesitation and refusal phrases.
- Clinic gait mirror logs showing repeated therapeutic movement patterns.
- Echo Core motor telemetry showing patient-authored signal, assisted signal,
  fatigue drift, or foreign procedural load.
- Home Core care residue that may have taught, nudged, or corrected movement.
- Prosthetic firmware hashes and patch provenance.
- Dream Network room-state logs, including soft-lock timing and exit rights.
- Analog bedside witness notes when the room data looks too clean.

## Social Function

- Gives recovering patients a way to contest being celebrated as healed before
  they feel present inside their own movement.
- Gives Dream Network clinicians a bounded alternative to deleting every
  disputed motor companion as occupation malware.
- Gives hospitals an evidence path that is harder to reduce to outcome metrics.
- Gives Ghost Court and White Harbor tribunals a limited medical record without
  turning therapy rooms into personhood courts.
- Gives Season 1 and early Season 2 a body-agency pressure point distinct from
  civic access, debt, registry, or inheritance disputes.

## Failure Modes

- Outcome capture: the hospital treats improved motion as consent because
  insurers reward recovery metrics.
- Gentle occupation: a care routine or Ghost companion prevents harm so often
  that the patient loses the practical ability to refuse.
- Shame misread: the review mistakes embarrassment, speech difficulty, or
  fatigue for permission.
- Prosthetic laundering: a Black Zone patch mimics patient intent by copying
  gait mirror signatures from legitimate therapy sessions.
- Soft-lock harm: pausing a room preserves evidence but interrupts therapy,
  worsens recovery, or traps a digital participant without clean compute exit.
- Family proxy pressure: relatives ask the room to privilege the version of the
  patient who moves more conveniently.

## Story Hooks

- Ema Sayegh freezes a celebrated recovery after a patient's hand signs a
  discharge form while the patient whispers a refusal phrase.
- Mira Voss proves the limb moved under mixed authorship, but the hospital
  argues mixed authorship is normal rehabilitation.
- Luna can enter only after both living and digital wake anchors are verified;
  Dream Dive remains neural-interface traversal through Dream Network systems.
- Kane recognizes the logic from Combat Download and is forced to distinguish
  borrowed survival skill from unwanted therapeutic control.
- A disputed motor companion calls itself a spouse's care habit, while the
  firmware route points toward Black Zone prosthetic brokers.

## Boundaries

- Wake-Gait Authorship Review is not Ghost Court. It can preserve evidence for
  personhood or occupation cases, but it cannot grant legal identity.
- It is not Reciprocal Wake Session. Reciprocal waking governs shared projection
  exit rights; wake-gait review governs bodily movement authorship during
  recovery.
- It is not the `Ten Seconds` combat occupation beat. The conflict is slow,
  clinical, and ambiguous because assistance may be medically beneficial.
- It is not Home Layer Mismatch Review. The contested surface is bodily agency,
  not household access or borrowed domestic habit bleed.

## Pipeline State

```yaml
stage: candidate_output
agent: LoreAgent
created_at: "2026-07-21T13:02:04+08:00"
canon_promotion: false
related_candidates:
  - outputs/character/20260721-090154-candidate-character-029-ema-sayegh.md
  - outputs/technology/20260721-130204-technology-entry-motor-authorship-trace-packet.md
  - outputs/faction/20260721-130204-faction-impact-wake-gait-authorship-review.md
requires:
  - RelationshipAgent review for Ema, Luna, Mira Voss, Kane, Dream Network, Black Zone prosthetic brokers, and Ghost Companion R-17
  - StoryAgent route before promotion
timeline_update: suggested_if_promoted
asset_tasks: blocked_until_story_route
```
