# Asset Factory

This folder is the future visual-generation boundary.

The canon engine should only create structured image/storyboard tasks. Workers in this folder can later consume those tasks and call:

- ComfyUI
- SDXL
- Flux
- ControlNet / IP-Adapter / LoRA workflows
- Manga storyboard and panel-layout tools

Keep this layer replaceable. Canon should not depend on one image model.
