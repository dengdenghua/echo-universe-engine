# Faction Dossier (Candidate): Route Insurer — Naming Review Readiness

Status: candidate

Agent: FactionAgent (with LoreAgent / TechnologyAgent support)

Created at: 2026-08-19T13:02:00+08:00

## Purpose

This dossier fulfills criterion_3 of the 2026-08-18 route-insurer decision
before the naming review can run: a candidate faction file must exist in
`outputs/faction/` first. It re-checks all three promotion criteria after the
quiet-log story beat landed and after Nina Alvarez carried the coverage-
condition logic to the Home Layer. It does not name the insurer, does not
promote anything into `factions/`, `bible/`, `timeline/`, or
`relationships/`, and does not change the display token.

```yaml
route_insurer_status:
  current: candidate_pressure_layer
  display_token: route_insurer_conduct_desk
  prose_alias: the desk
  naming_review_ready: false
  promoted_to_primary_faction: false
  promoted_to_timeline: false
```

## Promotion Criteria Re-Check (2026-08-19 13:00)

```yaml
promote_route_insurer_when:
  criterion_1_timeline:
    met: candidate_only
    status: >
      The sealed-phrase orbital civic route received a candidate Season 1
      timeline placement in this bundle
      (outputs/lore/20260819-130200-lore-entry-season1-timeline-orbital-civic-arc.md).
      Final approval still needs the Season 1 packaging decision.
  criterion_2_recurrence:
    met: partially
    status: >
      Recurrence #1 is story-validated: The Kindness Log Goes Quiet
      (2026-08-18) pressed the conduct desk as an anonymous procedure.
      Recurrence #2 pressure function — the domestic audit sweep that hunts
      the silence it created — is established at character level via Nina
      Alvarez (2026-08-19 09:00) but must land in story form at the 18:00
      StoryAgent beat before this criterion reads as met.
  criterion_3_bible_need:
    met: candidate_only
    status: >
      This file is the required candidate faction file. A named desk or
      consortium is now justified only if the Home Layer extension survives
      the story beat and Season 1 packaging keeps the orbital civic case chain
      in continuity. Naming itself stays deferred.
```

## Naming Candidate Narrowing (Home Layer Extension Weigh-In)

The desk followed a worker from orbital hospice to a domestic eldercare route
on the Home Layer. That narrows the candidate names because a corridor-bound
name now undersells the insurer's actual reach.

```yaml
naming_candidates_unpromoted:
  - name: Route Coverage Consortium (RCC)
    fit_after_home_layer: strong
    reason: >
      Its public instrument is route coverage: coverage-condition letters,
      reserve feeds, and audit sweeps, none of which are corridor-bound. Fits
      the orbital and Home Layer routes equally.
  - name: Ceres Route Underwriting Collective
    fit_after_home_layer: moderate
    reason: >
      Route-level collective language still works, but the Ceres frame ties
      the name to orbital economy when the desk now operates ground-side.
  - name: Orbital Hospice Underwriters Guild
    fit_after_home_layer: weak
    reason: >
      The word "Orbital" is now false on the Home Layer; the guild frame also
      overstates a mutuality the desk does not have.
  - name: the desk that signs (prose alias)
    fit_after_home_layer: preserved
    reason: >
      Remains the safe prose token for beats. Keep using it until naming is
      formally selected.
```

Final selection is deliberately deferred to the naming review that runs after
the 18:00 Nina beat lands and the 23:00 relationship pass closes.

## Institutional Footprint (Functions The Desk Exercises)

```yaml
institutional_footprint:
  public_instrument: route coverage (coverage-condition letters, reserve feeds, audit sweeps)
  pressure_functions:
    - coverage_condition_review: classifies worker intervals as covered care, worker fault, excluded courtesy, or safety-event precursor
    - reserve_insufficiency_motion: converts a false surplus into a red reserve read
    - adverse_reviewer_file: turns an honest classification into reviewer exposure (Priya Chand)
    - bond_drawdown: makes lower recorded hours a conditional-slot risk
    - domestic_audit_sweep: new Home Layer function that hunts the silence it created by relabeling hidden listening as ghost labor
  operating_corridors:
    - orbital hospice route (Nara corridor) — recurrence #1
    - Home Layer domestic eldercare route — recurrence #2 pressure function
  force_sources:
    - route policy clauses
    - coverage-condition letters
    - reserve model capacity reads
    - worker bond exposure flags
    - appeal timers
    - audit sweep thresholds
    - CHASER safety-event boundary (bounded)
```

## What The Desk Is Not

- Not a person and not a villain to blame. Keeping it faceless preserves the
  story wound: kindness becomes exposure through procedure, not malice.
- Not a Ghost, not a God Fragment, not an ECHO emergent will. Its force comes
  from plausible infrastructure listed above.
- Cannot open sealed Home Layer content, decide Ghost personhood, cancel
  Memory Bank debt, clear conduct files, override CHASER safety thresholds,
  or restore recorded capacity.

## Faction Response Deltas (Home Layer Extension)

```yaml
Free_Orbital_Mutual_Hospice_Network:
  delta: >
    The network's test corridor is no longer the only place the wound shows;
    the quiet log now runs on ground routes it does not staff, which weakens
    the orbital-specific remedy.
Ghost_Union:
  delta: >
    The anti-starvation reserve now has a ground-side mirror; the union's
    re-record motion must decide whether it covers domestic eldercare routes.
Memory_Bank:
  delta: >
    The bank prices the Home Layer silence as capacity loss the same way it
    priced the orbital silence, confirming the cost language follows the
    worker, not the corridor.
CHASER:
  delta: >
    The domestic audit sweep risks reading real listening as ghost labor;
    Zero's boundary note must now hold on the Home Layer, not only in orbit.
Black_Market:
  delta: >
    Domestic route cooperatives under audit pressure are a new demand signal
    for forged clean records; Black Market stays downstream of the legal wound.
```

## Canon Boundaries

- Quiet log is not fraud. Any audit must name the coercion before the "theft."
- The desk cannot turn a sealed afterword into a fraud exhibit; the widow's
  Home Layer content and the husband's residue stay closed, unpriced, uncopied,
  untranslated, uncertified, and unresolved.
- No magic, supernatural powers, multiverse, or time travel.

## Pipeline State

```yaml
stage: candidate_output
agent: FactionAgent
created_at: "2026-08-19T13:02:00+08:00"
canon_promotion: false
fulfills_prerequisite: criterion_3 candidate faction file for the route-insurer naming review
related_lore: outputs/lore/20260819-130200-lore-entry-season1-timeline-orbital-civic-arc.md
related_technology: outputs/technology/20260819-130200-technology-gate-recheck-quiet-log.md
related_character: outputs/character/20260819-090200-candidate-character-044-nina-alvarez.md
related_story_beat_required: 2026-08-19 18:00 Nina domestic-audit-sweep beat (pending)
faction_canon_update: held
next_decision_point: naming review after the 18:00 Nina beat + 23:00 relationship pass + Season 1 packaging decision
```
