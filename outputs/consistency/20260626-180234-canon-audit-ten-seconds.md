# Consistency Audit: Ten Seconds

Status: candidate_check

Subject:

- `outputs/story/20260626-180234-story-beat-ten-seconds.md`

Agent: ConsistencyAgent

## Verdict

Pass as candidate output. Do not promote yet.

The story beat fits the Season 1 Episode 4 slot and routes forward from Episode
3 without duplicating the Black Zone receipt case. It keeps the opening
world-centric by beginning with Tomas Vale, a veteran care-status renewal, and a
Home Core subsidy threat before White Ghost Team enters.

## Canon Compatibility

```yaml
hard_rules:
  no_magic: pass
  no_supernatural_possession: pass
  no_multiverse: pass
  no_time_travel: pass
  technology_origin: pass
  god_fragment_physics_break: not_applicable
story_rules:
  hero_centric_false: pass
  case_character_emotional_center: pass
  white_ghost_team_as_investigators: pass
  one_major_system_increment: pass
terminology:
  avoids_forbidden_product_terms: pass
  uses_story_facing_terms: pass
```

## Checks Against Existing Canon

- Matches `characters/002_kane.md`: Kane's Combat Download requires ten seconds
  of uninterrupted Echo Core sync and becomes unstable under emotional stress.
- Matches `technologies/ability_constraints.md`: the cost includes borrowed
  fear, tremor, fatigue, reflex mismatch, and trauma residue; the ability does
  not exceed body tolerance or erase emotional cost.
- Matches `stories/season_1_episode_outline.md`: Episode 4 focuses on a
  body-occupied ex-soldier, Kane, borrowed skill, borrowed pain, and Zero's
  upload-fragility pressure.
- Routes from `outputs/story/20260625-180114-story-beat-black-zone-receipt.md`
  by using the shell-buyer and White Ghost record test as the next-episode
  pressure point.

## Duplication Check

No existing story output develops Episode 4 as a full beat. Existing material
mentions:

- Episode 4 title and summary in Season 1 outline.
- Kane's ability limits in character and technology files.
- Episode 3's ending hook about upload-fragility testing.

The new candidate expands those seeds without replaying the Episode 3 Black Zone
market structure.

## Risks Before Promotion

1. Tomas Vale and Ilya Sorn are new names and should remain candidate-only until
   CharacterAgent decides whether they become formal B-rank/case characters.
2. The phrase "body-occupied" should be explained in canon as neural motor
   overwrite / procedural occupation, not metaphysical possession.
3. Veteran care infrastructure needs a later LoreAgent or TechnologyAgent pass
   if it becomes recurring rather than single-episode context.
4. The E-01 upload-fragility tag should remain a hint. It must not reveal Zero's
   full Project E-01 origin before Episode 14.

## Promotion Recommendation

Hold in `outputs/story/` as candidate.

Recommended next pipeline steps:

- CharacterAgent: decide whether Tomas Vale and Ilya Sorn need candidate files.
- TechnologyAgent: define "procedural occupation" as a constrained neural
  interface exploit if reused.
- RelationshipAgent: add a candidate Kane -> Zero pressure note after Episode 4
  if the beat is promoted.
- Asset task generation: convert the included location, action, prop, and case
  character seeds into workflow-compatible asset tasks after promotion.
