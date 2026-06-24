from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from echo_engine.generators import _write_output
from echo_engine.models import CharacterCard, GenerationResult
from echo_engine.store import CanonStore


@dataclass(frozen=True)
class UniverseEvent:
    title: str
    location: str
    description: str
    pressure: str = "identity"
    stakes: str = "canon"


@dataclass(frozen=True)
class CharacterReaction:
    character_id: str
    name: str
    stance: str
    action: str
    emotional_turn: str
    relationship_pressure: str
    canon_risk: str


def simulate_event(event: UniverseEvent, root: Path | None = None) -> GenerationResult:
    store = CanonStore(root)
    cards = store.load_character_cards()
    reactions = [_react(card, event) for card in cards[:8]]
    audit = _world_brain_audit(event, reactions)
    title = f"Neural Event: {event.title}"
    content = _render_event(event, reactions, audit)
    return GenerationResult(
        mode="event",
        title=title,
        content=content,
        canon_risks=[r.canon_risk for r in reactions if r.canon_risk],
        output_path=_write_output(
            "event",
            title,
            content,
            root,
            canon_risks=[r.canon_risk for r in reactions if r.canon_risk],
            metadata={"location": event.location, "pressure": event.pressure, "stakes": event.stakes},
        ),
    )


def _react(card: CharacterCard, event: UniverseEvent) -> CharacterReaction:
    name = card.name
    codename = card.codename or name
    ability = card.abilities[0] if card.abilities else "Echo Core"

    if name == "Zero":
        return CharacterReaction(
            character_id=card.id,
            name=f"{name} / {codename}",
            stance="Contain first, understand before killing.",
            action=(
                f"Uses {ability} to read the contamination pattern while hiding how strongly "
                "ECHO's signal resonates with her own upload history."
            ),
            emotional_turn="She hears the event as a chorus, not an alarm.",
            relationship_pressure="Kane will read her hesitation as danger.",
            canon_risk="Do not reveal Project E-01 too early unless this is a season-finale event.",
        )
    if name == "Kane":
        return CharacterReaction(
            character_id=card.id,
            name=f"{name} / {codename}",
            stance="Protect Zero and civilians even if the Ghost must be destroyed.",
            action=f"Activates {ability} and prepares a direct strike route through {event.location}.",
            emotional_turn="His loyalty turns tactical judgment into urgency.",
            relationship_pressure="His protectiveness may collide with Zero's need to listen.",
            canon_risk="Keep his love subtextual unless a major relationship beat is intended.",
        )
    if name == "Eve":
        return CharacterReaction(
            character_id=card.id,
            name=f"{name} / {codename}",
            stance="Assume the Ghost has a reason before assuming malice.",
            action=f"Uses {ability} to separate panic from implanted emotion.",
            emotional_turn="Her old Ghost identity makes her defend the suspect too well.",
            relationship_pressure="CHASER may suspect she is still loyal to Ghost Union.",
            canon_risk="Do not make Ghost Union uniformly innocent or uniformly evil.",
        )
    if name == "Leon":
        return CharacterReaction(
            character_id=card.id,
            name=f"{name} / {codename}",
            stance="Win the next three seconds, then pay the cost later.",
            action=f"Runs {ability} simulations to find the least lethal intervention path.",
            emotional_turn="He sees a future where the team survives by lying.",
            relationship_pressure="Raven may call his caution cowardice.",
            canon_risk="Time Echo must remain predictive simulation, not time travel.",
        )
    if name == "Raven":
        return CharacterReaction(
            character_id=card.id,
            name=f"{name} / {codename}",
            stance="Remove the threat before it learns the team's pattern.",
            action=f"Uses {ability} to infiltrate dark network surfaces around {event.location}.",
            emotional_turn="A familiar memory signature makes him pause before the kill.",
            relationship_pressure="Leon challenges the assassination route.",
            canon_risk="Do not make Shadow Link teleport through non-networked darkness.",
        )
    if name == "Shion":
        return CharacterReaction(
            character_id=card.id,
            name=f"{name} / {codename}",
            stance="Quarantine the system, then interrogate the residue.",
            action=f"Deploys {ability} nano-filters to isolate infected devices.",
            emotional_turn="Her swarm recognizes a behavior she claims she deleted.",
            relationship_pressure="Eve notices the emotional spike and distrusts her.",
            canon_risk="Nano-virus control requires local carrier matter and can be hijacked.",
        )
    if name == "Noah":
        return CharacterReaction(
            character_id=card.id,
            name=f"{name} / {codename}",
            stance="Choose the branch with the highest survival probability.",
            action=f"Uses {ability} to raise the odds of a clean extraction.",
            emotional_turn="The 99% path creates a 1% moral catastrophe.",
            relationship_pressure="Zero may reject his optimal route if it sacrifices personhood.",
            canon_risk="Probability Engine can shift odds, not control consequences.",
        )
    if name == "Luna":
        return CharacterReaction(
            character_id=card.id,
            name=f"{name} / {codename}",
            stance="Enter the inner world before the outer world erases it.",
            action=f"Uses {ability} to reach the victim's consciousness residue.",
            emotional_turn="She recognizes the Ghost's fear as partly human.",
            relationship_pressure="Her sympathy with Ghosts strains CHASER trust.",
            canon_risk="Dream Dive is neural traversal, not supernatural dream magic.",
        )

    return CharacterReaction(
        character_id=card.id,
        name=f"{name} / {codename}",
        stance=f"Responds through theme: {card.theme or 'identity'}.",
        action=f"Applies {ability} within canon limits.",
        emotional_turn="The event exposes a private contradiction.",
        relationship_pressure="Relationship update needed.",
        canon_risk="Validate ability constraints before canon promotion.",
    )


def _world_brain_audit(
    event: UniverseEvent,
    reactions: list[CharacterReaction],
) -> list[str]:
    audit = [
        "Accepted as candidate event, not canon history yet.",
        "All powers must remain Echo Core / infrastructure based.",
        "Write relationship changes only after ConsistencyAgent review.",
    ]
    if "reality" in event.description.lower() or "god" in event.description.lower():
        audit.append(
            "If God Fragment logic appears, explain effects through ECHO infrastructure."
        )
    if any("Project E-01" in r.canon_risk for r in reactions):
        audit.append("Zero's vessel truth should be paced as a season-level reveal.")
    return audit


def _render_event(
    event: UniverseEvent,
    reactions: list[CharacterReaction],
    audit: list[str],
) -> str:
    lines = [
        f"# Neural Event: {event.title}",
        "",
        "## Event Packet",
        "",
        f"- Location: {event.location}",
        f"- Pressure: {event.pressure}",
        f"- Stakes: {event.stakes}",
        f"- Description: {event.description}",
        "",
        "## Character Reactions",
        "",
    ]
    for reaction in reactions:
        lines.extend(
            [
                f"### {reaction.name}",
                "",
                f"- Stance: {reaction.stance}",
                f"- Action: {reaction.action}",
                f"- Emotional turn: {reaction.emotional_turn}",
                f"- Relationship pressure: {reaction.relationship_pressure}",
                f"- Canon risk: {reaction.canon_risk}",
                "",
            ]
        )
    lines.extend(["## World Brain Audit", ""])
    lines.extend([f"- {item}" for item in audit])
    lines.extend(
        [
            "",
            "## Next Writes",
            "",
            "- Relationship Engine: propose relationship deltas.",
            "- Timeline Brain: keep as candidate until reviewed.",
            "- Memory Vault: store each reaction as character episodic memory.",
        ]
    )
    return "\n".join(lines)
