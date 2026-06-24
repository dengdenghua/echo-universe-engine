from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

CONFIG_PATH = Path("integrations/octopus_ecosystem.yaml")


def load_octopus_ecosystem(root: Path | None = None) -> dict[str, Any]:
    base = root or Path.cwd()
    path = base / CONFIG_PATH
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        msg = f"{CONFIG_PATH} must contain a YAML mapping."
        raise ValueError(msg)
    return data


def render_octopus_ecosystem_plan(root: Path | None = None) -> str:
    config = load_octopus_ecosystem(root)
    repos = config.get("repositories", {})
    layers = config.get("layers", {})
    flows = config.get("flows", {})
    boundaries = config.get("canon_boundaries", {})
    doctrine = config.get("product_doctrine", {})
    realm_governance = config.get("realm_governance", {})

    lines = [
        "# Octopus Ecosystem Integration Plan",
        "",
        f"- Ecosystem: {config.get('ecosystem', 'octopus')}",
        f"- Mode: {config.get('mode', 'neural_universe')}",
        f"- Version: {config.get('version', '0.1')}",
        f"- Architecture codex: {config.get('architecture_codex', 'unset')}",
        "",
        "## Repository Roles",
        "",
    ]
    for repo_id, repo in repos.items():
        lines.extend(
            [
                f"### {repo_id}",
                "",
                f"- Role: {repo.get('role', 'unknown')}",
                f"- Default path: {repo.get('default_path', 'unset')}",
            ]
        )
        owned = repo.get("owns") or repo.get("reuses") or []
        if owned:
            lines.append("- Owns/Reuses:")
            lines.extend(f"  - {item}" for item in owned)
        lines.append("")

    if doctrine:
        lines.extend(["## Product Doctrine", ""])
        if doctrine.get("category"):
            lines.append(f"- Category: {doctrine.get('category')}")
        if doctrine.get("not_category"):
            lines.append(f"- Not category: {doctrine.get('not_category')}")
        if doctrine.get("north_star"):
            lines.append(f"- North star: {doctrine.get('north_star')}")
        lines.append("")
        for section_id in ("mvp_loop", "success_criteria"):
            items = doctrine.get(section_id, [])
            if not items:
                continue
            title = section_id.replace("_", " ").title()
            lines.extend([f"### {title}", ""])
            lines.extend(f"- {item}" for item in items)
            lines.append("")

    if realm_governance:
        lines.extend(["## Realm Governance", ""])
        for key in ("source", "reviewers_source", "route_api", "rule"):
            if realm_governance.get(key):
                lines.append(f"- {key.replace('_', ' ').title()}: {realm_governance.get(key)}")
        hierarchy = realm_governance.get("hierarchy", [])
        if hierarchy:
            lines.append(f"- Hierarchy: {' -> '.join(hierarchy)}")
        routing = realm_governance.get("impact_routing", {})
        if routing:
            lines.extend(["", "### Impact Routing", ""])
            lines.extend(f"- {scope}: {approval}" for scope, approval in routing.items())
        lines.append("")

    lines.extend(["## Neural Universe Layers", ""])
    for layer_id, layer in layers.items():
        writes = ", ".join(layer.get("writes_to", [])) or "none"
        lines.extend(
            [
                f"### {layer_id}",
                "",
                f"- Owner: {layer.get('owner', 'unknown')}",
                f"- Runtime: {layer.get('runtime', 'local')}",
                f"- Storage: {layer.get('storage', 'local')}",
                f"- Purpose: {layer.get('purpose', '')}",
                f"- Writes to: {writes}",
                "",
            ]
        )

    lines.extend(["## Operating Flows", ""])
    for flow_id, flow in flows.items():
        lines.extend(
            [
                f"### {flow_id}",
                "",
                f"- Schedule: {flow.get('schedule', 'manual')}",
                f"- Runner: `{flow.get('runner', 'unset')}`",
                f"- Status: {flow.get('status', 'unknown')}",
                f"- Approval: {flow.get('approval', 'unknown')}",
                "",
            ]
        )

    lines.extend(["## Canon Boundaries", ""])
    for boundary_id, items in boundaries.items():
        lines.append(f"### {boundary_id}")
        lines.append("")
        lines.extend(f"- {item}" for item in items)
        lines.append("")

    lines.extend(
        [
            "## Implementation Rule",
            "",
            "ECHO owns canon. Octopus runs the nervous system. Mobile and storage layers extend sensing, memory, and assets without rewriting canon directly.",
        ]
    )
    return "\n".join(lines)


def ecosystem_paths(root: Path | None = None) -> dict[str, Path]:
    config = load_octopus_ecosystem(root)
    repos = config.get("repositories", {})
    return {
        repo_id: Path(str(repo.get("default_path", "")))
        for repo_id, repo in repos.items()
        if repo.get("default_path")
    }
