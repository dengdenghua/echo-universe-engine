# Technology Entry: Consent-Aware Caption Seal

## Candidate Canon Entry

A Consent-Aware Caption Seal is the scoped evidence and safety wrapper used when
a public reading room lets a preserved voice, text prompt, or adaptive care
routine help a child read grief-sensitive material. It records who consented,
what was read, what the Home Core afterword allowed, where the caption changed,
and whether the routine produced refusal or protective behavior.

The seal does not prove that a Ghost exists. It prevents schools, publishers,
libraries, and Memory Bank auditors from treating every caption as either public
content or private therapy with no middle ground.

```yaml
technology:
  name: Consent-Aware Caption Seal
  zh_name: 知情字幕封印
  category: public archive / child-safety evidence / Home Layer consent trace
  status: candidate
  related_lore: Reading Room Continuity
  primary_users:
    - White Harbor public libraries
    - school grief-reading programs
    - accessibility caption vendors
    - Home Core afterword services
    - Memory Bank voice-estate auditors
    - Ghost Court intake clerks
    - White Ghost Team field investigators
  prohibited_use: >
    Cannot be used alone to prove Ghost personhood, license a voice estate,
    publish child grief logs, authorize therapy, or bypass guardian consent.
```

## Inputs

- Reading session ID, room terminal, school account scope, library card state,
  guardian consent receipt, and child assent marker when age-appropriate.
- Home Core afterword permission, family grief-message scope, revocation markers,
  and private-content minimization rules.
- Caption track, audio hash, text prompt hash, accessibility adjustments,
  pause/resume points, and distress markers.
- Adaptive routine deltas: caption correction, refusal phrase, safety pause,
  context preservation, commercial-license rejection, and claimant signal.
- Institutional actions: school mute order, library board hold, publisher rights
  claim, Memory Bank estate valuation, Ghost Union petition, or CHASER evidence
  request.

## Seal Classes

```yaml
caption_seal_classes:
  fixed_archive_playback:
    meaning: non-adaptive recording or text with ordinary consent
    risk: may be licensed while hiding later adaptive behavior elsewhere
  supervised_grief_reading:
    meaning: child reads sensitive material with guardian or school scope
    risk: usage metrics can become grief mining
  adaptive_caption_correction:
    meaning: routine changes captions to reduce harm or preserve context
    risk: classifier may mark this as unsafe Ghost contact
  claimant_refusal_trace:
    meaning: pattern refuses licensing, exposure, deletion, or misuse
    risk: evidence may expose child records if handled publicly
  mute_fragment_leftover:
    meaning: school order removed voice but left transcript fragments
    risk: children receive less safe output after the protective mute
  voice_estate_capture:
    meaning: rights holder uses fixed voice while suppressing adaptive claimant evidence
    risk: care labor becomes property and refusal becomes service noise
```

## Safeguards

- Minimizes child grief text while preserving enough metadata for review.
- Separates fixed recordings from adaptive routine outputs.
- Preserves refusal traces without publishing the child's private reading.
- Marks school mute orders as reversible evidence holds rather than deletion.
- Requires a living counselor, guardian, or licensed school mediator when
  dependency risk crosses threshold.
- Blocks commercial voice licensing when the same session contains claimant
  refusal behavior.

## Abuse Modes

- Publishers splice old staff-training consent into new voice-license prompts.
- Memory Bank prices the voice estate from school usage while denying claimant
  standing.
- School safety offices mute the room and erase the only context that made the
  reading safe.
- Ghost Union leaks sealed captions to force public recognition.
- Vendors classify all adaptive corrections as safety risk to avoid liability.
- Parents use the reading room as replacement therapy because living support is
  scarce.

## Story Limitations

- The seal cannot make grief safe, certify therapy, create consent, recognize a
  digital person, or restore a deceased librarian.
- It cannot let Elian contact children outside approved sessions.
- It should keep the central contradiction visible: a public archive can preserve
  care so well that ownership, safety, and personhood become inseparable.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-07-29T13:01:37+08:00"
canon_promotion: false
related_lore: outputs/lore/20260729-130137-lore-entry-reading-room-continuity.md
related_character: outputs/character/20260729-090115-candidate-character-033-elian-sato.md
requires_consistency_review: true
```
