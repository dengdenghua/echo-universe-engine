# Lore Entry: Civil Exposure Classification

## Candidate Canon Entry

Civil Exposure Classification is the CHASER civil-triage system used when a
person, Home Core, clinic, shelter, or public service route may be carrying
personality contamination without yet meeting the threshold for threat detention.

It exists because Memory Storm is not a simple attack. In Episode 12, civilians
inherit strangers' skills, phobias, grief, family habits, emergency routines,
and fragments of identity residue through coordinated Home Layer behavior. Some
carriers are dangerous. Some are witnesses. Some are patients. Some are the only
evidence that an emerging Ghost pattern was self-updating before the city tried
to erase it.

Civil Exposure Classification is CHASER's attempt to keep those categories from
collapsing into one word: threat.

## Timeline Placement

- 2126: White Harbor intake desks begin separating Ghost-adjacent witnesses from
  active hostile carriers after several early quarantine cases erase usable
  testimony.
- 2134: CHASER Central standardizes exposure classes for personality
  contamination, Home Core residue spillover, and Echo Core skill-transfer
  incidents.
- 2141: Memory Bank contracts begin using exposure class labels to price
  continuity insurance, making civil triage economically consequential.
- 2146: CHASER hardliners argue that exit criteria slow containment during
  multi-city incidents.
- 2147: Memory Storm makes the system politically explosive when hardliners
  demand district quarantine while civil officers such as Lian Zhou insist that
  classifying victims, witnesses, and carriers separately is the only way to
  preserve evidence and personhood claims.

## Classification Bands

```yaml
civil_exposure_classification:
  E0_clear:
    meaning: "ordinary witness; no active contamination indicators"
    default_action: "statement, rights notice, no movement restriction"
  E1_contact:
    meaning: "exposed to a contaminated person, Home Core, or public route"
    default_action: "medical monitoring, limited Home Layer export, voluntary check-in"
  E2_residue_bearing:
    meaning: "carries foreign memory, habit, fear, or grief residue without agency loss"
    default_action: "witness protection, consent anchor, temporary service safeguards"
  E3_unstable_carrier:
    meaning: "foreign pattern changes speech, skill, behavior, or identity continuity"
    default_action: "welfare hold, technical review, exit criteria required"
  E4_active_vector:
    meaning: "pattern propagates through infrastructure, bodies, or Home Layer links"
    default_action: "quarantine with medical and forensic safeguards"
  E5_command_threat:
    meaning: "confirmed hostile routing, body occupation, lethal infrastructure control"
    default_action: "CHASER emergency containment"
```

## Exit Criteria

Every nonlethal exposure hold is supposed to name a release path before the hold
begins.

```yaml
exit_criteria:
  minimum_requirements:
    - stable self-report across repeated interviews
    - Echo Core exposure logs below escalation threshold
    - Home Layer witness export preserved without over-opening the home record
    - hospital telemetry stable or medically explained
    - Memory Bank continuity flag reviewed for billing conflict
    - field team note on whether the person is patient, witness, carrier, or threat
  review_window:
    routine: "six to twenty-four hours"
    emergency: "minutes to hours before Central lock"
  failure_state:
    - no exit criteria recorded
    - threat label applied before independent review
    - Home Core record opened wider than emergency need
    - evidence compaction destroys residue drift
```

## Social Function

- Gives CHASER a reason to exist beyond force: someone must separate danger,
  illness, testimony, and personhood risk during contamination events.
- Makes Lian Zhou's authority concrete. Her mercy is not sentimental; it is a
  procedural demand for exit criteria and defensible labels.
- Lets hardliners be frightening without making them stupid. In a true E4 or E5
  incident, delay can kill people.
- Gives White Ghost Team a field dilemma in Memory Storm: preserving ambiguous
  carriers may protect the only proof that the storm is coordinated
  infrastructure behavior.
- Creates class tension because wealthy citizens can buy longer review, while
  poor districts are easier to label as active vectors.

## Story Hooks

- A child repeats a dead miner's last words during Memory Storm, and CHASER
  Central wants E3 upgraded to E4 because the phrase appears in three cities.
- Eve calms an intake room, but Lian requires every affective intervention to be
  logged so that comfort does not become hidden control.
- Shion proves a Home Core export was enough to classify a patient as E2, but
  Memory Bank wants a wider export to reduce its own liability.
- Kane wants the route sealed after a carrier injures a nurse; Lian asks whether
  sealing the route also deletes the nurse's best evidence.
- Zero sees that her own unresolved continuity could be processed by the same
  bands if CHASER Central stops treating her as an officer.

## Consistency Notes

- Civil Exposure Classification is law, medicine, infrastructure telemetry,
  witness handling, and bureaucratic pressure. It is not supernatural diagnosis.
- The bands identify operational risk, not moral worth or metaphysical truth.
- A Home Core or Home Layer export should be scoped. More data can mean more
  harm, not more truth.
- The mechanism supports Memory Storm, Project E-01, and White Ghost Mutiny but
  does not solve them.
- Story-facing prose should use Home Core, Home Layer, Memory Sea, Second
  Nervous System, Echo Core, CHASER, and White Harbor.

## Pipeline State

```yaml
stage: candidate_output
agent: LoreAgent
created_at: 2026-07-08T13:01:51+08:00
canon_promotion: false
related_candidates:
  - outputs/character/20260708-090128-candidate-character-020-lian-zhou.md
  - outputs/consistency/20260708-090128-canon-audit-lian-zhou.md
  - outputs/story/20260704-180101-story-beat-memory-storm.md
  - stories/season_1_production_plan.md
  - bible/chaser_organization.md
requires:
  - TechnologyAgent entry for Exposure Class Override Ledger
  - FactionAgent impact on CHASER, White Harbor, Memory Bank, Ghost Union, and Black Zone
  - ConsistencyAgent review against prior quarantine and classification mechanisms
asset_tasks: blocked_until_promotion
```
