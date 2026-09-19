# Lore Promotion: Episode 07 Relation / Delay Infrastructure

Status: promoted_narrow

Agent: LoreAgent with TechnologyAgent and FactionAgent support

Created at: 2026-08-30T13:01:46+08:00

## Decision

Promote `Household Relation Graph` and `Civil Delay Token` as narrow Season 1
Episode 7 technologies. Promote `Family Graph Rollback` and `Emergency Delay
Window` as their Episode 7 use cases, not as broad legal regimes.

Primary canon added:

- `technologies/household_relation_graph.md`
- `technologies/civil_delay_token.md`

Primary faction canon updated:

- `factions/white_harbor.md`
- `factions/memory_bank.md`
- `factions/chaser.md`

## Promotion Rationale

Episode 7 needs a civic mechanism before StoryAgent drafts the full
`Probability Debt` treatment. The existing candidate bundle has already passed
distinctness checks, and the 09:00 character boundary sheet depends on these
mechanisms directly.

The promotion stays narrow:

- `Household Relation Graph` is the data layer that stores relation authority.
- `Family Graph Rollback` is the failure mode that damages those relation
  edges while civil identity remains active.
- `Civil Delay Token` is the time-limited White Harbor authorization.
- `Emergency Delay Window` is the interval created by that token.

## Episode 7 Lock

```yaml
episode_07_relation_delay_infrastructure:
  episode: "Season 1 Episode 7 / Probability Debt"
  civilian_center: Imari_Chen_family
  responsible_pressure_point: Noah
  procedural_hinge: Sofia_Marin
  institutional_offer: Yao_Nian
  failure_surface: Family_Graph_Rollback
  data_layer: Household_Relation_Graph
  delay_surface: Emergency_Delay_Window
  token: Civil_Delay_Token
  opening_harm: school_gate_denies_guardian_relation
  required_limit: delay_buys_time_not_restoration
```

## Canonized Boundaries

- Imari Chen remains living, legally active, and non-Ghost.
- The harm is relation-edge rollback, not memory erasure or total identity
  deletion.
- The Probability Engine can route risk through predictive allocation, queue
  priority, infrastructure timing, and resource routing only.
- Civil Delay Tokens can pause a named automated action; they cannot repair the
  graph.
- Home Core evidence must remain scoped to disputed edges unless a separate
  review authorizes more.
- Memory Bank repair can be technically effective and morally dangerous at the
  same time.
- CHASER evidence holds can preserve proof while worsening a family's practical
  restoration timeline.

## Held Unresolved

- Full Episode 7 story package.
- Episode 7 relationship map.
- Imari Chen or Sofia Marin as promoted recurring character entries.
- Noah's long-term accountability outcome.
- Any general cross-episode law for all relation damage.
- Memory Bank repair terms beyond this narrow collateral pressure.

## Pipeline State

```yaml
idea: episode_07_probability_debt_relation_delay_infrastructure
candidate_output: accepted_from_existing_bundle
consistency_check: complete
canon_promotion: narrow_primary_technology_and_faction_notes
timeline_update: not_required
relationship_update: deferred_until_story_acceptance
faction_update: complete
asset_task_generation: queued
next_recommended_step: "18:00 StoryAgent should draft the full Episode 7 Probability Debt treatment."
```
