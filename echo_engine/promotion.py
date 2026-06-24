from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from echo_engine.generators import _slugify
from echo_engine.models import CharacterCard
from echo_engine.journal import (
    JournalEvent,
    candidate_promotion_state,
    candidate_review_state,
    journal,
    record_promotion,
)


PROMOTION_TARGETS = {
    "story": "stories",
    "character": "characters",
    "lore": "bible",
    "faction": "factions",
    "technology": "technologies",
    "relationship": "relationships",
}


@dataclass(frozen=True)
class PromotionResult:
    event_id: str
    source_path: str
    promoted_path: str
    mode: str
    title: str


class PromotionError(RuntimeError):
    pass


def promote_candidate(
    event_id: str,
    *,
    root: Path | None = None,
    target_dir: str | None = None,
    filename: str | None = None,
    refresh_octopus_agents: bool = True,
) -> PromotionResult:
    base = root or Path.cwd()
    event = _candidate_event(event_id, root)
    decision = candidate_review_state(root).get(str(event.event_id))
    if decision is None or decision.canon_status != "accepted":
        raise PromotionError("candidate must be accepted before promotion")
    existing_promotion = candidate_promotion_state(root).get(str(event.event_id))
    if existing_promotion:
        promoted_path = existing_promotion.output_path or "unknown target"
        raise PromotionError(f"candidate already promoted: {promoted_path}")
    if not event.output_path:
        raise PromotionError("candidate has no output_path")

    source = base / event.output_path
    if not source.is_file():
        raise PromotionError(f"candidate output not found: {event.output_path}")

    target_root = base / (target_dir or _target_dir_for_mode(event.mode))
    target_root.mkdir(parents=True, exist_ok=True)
    target = target_root / (filename or _promotion_filename(event, base))
    if target.exists():
        raise PromotionError(f"promotion target already exists: {target.relative_to(base)}")

    content = source.read_text(encoding="utf-8")
    promoted_content = _promoted_content(event, decision, content)
    target.write_text(promoted_content, encoding="utf-8")
    result = PromotionResult(
        event_id=str(event.event_id),
        source_path=str(source.relative_to(base)),
        promoted_path=str(target.relative_to(base)),
        mode=event.mode,
        title=event.title,
    )
    record_promotion(
        event_id=result.event_id,
        mode=result.mode,
        title=result.title,
        source_path=result.source_path,
        promoted_path=result.promoted_path,
        root=root,
    )
    if refresh_octopus_agents and result.mode == "character":
        _refresh_octopus_agents(root)
    return result


def _refresh_octopus_agents(root: Path | None = None) -> None:
    from echo_engine.neural.octopus_export import export_octopus_agents

    export_octopus_agents(root=root)


def _candidate_event(event_id: str, root: Path | None = None) -> JournalEvent:
    for event in journal(root).read_all(event_type="candidate_output"):
        if str(event.event_id) == event_id:
            return event
    raise PromotionError(f"candidate event not found: {event_id}")


def _target_dir_for_mode(mode: str) -> str:
    try:
        return PROMOTION_TARGETS[mode]
    except KeyError as exc:
        raise PromotionError(f"no promotion target configured for mode: {mode}") from exc


def _promotion_filename(event: JournalEvent, base: Path) -> str:
    slug = _slugify(event.title)
    if event.mode == "character":
        character_data = _extract_yaml_from_output_path(event, base)
        if character_data:
            card = CharacterCard.model_validate(character_data)
            return f"{card.id}_{_slugify(card.name).replace('-', '_')}.md"
    if event.mode == "relationship":
        return f"{slug}.yaml"
    return f"promoted_{slug}.md"


def _promoted_content(event: JournalEvent, decision: JournalEvent, content: str) -> str:
    if event.mode == "character":
        data = _extract_yaml_block(content)
        if data is None:
            raise PromotionError("character candidate does not contain a fenced yaml block")
        card = CharacterCard.model_validate(data)
        return _render_character_card(card, event, decision)
    if event.mode == "relationship":
        data = _extract_yaml_block(content)
        if data is None:
            raise PromotionError("relationship candidate does not contain a fenced yaml block")
        return _render_yaml_promotion(data, event, decision)
    return _promotion_header(event, decision) + content


def _extract_yaml_from_output_path(event: JournalEvent, base: Path) -> dict[str, Any] | None:
    if not event.output_path:
        return None
    path = base / event.output_path
    if not path.exists():
        return None
    return _extract_yaml_block(path.read_text(encoding="utf-8"))


def _extract_yaml_block(content: str) -> dict[str, Any] | None:
    marker = "```yaml"
    if marker not in content:
        return None
    yaml_text = content.split(marker, 1)[1].split("```", 1)[0]
    data = yaml.safe_load(yaml_text) or {}
    return data if isinstance(data, dict) else None


def _render_character_card(
    card: CharacterCard,
    event: JournalEvent,
    decision: JournalEvent,
) -> str:
    data = card.model_dump(exclude_none=True)
    yaml_text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False).strip()
    sections = [
        _promotion_header(event, decision).rstrip(),
        f"# {card.name}",
        "",
        "```yaml",
        yaml_text,
        "```",
    ]
    return "\n".join(sections) + "\n"


def _render_yaml_promotion(
    data: dict[str, Any],
    event: JournalEvent,
    decision: JournalEvent,
) -> str:
    yaml_text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False).strip()
    header = (
        "# Promoted from ECHO candidate output.\n"
        f"# source_event_id: {event.event_id}\n"
        f"# decision_event_id: {decision.event_id}\n"
        f"# source_output: {event.output_path}\n"
        f"# review_reason: {decision.summary}\n"
    )
    return header + yaml_text + "\n"


def _promotion_header(event: JournalEvent, decision: JournalEvent) -> str:
    return (
        "<!--\n"
        "Promoted from ECHO candidate output.\n"
        f"source_event_id: {event.event_id}\n"
        f"decision_event_id: {decision.event_id}\n"
        f"source_output: {event.output_path}\n"
        f"review_reason: {decision.summary}\n"
        "-->\n\n"
    )
