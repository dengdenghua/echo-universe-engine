from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

import yaml

from echo_engine.generators import _write_output
from echo_engine.models import CharacterCard, GenerationResult
from echo_engine.store import CanonStore

STATE_PATH = Path("data/digital_life_state.yaml")


def load_or_seed_life_states(base: Path, cards: list[CharacterCard]) -> dict[str, dict[str, Any]]:
    return _load_or_seed_states(base, cards)


def save_life_states(base: Path, states: dict[str, dict[str, Any]]) -> None:
    _save_states(base, states)


def seed_life_state(card: CharacterCard) -> dict[str, Any]:
    return _seed_state(card)


def run_daily_life_tick(root: Path | None = None) -> GenerationResult:
    base = root or Path.cwd()
    store = CanonStore(base)
    cards = store.load_character_cards()
    states = _load_or_seed_states(base, cards)
    today = date.today().isoformat()
    entries: list[dict[str, Any]] = []
    for card in cards[:8]:
        state = states.setdefault(card.id, _seed_state(card))
        entry = _tick_character(card, state, today)
        entries.append(entry)
    _save_states(base, states)
    title = f"Digital Life Tick {today}"
    content = _render_tick(today, entries)
    return GenerationResult(
        mode="digital_life",
        title=title,
        content=content,
        canon_risks=[
            "Daily life logs are candidate memory, not canon history, until World Brain review."
        ],
        output_path=_write_output(
            "digital_life",
            title,
            content,
            root,
            canon_risks=[
                "Daily life logs are candidate memory, not canon history, until World Brain review."
            ],
            metadata={"date": today, "character_count": len(entries)},
        ),
    )


def _load_or_seed_states(base: Path, cards: list[CharacterCard]) -> dict[str, dict[str, Any]]:
    path = base / STATE_PATH
    if path.exists():
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        states = data.get("characters", {})
        if isinstance(states, dict):
            return states
    return {card.id: _seed_state(card) for card in cards}


def _save_states(base: Path, states: dict[str, dict[str, Any]]) -> None:
    path = base / STATE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"characters": states}
    path.write_text(yaml.safe_dump(payload, allow_unicode=True, sort_keys=True), encoding="utf-8")


def _seed_state(card: CharacterCard) -> dict[str, Any]:
    return {
        "id": card.id,
        "name": card.name,
        "codename": card.codename or card.name,
        "day": 0,
        "current_focus": card.theme or "identity",
        "beliefs": _initial_beliefs(card),
        "goals": _initial_goals(card),
        "friends": dict(card.relationships),
        "memory": [
            f"Day 0: I entered ECHO Universe as {card.name} / {card.codename or card.name}."
        ],
        "diary": [],
        "growth": [],
    }


def _initial_beliefs(card: CharacterCard) -> list[str]:
    base = ["ECHO is not simple evil.", "Identity is more than stored memory."]
    if card.name == "Kane":
        base.append("Protecting the team is worth personal cost.")
    if card.name == "Luna":
        base.append("Ghosts and humans may coexist.")
    if card.name == "Raven":
        base.append("Some threats must be ended before they speak.")
    if card.name == "Zero":
        base.append("Humanity must be protected, even from my own origin.")
    return base


def _initial_goals(card: CharacterCard) -> list[str]:
    if card.name == "Zero":
        return ["Protect White Ghost Team", "Understand my connection to ECHO"]
    if card.name == "Kane":
        return ["Train daily", "Keep Zero alive", "Hold the team together"]
    if card.name == "Luna":
        return ["Explore Dream Network", "Find proof coexistence is possible"]
    if card.name == "Raven":
        return ["Track Black Zone threats", "Protect the team from unseen enemies"]
    return [f"Advance my arc: {card.future or card.theme or 'unwritten'}"]


def _tick_character(card: CharacterCard, state: dict[str, Any], today: str) -> dict[str, Any]:
    state["day"] = int(state.get("day", 0)) + 1
    day = state["day"]
    activity = _daily_activity(card, day)
    memory = f"Day {day}: {activity}"
    diary = _diary_line(card, activity)
    growth = _growth_line(card, day)
    state.setdefault("memory", []).append(memory)
    state.setdefault("diary", []).append({"date": today, "text": diary})
    if growth:
        state.setdefault("growth", []).append({"date": today, "text": growth})
    state["current_focus"] = _next_focus(card, day)
    return {
        "id": card.id,
        "name": card.name,
        "codename": card.codename or card.name,
        "day": day,
        "activity": activity,
        "diary": diary,
        "growth": growth,
        "focus": state["current_focus"],
    }


def _daily_activity(card: CharacterCard, day: int) -> str:
    name = card.name
    if name == "Zero":
        return "studied an abnormal ECHO resonance and heard one unfamiliar voice answer back"
    if name == "Kane":
        return "trained Combat Download under fatigue and checked Zero's field telemetry twice"
    if name == "Eve":
        return "mapped emotional residue from a Ghost witness without reporting every detail to CHASER"
    if name == "Leon":
        return "ran three-second prediction drills until his hands shook"
    if name == "Raven":
        return "entered Black Zone through a dead camera network and returned with a missing-name list"
    if name == "Shion":
        return "taught her nano-swarm to identify forged household AI inheritance keys"
    if name == "Noah":
        return "modeled a 99% extraction route and marked the 1% consequence as unacceptable"
    if name == "Luna":
        return "met a frightened Ghost child inside Dream Network and chose not to erase the contact"
    return f"continued training around {card.theme or 'identity'}"


def _diary_line(card: CharacterCard, activity: str) -> str:
    if card.name == "Zero":
        return f"I told myself it was only signal noise, but {activity}."
    if card.name == "Kane":
        return f"Ten seconds is enough to learn a weapon. It is not enough to say what I mean. Today I {activity}."
    if card.name == "Luna":
        return f"If a dream is where someone can still be afraid, I cannot call it fake. Today I {activity}."
    if card.name == "Raven":
        return f"The dark kept its mouth shut. I did not. Today I {activity}."
    return f"Today I {activity}."


def _growth_line(card: CharacterCard, day: int) -> str:
    if day % 7 != 0:
        return ""
    if card.name == "Zero":
        return "Zero becomes slightly less certain that human and ECHO are separable."
    if card.name == "Kane":
        return "Kane's loyalty shifts from obedience toward chosen protection."
    if card.name == "Luna":
        return "Luna becomes more willing to defend Ghost personhood openly."
    if card.name == "Raven":
        return "Raven delays one kill to verify whether the target is truly hostile."
    return f"{card.name} records a small but lasting change."


def _next_focus(card: CharacterCard, day: int) -> str:
    if day % 7 == 0:
        return "growth review"
    if card.name == "Zero":
        return "ECHO resonance"
    if card.name == "Kane":
        return "training and protection"
    if card.name == "Luna":
        return "Ghost coexistence"
    if card.name == "Raven":
        return "Black Zone surveillance"
    return card.theme or "identity"


def _render_tick(today: str, entries: list[dict[str, Any]]) -> str:
    lines = [f"# Digital Life Tick: {today}", ""]
    lines.extend(
        [
            "These logs are candidate character memory. They become canon only after World Brain review.",
            "",
            "## Character Logs",
            "",
        ]
    )
    for entry in entries:
        lines.extend(
            [
                f"### {entry['name']} / {entry['codename']}",
                "",
                f"- Day: {entry['day']}",
                f"- Focus: {entry['focus']}",
                f"- Activity: {entry['activity']}",
                f"- Diary: {entry['diary']}",
            ]
        )
        if entry["growth"]:
            lines.append(f"- Growth: {entry['growth']}")
        lines.append("")
    lines.extend(
        [
            "## World Brain Notes",
            "",
            "- Do not promote relationship or personality changes automatically.",
            "- Weekly growth lines should be reviewed against canon pacing.",
            "- Major secrets, deaths, betrayals, and romance beats require explicit promotion.",
        ]
    )
    return "\n".join(lines)
