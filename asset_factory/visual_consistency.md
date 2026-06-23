# Visual Consistency Pipeline

ECHO manga production must not generate character images from loose prompts alone.

Every recurring character needs a locked visual package before appearing in comic panels.

## Required Asset Stages

## Stage 1: Character Lock Sheet

Generate and approve:

- full body front view
- full body side view
- full body back view
- head close-up
- neutral expression
- 4 expression variants
- equipment callouts
- color swatches
- silhouette check

Output:

```text
assets/characters/<id>_<name>/lock_sheet/
```

## Stage 2: Reference Pack

From approved lock sheet, create:

- face reference
- outfit reference
- color reference
- pose reference
- accessory reference
- negative reference notes

Output:

```text
assets/characters/<id>_<name>/references/
```

## Stage 3: Model Consistency Layer

For production, use one or more:

- IP-Adapter face reference
- ControlNet pose / lineart
- LoRA per main character
- consistent seed library
- fixed prompt prefix
- approved color swatches

Do not rely on one text prompt for recurring characters.

## Stage 4: Panel Generation

Every panel task must include:

- character ids
- approved reference paths
- outfit state
- expression
- camera angle
- pose
- lighting
- location
- continuity notes
- negative prompt

## Stage 5: Consistency Review

Before panel approval, check:

- face match
- hair shape
- eye color / visor
- outfit silhouette
- accent color
- Echo Core light state
- accessories
- height relationship
- faction uniform rules
- no fantasy drift

## Global Style Lock

Use `bible/visual_system_v1.md` as the style authority.

Use `assets/characters/white_ghost_team_visual_locks.yaml` as character identity authority.

## File Naming

```text
assets/characters/001_zero/
  lock_sheet/
  references/
  expressions/
  poses/
  panels/
  metadata.yaml
```

## Canon Rule

If a generated image conflicts with the visual lock, the image is wrong. Do not update canon to match accidental generations.
