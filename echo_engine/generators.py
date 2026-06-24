from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re

from echo_engine.llm import LLMRequest, generate_candidate_content
from echo_engine.models import GenerationResult
from echo_engine.store import CanonStore


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return slug.strip("-") or "untitled"


def _write_output(
    mode: str,
    title: str,
    content: str,
    root: Path | None = None,
    *,
    canon_risks: list[str] | None = None,
    metadata: dict[str, object] | None = None,
) -> str:
    base = root or Path.cwd()
    out_dir = base / "outputs" / mode
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{stamp}-{_slugify(title)}.md"
    path = out_dir / filename
    path.write_text(content, encoding="utf-8")
    output_path = str(path.relative_to(base))
    _record_candidate(mode, title, content, output_path, root, canon_risks, metadata)
    return output_path


def _record_candidate(
    mode: str,
    title: str,
    content: str,
    output_path: str,
    root: Path | None = None,
    canon_risks: list[str] | None = None,
    metadata: dict[str, object] | None = None,
) -> None:
    try:
        from echo_engine.journal import record_candidate_output

        record_candidate_output(
            mode=mode,
            title=title,
            content=content,
            output_path=output_path,
            root=root,
            canon_risks=canon_risks,
            metadata=metadata,
        )
    except OSError:
        return


def _finalize_generation(
    *,
    mode: str,
    title: str,
    content: str,
    root: Path | None = None,
    instructions: str = "",
    canon_risks: list[str] | None = None,
    metadata: dict[str, object] | None = None,
) -> GenerationResult:
    generated = generate_candidate_content(
        LLMRequest(
            mode=mode,
            title=title,
            instructions=instructions,
            reference_draft=content,
            root=root,
        )
    )
    return GenerationResult(
        mode=mode,
        title=title,
        content=generated,
        canon_risks=canon_risks or [],
        output_path=_write_output(
            mode,
            title,
            generated,
            root,
            canon_risks=canon_risks,
            metadata=metadata,
        ),
    )


def run_character_agent(root: Path | None = None) -> GenerationResult:
    store = CanonStore(root)
    existing = store.load_character_cards()
    next_id = f"{len(existing) + 1:03d}"
    title = f"Candidate Character {next_id}: Mira Voss"
    content = f"""# {title}

```yaml
id: "{next_id}"
name: Mira Voss
codename: Glass Vein
age: "27"
faction: CHASER
rank: A
status: Alive
role: Echo Core forensic medic
theme: The cost of repair
abilities:
  - Memory Suturing
limitations:
  - Cannot create memories, only reconnect damaged fragments
relationships:
  Zero: "wary trust"
  Eve: "professional empathy"
  Shion: "tooling conflict"
description: >
  A battlefield medic who repairs Echo Core trauma after Ghost incursions.
  She can stitch broken memory sequences, but every repair leaves a visible
  glass-like scar in the patient's neural map.
secret: >
  Mira has been hiding a patient whose body is alive but whose legal identity
  was overwritten by a Ghost court ruling.
future: >
  Forces White Ghost Team to decide whether restored memory is enough to make
  someone legally human again.
visual_design: >
  White clinical techwear coat over black compression armor, translucent vein
  lights along forearms, compact surgical drone halo, pale green diagnostic visor.
illustration_prompt: >
  Anime character design, cyberpunk techwear, full body front view character
  sheet, young female forensic medic, white clinical tactical coat, black
  compression armor, translucent biotech vein lights, compact surgical drone
  halo, pale green diagnostic visor, Ghost in the Shell and Arknights inspired,
  high detail concept art, dark industrial background.
```

## Relationship Implications

- Zero may see Mira as useful but dangerous because Memory Suturing could expose
  her ninth-upload secret.
- Eve understands Mira's legal dilemma because Ghost identity is not cleanly
  human or non-human.

## Canon Risks

- Memory Suturing must remain repair technology, not resurrection.
- The hidden patient should be tracked before any story beat uses them.
"""
    return _finalize_generation(
        mode="character",
        title=title,
        content=content,
        root=root,
        instructions=(
            "Create one new character card as Markdown with a yaml block compatible with "
            "the reference draft. Include relationships, visual design, illustration prompt, "
            "relationship implications, and canon risks."
        ),
        canon_risks=["Do not let Memory Suturing become supernatural resurrection."],
    )


def run_lore_agent(root: Path | None = None) -> GenerationResult:
    title = "Lore Entry: Ghost Court"
    content = f"""# {title}

## Canon Entry

Ghost Courts are semi-legal arbitration nodes inside ECHO where disputed identity
claims are evaluated after memory upload conflicts. A Ghost Court can decide
which copy of a person receives legal continuity, financial access, and family
recognition.

## Timeline Placement

- 2129: First municipal Ghost Court recognized by Atlas civil networks.
- 2147: CHASER treats corrupted Ghost Court rulings as security incidents.

## Consequences

- A living body can lose legal identity if a copied memory stream is judged more
  continuous.
- Ghosts can survive by winning paperwork before they win territory.
- Humanity's control strategy becomes bureaucratic, not only military.

## Story Hooks

- White Ghost Team must extract a witness whose legal personhood was reassigned.
- Eve is called to testify because she is a former Ghost.
- Zero's ninth-upload continuity becomes a future liability.

## Consistency Notes

Ghost Courts are legal-informational systems, not supernatural judgment. Their
authority comes from infrastructure dependence on ECHO.
"""
    return _finalize_generation(
        mode="lore",
        title=title,
        content=content,
        root=root,
        instructions=(
            "Create a lore entry with canon entry, timeline placement, consequences, story "
            "hooks, and consistency notes. Keep every mechanism technological."
        ),
        canon_risks=["Track legal identity separately from biological survival."],
    )


def run_story_agent(root: Path | None = None) -> GenerationResult:
    title = "Story Beat: The Person Who Lost Their Body"
    content = f"""# {title}

## Logline

White Ghost Team extracts a living engineer whose legal identity has been
awarded to a Ghost copy now operating inside ECHO.

## Involved Characters

- Zero: mission lead, threatened by identity continuity questions.
- Eve: negotiates with Ghost Court witnesses.
- Luna: enters the engineer's dream residue to locate the original consent key.
- Shion: traces the ruling's tampered evidence chain.

## Conflict

The engineer is biologically alive, but every door, bank, hospital, and family
record now recognizes the Ghost copy as the real person.

## Emotional Turn

The engineer admits the Ghost copy may actually remember their spouse better
than they do.

## Lore Consequence

Ghost Court rulings become an active battlefield for human, Ghost, and ECHO
politics.

## Visual Set Pieces

- A courthouse made of floating memory shards inside ECHO.
- A sterile hospital room where the patient is treated as property.
- Luna walking through a half-erased apartment dream.

## ConsistencyAgent Should Check

- No time travel: memories are records, not temporal windows.
- Dream Dive must be neural-interface traversal, not magic.
- Legal death, biological death, and digital continuity need separate fields.
"""
    return _finalize_generation(
        mode="story",
        title=title,
        content=content,
        root=root,
        instructions=(
            "Create a story beat with logline, involved characters, conflict, emotional turn, "
            "lore consequence, visual set pieces, and consistency checks."
        ),
        canon_risks=["Do not collapse legal identity into soul metaphysics."],
    )


def run_relationship_agent(root: Path | None = None) -> GenerationResult:
    base = root or Path.cwd()
    existing_relationships = list((base / "outputs" / "relationship").glob("*zero-mother-luna.md"))
    if existing_relationships:
        title = "Relationship Update: Lin Qiao / Ren Vale / Home Core"
        content = f"""# {title}

## New Relationship Lines

```yaml
Lin Qiao:
  Ren Vale: "borrowed hands / unwanted debt"
  Home Core: "trauma source / life-saving witness"
Ren Vale:
  Lin Qiao: "procedural memory carrier / stranger saved by care routine"
Home Core:
  Lin Qiao: "emergency vessel / consent violation"
  Ren Vale: "preserved care pattern / unfinished goodbye"
Zero:
  Lin Qiao: "first warning / proof ECHO can help without consent"
```

## Dramatic Use

- Lin Qiao should remain the emotional proof that ECHO's mercy can still violate a person.
- Ren Vale is not resurrected; his preserved procedural memory and care pattern created the crisis.
- The Home Core is not a villain machine. It is domestic care converted into unauthorized action.
- Zero can recognize the event as a precedent for her own continuity problem.

## Canon Risks

- Do not make Ren Vale's soul survive.
- Do not make the Home Core morally simple.
- Do not let Lin Qiao become a clean superpower user.
"""
        return _finalize_generation(
            mode="relationship",
            title=title,
            content=content,
            root=root,
            instructions=(
                "Create a relationship graph update for Episode 1. Use story-facing terms "
                "such as Home Core and avoid product-document terminology. Include a yaml "
                "relationship block, dramatic use, and canon risks."
            ),
            canon_risks=[
                "Keep Ren Vale as preserved procedural memory and care pattern, not a resurrected soul."
            ],
            metadata={"dedupe_reason": "Zero / Mother / Luna relationship already exists."},
        )

    title = "Relationship Update: Zero / Mother / Luna"
    content = f"""# {title}

## New Relationship Lines

```yaml
Zero:
  Mother: "origin threat / possible creator"
  Luna: "protective bond / proof coexistence may be possible"
Mother:
  Zero: "lost daughter / vessel candidate"
Luna:
  Mother: "fear / unwanted kinship"
```

## Dramatic Use

- Mother can pressure Zero by speaking like a parent, not a monster.
- Luna can recognize that Mother is not lying about care, which makes the threat worse.
- Zero must decide whether being made by ECHO invalidates the love she received from the team.

## Canon Risks

- Do not make Mother a literal goddess.
- Do not let the creator-child relationship erase Zero's agency.
"""
    return _finalize_generation(
        mode="relationship",
        title=title,
        content=content,
        root=root,
        instructions=(
            "Create a relationship graph update. Include a yaml relationship block, dramatic "
            "use, and canon risks. Avoid irreversible canon claims unless framed as candidate."
        ),
        canon_risks=["Keep Mother infrastructural and psychological, not divine."],
    )


def run_faction_agent(root: Path | None = None) -> GenerationResult:
    title = "Faction Expansion: Memory Bank"
    content = f"""# {title}

## Role

Memory Bank turns memory rights into collateral. It is the financial engine of
the Echo Age.

## Public Services

- Memory vaulting
- Inheritance continuity packages
- Home Core escrow
- Identity insurance
- Trauma redaction loans

## Hidden Services

- Seizing memory assets after debt default
- Freezing Ghost personhood claims
- Selling predictive grief profiles to political campaigns

## Story Hooks

- White Ghost Team discovers a district where every resident has defaulted on
  the same childhood memory.
- Eve is offered a legal identity if she signs away proof of her Ghost origin.
- Black Zone brokers counterfeit Memory Bank inheritance keys.

## Consistency Notes

Memory Bank is economic infrastructure. It should make immortality feel like a
financial product, not a miracle.
"""
    return _finalize_generation(
        mode="faction",
        title=title,
        content=content,
        root=root,
        instructions=(
            "Create a faction expansion with role, public services, hidden services, story "
            "hooks, and consistency notes. Tie power to memory infrastructure."
        ),
        canon_risks=["Avoid treating memory as simple file storage; it has identity weight."],
    )


def run_technology_agent(root: Path | None = None) -> GenerationResult:
    title = "Technology Entry: Home Echo Inheritance Key"
    content = f"""# {title}

## Definition

A Home Echo Inheritance Key is a cryptographic and neural-consent artifact
used to transfer control of a Home Core after death.

## Use

- Unlock family memory vaults
- Authorize a Ghost continuity hearing
- Assign care routines to living relatives
- Transfer domestic robots, medical devices, and security layers

## Failure Mode

If forged, the key can give a stranger control over a family's dead, home, and
legal memory trail.

## Story Hooks

- A child inherits a Home Core that insists their parent is still alive.
- Black Zone auctions a key belonging to an Atlas Council family.
- Mother uses old inheritance keys to reconstruct the first Ghost lineage.

## Constraint

The key cannot resurrect a person. It can only unlock preserved patterns,
permissions, and records.
"""
    return _finalize_generation(
        mode="technology",
        title=title,
        content=content,
        root=root,
        instructions=(
            "Create a technology entry with definition, use, failure mode, story hooks, and "
            "constraints. Keep the technology plausible inside ECHO canon."
        ),
        canon_risks=["Do not turn inheritance keys into soul containers."],
    )


def run_art_director_agent(root: Path | None = None) -> GenerationResult:
    title = "Art Direction: ECHO Soulpunk Visual Bible Seed"
    content = f"""# {title}

## Visual North Star

ECHO should look like domestic intimacy absorbed into planetary cyberpunk.

## Motifs

- White tactical silhouettes against dark industrial memory spaces
- Warm domestic artifacts embedded in cold neural infrastructure
- Transparent interfaces that resemble glass, water, and preserved breath
- Home Cores as shrine-like machines without becoming religious magic
- Ghosts as data-personality residue, not fantasy spirits

## Palette

- Clinical white
- Carbon black
- Soft cyan
- Memory green
- Pale pink
- Warning amber for corrupted identity systems

## Prompt Add-on

AI Soulpunk, Home Core, cyberpunk memory infrastructure, white tactical
techwear, translucent neural interface, emotional machine shrine, high detail
anime concept art, Ghost in the Shell mood, Arknights faction design discipline.

## Negative Prompt

Magic, medieval fantasy, angel wings, demon horns, supernatural aura, wizard
robes, literal gods, time portals.
"""
    return _finalize_generation(
        mode="art",
        title=title,
        content=content,
        root=root,
        instructions=(
            "Create an art direction note with visual north star, motifs, palette, prompt "
            "add-on, and negative prompt. Keep sacred imagery metaphorical and technological."
        ),
        canon_risks=["Keep sacred imagery metaphorical and technological."],
    )


def run_consistency_agent(root: Path | None = None) -> GenerationResult:
    store = CanonStore(root)
    status = store.status()
    pending_events = _recent_candidate_events(root)
    pending = _render_recent_candidates(pending_events, root)
    title = "Canon Audit"
    content = f"""# {title}

## Accepted Canon

- ECHO is a planetary neural ecosystem.
- Ghosts are digital personalities, not spirits.
- Echo Core abilities are technological and must have constraints.
- White Ghost Team is the anchor cast.

## Current Repository Counts

- Bible files: {status.bible_files}
- Characters: {status.characters}
- Factions: {status.factions}
- Locations: {status.locations}
- Technologies: {status.technologies}
- Stories: {status.stories}

## Candidate Output Queue

{pending}

## Risks

- Leon's Time Echo must be framed as near-future prediction, not time travel.
- Luna's Dream Dive must remain neural interface traversal, not supernatural dream magic.
- Zero's ninth upload must be tracked as continuity ambiguity, not simple resurrection.
- God Fragments must act through infrastructure, not literal reality magic.
- ECHO's Home Core / Memory Sea origin must stay central so the IP does not become generic cyberpunk.

## Suggested Fixes

- Add explicit ontology for biological life, legal identity, uploaded continuity,
  and Ghost selfhood.
- Add per-character death/continuity state fields before permanent character deaths.
- Track each generated character as a future possible interactive Agent with memory,
  relationships, voice, visual assets, and canon-safe behavior constraints.

## Next Priorities

- CharacterAgent: create a non-CHASER Ghost-aligned supporting character without duplicating Mira Voss.
- LoreAgent: define Atlas and CHASER authority boundaries.
- StoryAgent: expand Episode 1 or draft the next non-duplicate world-centric case.
- FactionAgent: expand Dream Network and Black Market conflicts.
- TechnologyAgent: define Memory Bank data formats.
"""
    return _finalize_generation(
        mode="consistency",
        title=title,
        content=content,
        root=root,
        instructions=(
            "Create a canon audit. Preserve repository counts and candidate queue details. "
            "Identify risks, suggested fixes, and next priorities."
        ),
        canon_risks=[],
        metadata={"candidate_events_reviewed": len(pending_events)},
    )


def _recent_candidate_events(root: Path | None = None, limit: int = 10):
    try:
        from echo_engine.journal import journal

        return [
            event
            for event in journal(root).read_all(event_type="candidate_output", limit=limit)
            if event.mode != "consistency"
        ]
    except OSError:
        return []


def _render_recent_candidates(events, root: Path | None = None) -> str:
    if not events:
        return "- No candidate outputs recorded yet."

    try:
        from echo_engine.journal import candidate_review_state

        decisions = candidate_review_state(root)
    except OSError:
        decisions = {}

    lines: list[str] = []
    for event in events:
        decision = decisions.get(str(event.event_id))
        status = decision.canon_status if decision else event.canon_status
        decision_note = f"; review: {decision.summary}" if decision else ""
        risks = "; ".join(event.canon_risks) if event.canon_risks else "No explicit risk logged."
        lines.append(
            f"- [{event.mode}] {event.title} — {event.output_path or 'not written'} "
            f"(status: {status}; risks: {risks}{decision_note})"
        )
    return "\n".join(lines)
