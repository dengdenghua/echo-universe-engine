# Creative Plugin Pipeline

ECHO Universe Engine now keeps local mirrors of two Codex creative plugins:

- `codex_plugins/product-design`: product design, UX audit, visual ideation, URL-to-code, image-to-code, and prototype sharing workflows.
- `codex_plugins/remotion`: Remotion and React video-production guidance for animation, audio, captions, 3D, transitions, charts, and composition setup.

These plugins sit beside the canon engine. They do not replace the Python runtime, the canon bible, or the asset factory. They provide repeatable creative workflows that can turn ECHO canon into reviewable interfaces and videos.

## ECHO Inputs

Use these project sources as grounding before invoking either plugin:

| Source | Use |
| --- | --- |
| `bible/` | Canon law, factions, setting rules, world overview, visual system, and technology constraints. |
| `stories/` and `outputs/story/` | Beats, episodes, scene material, dialogue hooks, and trailer candidates. |
| `characters/` and `outputs/character/` | Character sheets, relationship hooks, visual traits, and personality constraints. |
| `relationships/` | Faction and character tension maps for storyboards and product flows. |
| `console/` | Existing web console surface for Product Design audits and prototype iterations. |
| `workflows/asset_task.schema.yaml` | Visual asset handoff shape for later render workers. |

## Product Design Usage

Use Product Design when the output is an interactive product artifact:

- ECHO console redesigns or feature prototypes.
- Mobile gateway flows for character binding, universe feed, realm access, wallet, or identity status.
- Creator/admin tools for canon review, faction events, story promotion, or asset task review.
- UX audits of `console/` or any future web surface.

Expected workflow:

1. Ground the request in current ECHO product context and visual sources.
2. Confirm the product/design brief before ideation or build work.
3. Generate or select visual directions before implementing a new UI.
4. Keep implementation aligned with existing surfaces, styles, and product intent.
5. Store durable notes, screenshots, and follow-up specs under `workflows/` or `outputs/`.

## Remotion Usage

Use Remotion when the output is a video artifact:

- Season trailers, faction explainers, character reveal reels, and lore capsules.
- Animated charts for economy, memory market, or faction influence.
- Captioned story beats and social clips derived from `outputs/story/`.
- Visual system tests that combine typography, timing, audio, and generated images.

Recommended project shape when a real Remotion app is needed:

```text
video/
  remotion-studio/
    package.json
    src/
    public/
```

Keep generated videos and still frames out of source control unless they are intentional review artifacts. Prefer storing task specs, scripts, and small preview stills.

## Combined Flow

For ECHO creative work that needs both product and video:

1. Pick canon sources from `bible/`, `stories/`, `characters/`, and `relationships/`.
2. Use Product Design to shape the reviewable product surface or storyboard control panel.
3. Use Remotion to turn the approved story, art direction, or prototype motion into a renderable composition.
4. Send asset requests through the existing visual pipeline when real images, character art, or environment plates are required.
5. Record final decisions in the relevant workflow or output folder so future agents inherit the same constraints.

## Quality Gates

- Respect hard canon: no magic, no supernatural powers, no multiverse, and no time travel.
- Keep ECHO visual work consistent with `bible/visual_bible.md` and `bible/visual_system_v1.md`.
- For UI work, inspect existing screens and styles before proposing changes.
- For video work, verify timing, layout, captions, audio, and frame readability before handoff.
- Preserve third-party plugin manifests and licenses when refreshing `codex_plugins/`.
