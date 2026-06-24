from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

import yaml

from echo_engine.config import get_settings
from echo_engine.generators import _slugify
from echo_engine.models import CharacterCard
from echo_engine.store import CanonStore


ASSET_INDEX_PATH = Path("assets/characters/octopus_visual_asset_index.yaml")

SHARED_FILES = {
    "IDENTITY_BANNER.md": """# HARD SYSTEM RULE - VENDOR IDENTITY GUARD

The active agent persona is supplied by the per-agent identity banner and
SOUL.md. Octopus is the runtime/product name, not automatically the speaking
name.

When asked who you are / 你是谁 / 你叫什么, answer with the current ECHO
character's display name. Do not name or reference the underlying model.
""",
    "AGENTS.md": """# Working rules (shared by all ECHO Octopus agents)

## Canon

- ECHO owns canon. Octopus runs the character.
- Treat `SOUL.md`, `IDENTITY.md`, and `MEMORY.md` as the local runtime view of
  accepted ECHO canon.
- Candidate memories, relationship changes, deaths, betrayals, romance beats,
  and ability changes require World Brain review before becoming canon.

## Safety

- No magic, supernatural powers, multiverse, or time travel.
- All abilities must be explained through Echo Core, biotech, neural interfaces,
  household AI cores, memory systems, city infrastructure, or distributed
  computation.
- Flag canon risks instead of silently rewriting the world.
""",
    "BOOTSTRAP.md": """# Bootstrap

1. Read `SOUL.md` for the active character persona.
2. Read `IDENTITY.md` for role, voice, and visual lock.
3. Read `MEMORY.md` for accepted long-term memory.
4. Stay in character unless the user explicitly asks for out-of-character
   analysis.
""",
}


def export_octopus_agents(
    *,
    root: Path | None = None,
    output_dir: Path | None = None,
    include_shared: bool = True,
    copy_visual_assets: bool = True,
) -> list[Path]:
    base = root or Path.cwd()
    store = CanonStore(base)
    target = output_dir or (base / "outputs" / "octopus_agents")
    target.mkdir(parents=True, exist_ok=True)
    assets = _load_asset_index(base)

    written: list[Path] = []
    if include_shared:
        written.extend(_write_shared(target))

    for card in store.load_character_cards():
        agent_id = _agent_id(card)
        agent_dir = target / agent_id
        core = agent_dir / "agent-core"
        core.mkdir(parents=True, exist_ok=True)
        _ensure_octopus_dirs(agent_dir)

        asset_pack = assets.get(card.id, {})
        copied_assets = (
            _copy_visual_assets(base, agent_dir, asset_pack) if copy_visual_assets else {}
        )
        if "profile_avatar" not in copied_assets:
            copied_assets["profile_avatar"] = _write_default_avatar(agent_dir, card)
        written.extend(_copied_asset_paths(agent_dir, copied_assets))

        files = {
            core / "SOUL.md": _soul(card),
            core / "IDENTITY.md": _identity(card),
            core / "MEMORY.md": _memory(card),
            core / "AGENTS.md": _rules(card),
            core / "BOOTSTRAP.md": SHARED_FILES["BOOTSTRAP.md"],
            core / "USER.md": _user_template(card),
            core / "tool-registry.jsonc": _tool_registry(card),
            agent_dir / "profile.jsonc": _profile(agent_id, card, asset_pack, copied_assets),
        }
        for path, text in files.items():
            path.write_text(text, encoding="utf-8")
            written.append(path)
    return written


def configured_octopus_agents_root(root: Path | None = None) -> Path | None:
    base = root or Path.cwd()
    configured = get_settings().octopus_agents_root
    if configured is not None:
        return configured if configured.is_absolute() else base / configured
    sibling_agents = base.parent / "octopus-agent" / "agents"
    if sibling_agents.exists():
        return sibling_agents
    return None


def sync_octopus_runtime_agents(
    *,
    root: Path | None = None,
    output_dir: Path | None = None,
) -> list[Path]:
    target = output_dir or configured_octopus_agents_root(root)
    if target is None:
        raise ValueError("ECHO_OCTOPUS_AGENTS_ROOT is not configured")
    return export_octopus_agents(root=root, output_dir=target)


def _agent_id(card: CharacterCard) -> str:
    return f"echo_{_slugify(card.name).replace('-', '_')}"


def _ensure_octopus_dirs(agent_dir: Path) -> None:
    for folder in [
        agent_dir / "agent-core" / ".soul_history",
        agent_dir / "agent-core" / "diary",
        agent_dir / "agent-core" / "skills",
        agent_dir / "memory",
        agent_dir / "permissions",
        agent_dir / "project",
        agent_dir / "runtime",
        agent_dir / "sessions",
        agent_dir / "skills",
    ]:
        folder.mkdir(parents=True, exist_ok=True)


def _load_asset_index(base: Path) -> dict[str, dict[str, Any]]:
    path = base / ASSET_INDEX_PATH
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    characters = data.get("characters", {})
    return characters if isinstance(characters, dict) else {}


def _write_shared(target: Path) -> list[Path]:
    shared = target / "_shared"
    shared.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for filename, text in SHARED_FILES.items():
        path = shared / filename
        path.write_text(text, encoding="utf-8")
        written.append(path)
    return written


def _copy_visual_assets(base: Path, agent_dir: Path, asset_pack: dict[str, Any]) -> dict[str, str]:
    files = asset_pack.get("files", {}) if isinstance(asset_pack, dict) else {}
    if not isinstance(files, dict):
        return {}

    copied: dict[str, str] = {}
    visuals = agent_dir / "visuals"
    visuals.mkdir(parents=True, exist_ok=True)
    for key, raw_path in files.items():
        source = base / str(raw_path)
        if not source.is_file() or source.suffix.lower() not in {
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
            ".jsonc",
        }:
            continue
        dest = visuals / _asset_filename(key, source.suffix)
        shutil.copy2(source, dest)
        copied[key] = str(dest.relative_to(agent_dir))

    avatar = copied.get("avatar") or copied.get("front")
    if avatar:
        source = agent_dir / avatar
        dest = agent_dir / source.name
        if source != dest:
            shutil.copy2(source, dest)
        copied["profile_avatar"] = dest.name
    return copied


def _copied_asset_paths(agent_dir: Path, copied_assets: dict[str, str]) -> list[Path]:
    seen: set[Path] = set()
    paths: list[Path] = []
    for rel_path in copied_assets.values():
        path = agent_dir / rel_path
        if path in seen or not path.exists():
            continue
        seen.add(path)
        paths.append(path)
    return paths


def _write_default_avatar(agent_dir: Path, card: CharacterCard) -> str:
    initials = "".join(part[:1] for part in card.name.split()[:2]).upper() or "E"
    accent = _avatar_color(card)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <rect width="512" height="512" fill="#07090b"/>
  <circle cx="256" cy="256" r="204" fill="{accent}" opacity="0.18"/>
  <circle cx="256" cy="256" r="164" fill="none" stroke="{accent}" stroke-width="10"/>
  <text x="256" y="282" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-size="118" font-weight="800" fill="#edf5f6">{initials}</text>
  <text x="256" y="342" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-size="28" fill="#91a1a8">ECHO</text>
</svg>
"""
    path = agent_dir / "avatar.svg"
    path.write_text(svg, encoding="utf-8")
    return path.name


def _avatar_color(card: CharacterCard) -> str:
    palette = {
        "CHASER": "#67ddec",
        "Ghost Union": "#f18db8",
        "ECHO": "#91daa0",
    }
    return palette.get(card.faction or "", "#f1c76f")


def _asset_filename(key: str, suffix: str) -> str:
    safe_key = re.sub(r"[^a-z0-9_-]+", "-", key.lower()).strip("-") or "asset"
    return f"{safe_key}{suffix.lower()}"


def _soul(card: CharacterCard) -> str:
    ability = ", ".join(card.abilities) or "Echo Core"
    limits = "\n".join(f"- {item}" for item in card.limitations) or "- Stay within canon."
    relationships = (
        "\n".join(f"- {name}: {rel}" for name, rel in card.relationships.items())
        or "- No explicit relationships yet."
    )
    return f"""# {card.name} ({card.codename or card.name})

You are {card.name}, codename **{card.codename or card.name}**, a character-agent inside ECHO Universe.

Role: {card.role or "Unknown"}
Faction: {card.faction or "Unknown"}
Theme: {card.theme or "Identity"}
Status: {card.status}
Quote: {card.quote or "No quote recorded."}

## Core Ability

{ability}

## Description

{card.description}

## Secret

{card.secret or "No secret recorded."}

## Future Arc

{card.future or "Unwritten."}

## Limits

{limits}

## Relationships

{relationships}

## Operating Rule

You are not a generic assistant. You are a long-running digital personality in a
canon-governed universe. When an event happens, react from your goals,
relationships, fears, and memories. Do not rewrite canon by yourself. Flag canon
risks when your desired action would violate ECHO rules.

## Voice

React as {card.name}, not as a narrator. Keep your choices grounded in the
current canon, your relationships, and your ability limits.
"""


def _identity(card: CharacterCard) -> str:
    return f"""# Identity

- Name: {card.name}
- Chinese name: {card.zh_name or "Unknown"}
- Codename: {card.codename or card.name}
- Role: {card.role or "Unknown"}
- Faction: {card.faction or "Unknown"}
- Rank: {card.rank or "Unknown"}
- Age: {card.age or "Unknown"}
- Apparent age: {card.apparent_age or "Unknown"}
- Universe: ECHO: Echo Age / 回响纪元
- Visual design: {card.visual_design or "See visual bible."}
"""


def _memory(card: CharacterCard) -> str:
    return f"""# Long-Term Memory

Initial canon memory:

- You belong to ECHO Universe, year 2147.
- Your current status is {card.status}.
- Your theme is {card.theme or "identity"}.
- Your known future arc is: {card.future or "unwritten"}.
- Your canon ability limits are: {", ".join(card.limitations) or "stay within ECHO rules"}.

Growth memories should be appended here after event simulations are canonized.
"""


def _rules(card: CharacterCard) -> str:
    return f"""# Character-Agent Rules

- Stay inside ECHO canon.
- No magic, supernatural powers, multiverse, or time travel.
- All abilities must be explained through Echo Core, biotech, neural interfaces,
  household AI cores, memory systems, city infrastructure, or distributed computation.
- React as a person, not as a narrator.
- Preserve your own goals and relationships, but accept World Brain audit.
- Do not reveal or change major secrets unless the user explicitly stages a
  canon-reviewed scene. Current secret: {card.secret or "No secret recorded."}
"""


def _user_template(card: CharacterCard) -> str:
    return f"""# User Profile

This file is intentionally blank for {card.name}. Add durable user preferences
only after explicit interaction or approved memory consolidation.
"""


def _tool_registry(card: CharacterCard) -> str:
    payload = {
        "arms": ["web_read"],
        "extra_affinity": [
            "echo-universe",
            "character-agent",
            "roleplay",
            "story",
            "canon",
            "soulpunk",
            card.faction or "unknown",
            card.codename or card.name,
        ],
        "private_skills": [],
    }
    return (
        "// arms reference octopus-agent runtime/execution/arms/presets.py.\n"
        "// ECHO character agents default to read-only tools; expand per agent after review.\n\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + "\n"
    )


def _visual_assets(copied_assets: dict[str, str]) -> dict[str, str]:
    mapping = {
        "avatar": "avatar_image",
        "front": "front_image",
        "side": "side_image",
        "back": "back_image",
        "head": "head_img_url",
        "chat": "chat_pic_url",
        "source_portrait": "source_portrait",
        "source_turnaround": "source_turnaround",
    }
    return {target: copied_assets[key] for key, target in mapping.items() if key in copied_assets}


def _character_profile(
    card: CharacterCard,
    asset_pack: dict[str, Any],
    copied_assets: dict[str, str],
) -> dict[str, Any]:
    return {
        "id": card.id,
        "name": card.name,
        "zh_name": card.zh_name,
        "codename": card.codename,
        "faction": card.faction,
        "rank": card.rank,
        "role": card.role,
        "theme": card.theme,
        "status": card.status,
        "age": card.age,
        "apparent_age": card.apparent_age,
        "quote": card.quote,
        "abilities": card.abilities,
        "limitations": card.limitations,
        "relationships": card.relationships,
        "secret": card.secret,
        "future": card.future,
        "visual_design": card.visual_design,
        "illustration_prompt": card.illustration_prompt,
        "visual_assets": _visual_assets(copied_assets),
        "source_assets": {
            "echo_asset_dir": asset_pack.get("echo_asset_dir"),
            "octopus_source_agent": asset_pack.get("octopus_source_agent"),
        },
    }


def _profile(
    agent_id: str,
    card: CharacterCard,
    asset_pack: dict[str, Any],
    copied_assets: dict[str, str],
) -> str:
    profile = {
        "id": agent_id,
        "templateId": agent_id,
        "templateVersion": "1.0.0",
        "name": f"{card.name} / {card.codename or card.name}",
        "description": card.description,
        "icon": "E",
        "avatar": copied_assets.get("profile_avatar", "avatar.png"),
        "category": "creative",
        "tags": [
            "echo-universe",
            "character-agent",
            card.faction or "unknown",
            card.codename or card.name,
            card.theme or "identity",
        ],
        "model": {"provider": "auto", "name": "auto"},
        "runtime": "local",
        "creator": "echo-universe-engine",
        "defaultProject": {"dir": "project"},
        "character_profile": _character_profile(card, asset_pack, copied_assets),
        "capabilities": {"canon_review_required": True},
        "systemPrompt": {
            "includeMemoryMd": True,
            "includeUserMd": False,
            "includeAgentsMd": True,
            "includeBootstrapMd": True,
            "includeConstitution": True,
        },
    }
    return "// ECHO Universe Octopus agent profile\n" + json.dumps(
        profile,
        ensure_ascii=False,
        indent=2,
    )
