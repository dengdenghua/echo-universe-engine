# Codex Plugin Mirror

This directory vendors the Codex plugins that support ECHO Universe creative production.

The plugin bundles are copied from the local Codex plugin cache so the project can keep a stable, inspectable version of the capabilities it depends on.

## Included Plugins

| Plugin | Version | Source cache path | License | Project role |
| --- | --- | --- | --- | --- |
| `remotion` | `1.0.3` | `/Users/dangbei/.codex/plugins/cache/openai-curated-remote/remotion/1.0.3` | MIT | Programmatic video, trailers, explainers, character reels, captions, animation, and audio workflows. |
| `product-design` | `0.1.47` | `/Users/dangbei/.codex/plugins/cache/openai-curated-remote/product-design/0.1.47` | Proprietary | Product research, UX audits, visual directions, URL/image-to-code prototypes, and prototype sharing workflows. |

## Directory Contract

Each child directory is a complete Codex plugin root:

```text
codex_plugins/
  remotion/
    .codex-plugin/plugin.json
    skills/
    assets/
  product-design/
    .codex-plugin/plugin.json
    skills/
    references/
    templates/
    assets/
```

Keep these plugin directories close to their upstream package shape. Project-specific usage notes belong in `workflows/creative_plugins.md` instead of inside the vendored plugin files.

## Using These Plugins

When Codex is working in this repository, use the normal plugin mentions:

```text
@Remotion Create a short character reveal composition for Samir Haddad.
@Product Design Audit the ECHO console hub and propose prototype directions.
```

For local plugin testing or installation flows, point the plugin root at:

```text
codex_plugins/remotion
codex_plugins/product-design
```

## Updating From The Local Cache

To refresh these mirrors from the currently installed Codex plugins:

```bash
rsync -a --delete --exclude '.DS_Store' /Users/dangbei/.codex/plugins/cache/openai-curated-remote/remotion/1.0.3/ codex_plugins/remotion/
rsync -a --delete --exclude '.DS_Store' /Users/dangbei/.codex/plugins/cache/openai-curated-remote/product-design/0.1.47/ codex_plugins/product-design/
```

After updating, check `codex_plugins/*/.codex-plugin/plugin.json` for version changes and adjust this README if needed.
