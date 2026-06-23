# Asset Factory

This folder is the future visual-generation boundary.

The canon engine should only create structured image/storyboard tasks. Workers in this folder can later consume those tasks and call:

- ComfyUI
- SDXL
- Flux
- ControlNet / IP-Adapter / LoRA workflows
- Manga storyboard and panel-layout tools

Keep this layer replaceable. Canon should not depend on one image model.

## Consistency First

Main characters must not be generated from loose prompts alone.

Use:

```text
assets/characters/white_ghost_team_visual_locks.yaml
asset_factory/visual_consistency.md
asset_factory/comic_consistency_checklist.md
```

Before manga panel generation, create and approve character lock sheets, face references, outfit references, expression sheets, and consistency metadata.
