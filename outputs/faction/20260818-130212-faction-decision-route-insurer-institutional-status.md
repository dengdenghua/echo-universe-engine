# Faction Decision: Route Insurer Institutional Status

## Decision

Route insurers remain a candidate pressure layer. They are not promoted into
the primary faction list, are not given a proper noun, and do not appear in
`factions/`, `bible/`, `timeline/`, or `relationships/` canon.

The decision follows the Ama Osei canon audit gate: a FactionAgent/LoreAgent
decision was required before the quiet-log route could recur. This pass makes
that decision and records the promotion criteria so future runs do not re-litigate
it.

## Why Not Promoted Yet

```yaml
route_insurer_status:
  current: candidate_pressure_layer
  display_token: route_insurer_conduct_desk
  promoted_to_primary_faction: false
  reasons:
    - >
      The sealed-afterword route is candidate-only; it is not in Season 1
      episode continuity and has no timeline placement.
    - >
      A faceless desk preserves the story wound: kindness becomes exposure
      without a villain to blame, keeping the antagonist institutional.
    - >
      Naming the insurer now would create a faction without depth, inviting
      filler lore before the route earns a bible entry.
    - >
      The insurer has not yet recurred beyond the Nara corridor route; one
      named consortium would overcommit the orbital economy layer.
```

## Promotion Criteria (all three required)

```yaml
promote_route_insurer_when:
  - criterion_1_timeline: >
      the sealed-phrase orbital route enters Season 1 episode continuity and
      receives a timeline decision
  - criterion_2_recurrence: >
      the insurer's conduct desk recurs in at least two more story beats with
      distinct pressure functions (quiet-log beat, then one beyond it)
  - criterion_3_bible_need: >
      a named desk or consortium is needed to anchor a faction-conflict matrix
      entry or an institutional page; a candidate faction file must exist in
      outputs/faction first
```

Until then, story and relationship passes keep using the token
`route_insurer_conduct_desk` and the prose name "the desk."

## Unpromoted Naming Candidates

These are output-only candidates, explicitly not canon. Naming remains
deferred until the criteria are met; do not copy these into promoted files.

```yaml
naming_candidates_unpromoted:
  - Ceres Route Underwriting Collective
  - Orbital Hospice Underwriters Guild
  - Route Coverage Consortium (RCC)
  - the desk that signs (prose alias)
```

## Faction Responses Under This Decision

```yaml
Free_Orbital_Mutual_Hospice_Network:
  public_position: >
    No-copy care should not depend on workers hiding their own minutes.
  private_pressure: >
    The network needs the reserve to keep sealed cases fed, but making the
    quiet log visible again could collapse worker trust in the route.
  story_use: >
    Keeps hospice materially vulnerable and morally necessary; Ama's route is
    its test corridor.

Ghost_Union:
  public_position: >
    Anti-starvation reserve must not be starved by silence that fear created.
  private_pressure: >
    The Union wants the quiet log re-recorded without exposing workers; it
    cannot promise that and keep the reserve honest.
  story_use: >
    Creates a union motion that White Ghost Team can neither endorse nor stop.

Memory_Bank:
  public_position: >
    Unrecorded capacity is a valuation hole and a custody risk.
  private_pressure: >
    The bank prices the silence as loss while benefiting from the same
    invisibility that keeps release costs out of the ledgers.
  story_use: >
    Shows the bank's cost language making the quiet log look like theft.

CHASER:
  public_position: >
    A quiet log is not a safety event until a named threshold is met.
  private_pressure: >
    Financial scarcity and worker fear can be relabeled as ghost labor or a
    hazard precursor if the surplus is read without worker context.
  story_use: >
    Gives Zero the jurisdictional line to defend; the quiet log must not be
    treated as fraud or ghost labor.

Black_Market:
  public_position: >
    None. Brokers read the quiet log as demand for forged clean records.
  private_pressure: >
    Workers under bond pressure are offered illegal record repair; the quiet
    log's existence creates that market signal without Black Zone causing the
    wound.
  story_use: >
    Keeps Black Market downstream of a legal wound, never its origin.
```

## Canon Boundaries

- The desk cannot open sealed Home Layer content, decide Ghost personhood,
  cancel Memory Bank debt, clear conduct files, or override CHASER safety
  thresholds.
- The quiet log is not fraud; any audit must name the coercion before the
  "theft."
- No magic, supernatural powers, multiverse, or time travel. The desk's force
  comes from route policies, coverage letters, reserve feeds, bond ledgers,
  appeal timers, and CHASER boundaries.

## Pipeline State

```yaml
stage: candidate_output
agent: FactionAgent
created_at: "2026-08-18T13:02:12+08:00"
canon_promotion: false
fulfills_gate: "20260818-090039-canon-audit-ama-osei -> faction decision on route insurer status"
related_lore: outputs/lore/20260818-130212-lore-entry-quiet-log-negative-double-count.md
related_technology: outputs/technology/20260818-130212-technology-entry-quiet-log-work-log-withholding.md
related_character: outputs/character/20260818-090039-candidate-character-043-ama-osei.md
faction_canon_update: held
next_decision_point: criterion check at next 13:00 slot after the quiet-log story beat lands
```
