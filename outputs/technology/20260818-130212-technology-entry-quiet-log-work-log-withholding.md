# Technology Entry: Quiet Log (Home Core Work-Log Withholding)

## Candidate Canon Entry

The Quiet Log is a settings-level withholding practice inside the route
logging layer: a hospice worker stops mirroring unpaid comfort-hold and
afterword-reading minutes into the care-reserve model. The care still
happens; the record goes silent; the route model reads a false surplus.

It is not an Echo Core ability, memory erasure, Ghost continuity, or fraud
tool. Its force comes from Home Core work-log mirror settings, route staffing
rosters, care-reserve model reads, worker bond flags, coverage-condition
letters, and CHASER safety-event thresholds.

```yaml
technology:
  name: Quiet Log
  category: Home Core work-log withholding / route-model visibility control
  status: candidate (held)
  related_lore: The Quiet Log (Negative Double-Count)
  primary_users:
    - hospice route attendants under bond pressure
    - Free Orbital Mutual Hospice Network route workers
    - workers refusing to become adverse reviewer files
  prohibited_use: >
    Cannot erase memory, create care, restore recorded capacity, clear a
    conduct file, stop CHASER, open sealed Home Layer content, certify a
    Ghost, or falsify a route chit.
```

## Mechanism Fields

```yaml
quiet_log_mechanism:
  entry_point: Home Core work-log mirror settings on the route logging app
  withheld_interval: unpaid comfort-hold / afterword-reading minutes
  route_model_read: >
    physical presence, route chit, and staffing slot remain visible; unpaid
    minutes drop out of the capacity read
  visible_records:
    - route_staffing_roster
    - route_chit_hash
    - physical_presence_trace
  hidden_records:
    - unpaid_minute_window_ids
    - comfort_hold_duration
    - afterword_reading_duration
    - reserve_model_capacity_use
  worker_state:
    - worker_bond_exposure_flag
    - reassignment_risk
    - conditional_slot_status
  institution_state:
    - coverage_condition_letter_ids
    - Memory_Bank_custody_release_records
    - Ghost_Union_anti_starvation_motion
    - CHASER_safety_event_boundary
    - route_surplus_read
  contradiction_flags:
    - negative_double_count
    - false_surplus
    - coerced_invisibility
    - ghost_labor_mislabel_risk
    - safety_precursor_mislabel_risk
```

## Operations

- Mirror toggle: worker sets unpaid minutes to `keep` or `drop` per interval
  at the bracelet.
- Capacity read: the route model still sees the worker present and staffed but
  reads the unpaid interval as absent from the reserve.
- Surplus formation: enough withheld minutes produce a capacity surplus with
  no recorded labor — the negative double-count.
- Bond pressure: lower recorded hours make the bond conditional and the route
  slot easier to reassign if the model reads the worker as surplus.
- Scope preservation: hiding minutes does not open phrase text, reveal adapter
  locations, or grant Home Layer access.

## Failure Modes

- Starving the reserve: the anti-starvation fund shrinks while the route model
  reports surplus, so the sealed escrow loses support it appears to have.
- Ghost-labor mislabel: a technician who can see the double-count can read the
  quiet log as fraud or ghost labor instead of worker fear.
- Safety mislabel: an invisible precursor interval can be relabeled as a named
  hazard to justify CHASER authority without a real safety event.
- Forced re-recording: White Ghost Team visibility can make hidden care
  countable again, converting a survival tactic into reviewer exposure.
- Black-market drift: bond pressure pushes workers toward forged clean records,
  which is the illegal alternative the quiet log exists to refuse.

## Story Limitations

Ama Osei can keep or drop minutes. Shion can prove the surplus is real care
made unrecorded. Eve can name the coercion in the silence. Zero can keep
CHASER from calling it ghost labor or a hazard. None of them can restore the
reserve's honesty without exposing the workers, clear a conduct file, force
the insurer to pay, open Ilya Marr's afterword, or certify the trace as a
Ghost.

## Hold Decision

Per the Ama Osei promotion gate, a TechnologyAgent entry is only warranted if
the Quiet Log or the coverage-condition mechanism recurs beyond the Nara
corridor route. This entry is written to ground the next StoryAgent beat (The
Kindness Log Goes Quiet) and is explicitly held: no canon promotion, no
`technologies/` edit, no timeline entry, until the beat lands and the route
either recurs or is selected for Season 1 continuity.

## Pipeline State

```yaml
stage: candidate_output
agent: TechnologyAgent
created_at: "2026-08-18T13:02:12+08:00"
canon_promotion: false
hold_reason: mechanism not yet recursed beyond Nara corridor route
related_lore: outputs/lore/20260818-130212-lore-entry-quiet-log-negative-double-count.md
related_faction: outputs/faction/20260818-130212-faction-decision-route-insurer-institutional-status.md
related_character: outputs/character/20260818-090039-candidate-character-043-ama-osei.md
requires_consistency_review: true
```
