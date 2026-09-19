# Visual Audit: MiniMax H3 White Harbor Transit Test

Status: candidate reviewed

Canon action: none

Source scene: Season 1, Episode 1, `Stranger Memory / 陌生记忆`

Generated assets:

- `outputs/assets/20260822-minimax-h3-white-harbor-transit-test.mp4`
- `outputs/assets/20260822-minimax-h3-white-harbor-transit-test-poster.png`

## Generation Record

```yaml
application: MiniMax Design 3.0.2
model: MiniMax H3
task_id: "433476318962125"
duration_seconds: 8
aspect_ratio: "9:16"
resolution: "1440x2560"
video_codec: H.264
audio_codec: AAC
status: generated_candidate
```

The first submission failed before generation because MiniMax Design sent
`aspect_ratio` while the H3 endpoint required `ratio`. The in-app agent retried
with the supported field and completed the second task.

## Test Intent

Validate whether MiniMax H3 can express the ECHO visual language in a short
motion-comic shot:

- bright cold-white transit wreckage;
- clean monitored infrastructure rather than dirty neon cyberpunk;
- Lin Qiao stabilizing a trapped child with borrowed procedural memory;
- a white medical drone with restrained cyan interface light;
- memory contamination expressed as subtle compression afterimage;
- no readable text, logo, magic, literal Ghost, halo, or gore.

This test did not use a Lin Qiao character reference and must not establish her
visual canon.

## Pass

- Correct 9:16 vertical delivery at 2K resolution.
- Clean anime-film rendering is usable for motion-comic development.
- White transit interior and cyan medical interface are broadly aligned with
  ECHO's surgical monitored-world language.
- Medical drone is readable and remains technological.
- No dirty neon street aesthetic, fantasy armor, visible brand logo, or
  readable interface text.
- Camera movement is restrained enough for a short vertical scene.

## Fail

- Lin Qiao reads as a young male or androgynous adolescent rather than a
  thirty-two-year-old woman. Character identity failed.
- The trapped child and Lin Qiao are not staged clearly enough for the audience
  to understand the injury, maintenance panel, or emergency action.
- The medical choreography reads as reaching and holding rather than a precise
  life-saving procedure.
- The requested subtle hand afterimage becomes several solid overlapping hands
  near the end. This reads as anatomy failure, mutation, or supernatural power.
- The carriage wreckage is visible, but the shot lacks the bright civic-system
  calm and permission-denial tension that makes the ECHO incident distinctive.
- The visual result is generic anime disaster footage without the story context
  supplied by locked props, interfaces, and character design.

## Canon Check

Recommendation: reject for canon and final production; retain as a technical
generation test.

No literal magic is stated, but the solid duplicated hands violate the intended
technological reading. Memory contamination must be rendered as compression
lag, frame offset, UI motion trace, or translucent two-frame persistence, never
as additional physical limbs.

## Next Test Requirements

1. Create and approve a Lin Qiao face, outfit, and age reference before video
   generation.
2. Generate an approved still storyboard frame before asking H3 for motion.
3. Use one 4-6 second shot rather than four described shots inside eight seconds.
4. State `exactly two anatomical hands throughout`; forbid extra fingers,
   duplicate limbs, merged hands, and solid afterimages.
5. Express contamination as a two-frame translucent compression trail isolated
   to hand movement.
6. Show one concrete action: Lin Qiao opens the drone's emergency cartridge while
   the drone's abstract cyan permission indicator remains locked.
7. Keep the boy partially obscured by a maintenance panel so the emergency is
   readable without gore.

## Pipeline State

```yaml
idea: minimax_h3_white_harbor_transit_test
candidate_output: complete
consistency_check: complete
canon_promotion: rejected_for_now
timeline_update: not_applicable
relationship_update: not_applicable
faction_update: not_applicable
asset_task_generation: next_test_blocked_on_lin_qiao_visual_lock
```
