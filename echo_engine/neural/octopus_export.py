from __future__ import annotations

import json
from pathlib import Path

from echo_engine.models import CharacterCard
from echo_engine.store import CanonStore


def export_octopus_agents(
    *,
    root: Path | None = None,
    output_dir: Path | None = None,
) -> list[Path]:
    base = root or Path.cwd()
    store = CanonStore(base)
    target = output_dir or (base / "outputs" / "octopus_agents")
    target.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for card in store.load_character_cards():
        agent_id = f"echo_{card.name.lower()}"
        agent_dir = target / agent_id
        core = agent_dir / "agent-core"
        core.mkdir(parents=True, exist_ok=True)
        (agent_dir / "sessions").mkdir(exist_ok=True)
        (agent_dir / "skills").mkdir(exist_ok=True)

        files = {
            core / "SOUL.md": _soul(card),
            core / "IDENTITY.md": _identity(card),
            core / "MEMORY.md": _memory(card),
            core / "AGENTS.md": _rules(card),
            core / "tool-registry.jsonc": _tool_registry(),
            agent_dir / "profile.jsonc": _profile(agent_id, card),
        }
        for path, text in files.items():
            path.write_text(text, encoding="utf-8")
            written.append(path)
    return written


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
"""


def _identity(card: CharacterCard) -> str:
    return f"""# Identity

- Name: {card.name}
- Codename: {card.codename or card.name}
- Role: {card.role or "Unknown"}
- Faction: {card.faction or "Unknown"}
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

Growth memories should be appended here after event simulations are canonized.
"""


def _rules(card: CharacterCard) -> str:
    return """# Character-Agent Rules

- Stay inside ECHO canon.
- No magic, supernatural powers, multiverse, or time travel.
- All abilities must be explained through Echo Core, biotech, neural interfaces,
  household AI cores, memory systems, city infrastructure, or distributed computation.
- React as a person, not as a narrator.
- Preserve your own goals and relationships, but accept World Brain audit.
"""


def _tool_registry() -> str:
    return """{
  // Minimal read/write shell for future Octopus integration.
  "arms": ["shell", "fs_writer"],
  "skills": []
}
"""


def _profile(agent_id: str, card: CharacterCard) -> str:
    profile = {
        "id": agent_id,
        "templateId": agent_id,
        "name": f"{card.name} / {card.codename or card.name}",
        "description": card.description,
        "icon": "◌",
        "tags": ["echo-universe", "character-agent", card.faction or "unknown"],
        "model": None,
        "systemPrompt": {
            "includeMemoryMd": True,
            "includeUserMd": False,
            "includeAgentsMd": True,
        },
    }
    return "// ECHO Universe Octopus agent profile\n" + json.dumps(
        profile,
        ensure_ascii=False,
        indent=2,
    )
