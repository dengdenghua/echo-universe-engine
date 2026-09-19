# Relationship Acceptance: Episode 06 Story Package

Status: accepted_for_promotion

Agent: RelationshipAgent / ConsistencyAgent

Created at: 2026-08-29T23:01:18+08:00

Subject: `outputs/story/20260829-180116-episode-06-social-ocean-funeral-full-treatment.md`

## Decision

Accept the full Episode 6 treatment as the story package and promote two
compact primary canon surfaces:

- `stories/episode_06_social_ocean_funeral.md`
- `relationships/episode_06_social_ocean_funeral_relationships.yaml`

The relationship map is promoted because Episode 6 depends on active pressure
between the Wei family, the Wei Suyin pattern, Home Core permissions, Memory
Bank, Ghost Union, Yao Nian, and White Ghost Team. Keeping this only in
candidate output would make later Episode 7 routing too easy to flatten into a
technology problem.

## Accepted Relationship Logic

```yaml
accepted_episode_06_relationship_logic:
  case_center: Wei_family
  mother_pattern_status: possible_self_updating_爱的残响
  living_family_authority:
    Wei_Lin: refusal_remains_valid
    Wei_Min: one_night_voluntary_dinner_only
    Wei_An: consent_origin_responsibility_without_sole_villain_status
  institutional_triangle:
    Memory_Bank: collateral_pressure_and_emergency_stay_pricing
    Ghost_Union_legal_cells: review_preservation
    Ghost_Union_sanctuary_cells: illegal_copy_temptation
  white_ghost_role:
    Eve: table_testimony
    Shion: permission_split_and_vendor_signature
    Noah: no_clean_option
    Luna: door_boundary_echo
    Zero: narrow_evidence_hold
  outcome: harm_reduced_not_resolved
```

## Canon Promotion Notes

- The Wei family becomes Episode 6 case canon, not recurring-protagonist canon.
- Yao Nian remains candidate as a full character, but her Episode 6 function is
  accepted: forty-eight hours of stay under weak Ghost support language.
- Memory Lien Notice remains the promoted narrow Episode 6 mechanism.
- The Home Core permission split is accepted as harm reduction, not proof of
  innocence or guilt.
- The vendor signature route is accepted as Episode 7 handoff material, not a
  solved conspiracy.

## Held Unresolved

- Wei Suyin identity and personhood.
- Whether the mother-pattern is legally Wei Suyin, property, product, or
  malware.
- Memory Bank debt cancellation or ownership.
- Ghost Union sanctuary copy success.
- CHASER family containment.
- Broader Memory Lien Notice law outside Episode 6.
- Whether Yao Nian should be promoted into `characters/`.

## Timeline / Faction / Asset Decision

No timeline edit is required. `timeline/timeline.yaml` remains macro-history
scoped and should not absorb individual early Season 1 case beats.

No faction edit is required in this run. `factions/memory_bank.md` and
`factions/ghost_union.md` already hold the Episode 6 liened Home Core split.

No new asset task is required. The Wei family case-group task and Memory Lien
Notice prop task already cover the accepted story package.

## Pipeline State

```yaml
idea: episode_06_social_ocean_funeral
candidate_output: complete
consistency_check: passed
canon_promotion: complete
timeline_update: not_required
relationship_update: promoted_case_map
faction_update: not_required
asset_task_generation: existing_tasks_sufficient
next_recommended_step: "09:00 CharacterAgent should prepare Episode 7 probability-cost case characters and decide whether Noah needs a focused boundary sheet before the next treatment."
```
