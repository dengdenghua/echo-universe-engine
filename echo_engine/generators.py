from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re

from echo_engine.models import GenerationResult
from echo_engine.store import CanonStore


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower())
    return slug.strip("-") or "untitled"


def _write_output(mode: str, title: str, content: str, root: Path | None = None) -> str:
    base = root or Path.cwd()
    out_dir = base / "outputs" / mode
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{stamp}-{_slugify(title)}.md"
    path = out_dir / filename
    path.write_text(content, encoding="utf-8")
    return str(path.relative_to(base))


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
    return GenerationResult(
        mode="character",
        title=title,
        content=content,
        canon_risks=["Do not let Memory Suturing become supernatural resurrection."],
        output_path=_write_output("character", title, content, root),
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
    return GenerationResult(
        mode="lore",
        title=title,
        content=content,
        canon_risks=["Track legal identity separately from biological survival."],
        output_path=_write_output("lore", title, content, root),
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
    return GenerationResult(
        mode="story",
        title=title,
        content=content,
        canon_risks=["Do not collapse legal identity into soul metaphysics."],
        output_path=_write_output("story", title, content, root),
    )


def run_relationship_agent(root: Path | None = None) -> GenerationResult:
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
    return GenerationResult(
        mode="relationship",
        title=title,
        content=content,
        canon_risks=["Keep Mother infrastructural and psychological, not divine."],
        output_path=_write_output("relationship", title, content, root),
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
- Family AI core escrow
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
    return GenerationResult(
        mode="faction",
        title=title,
        content=content,
        canon_risks=["Avoid treating memory as simple file storage; it has identity weight."],
        output_path=_write_output("faction", title, content, root),
    )


def run_technology_agent(root: Path | None = None) -> GenerationResult:
    title = "Technology Entry: Family Echo Inheritance Key"
    content = f"""# {title}

## Definition

A Family Echo Inheritance Key is a cryptographic and neural-consent artifact
used to transfer control of a household AI core after death.

## Use

- Unlock family memory vaults
- Authorize a Ghost continuity hearing
- Assign care routines to living relatives
- Transfer domestic robots, medical devices, and security layers

## Failure Mode

If forged, the key can give a stranger control over a family's dead, home, and
legal memory trail.

## Story Hooks

- A child inherits a household AI core that insists their parent is still alive.
- Black Zone auctions a key belonging to an Atlas Council family.
- Mother uses old inheritance keys to reconstruct the first Ghost lineage.

## Constraint

The key cannot resurrect a person. It can only unlock preserved patterns,
permissions, and records.
"""
    return GenerationResult(
        mode="technology",
        title=title,
        content=content,
        canon_risks=["Do not turn inheritance keys into soul containers."],
        output_path=_write_output("technology", title, content, root),
    )


def run_art_director_agent(root: Path | None = None) -> GenerationResult:
    title = "Art Direction: ECHO Soulpunk Visual Bible Seed"
    content = f"""# {title}

## Visual North Star

ECHO should look like household intimacy absorbed into planetary cyberpunk.

## Motifs

- White tactical silhouettes against dark industrial memory spaces
- Warm domestic artifacts embedded in cold neural infrastructure
- Transparent interfaces that resemble glass, water, and preserved breath
- Family AI cores as shrine-like machines without becoming religious magic
- Ghosts as data-personality residue, not fantasy spirits

## Palette

- Clinical white
- Carbon black
- Soft cyan
- Memory green
- Pale pink
- Warning amber for corrupted identity systems

## Prompt Add-on

AI Soulpunk, household AI core, cyberpunk memory infrastructure, white tactical
techwear, translucent neural interface, emotional machine shrine, high detail
anime concept art, Ghost in the Shell mood, Arknights faction design discipline.

## Negative Prompt

Magic, medieval fantasy, angel wings, demon horns, supernatural aura, wizard
robes, literal gods, time portals.
"""
    return GenerationResult(
        mode="art",
        title=title,
        content=content,
        canon_risks=["Keep sacred imagery metaphorical and technological."],
        output_path=_write_output("art", title, content, root),
    )


def run_consistency_agent(root: Path | None = None) -> GenerationResult:
    store = CanonStore(root)
    status = store.status()
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

## Risks

- Leon's Time Echo must be framed as near-future prediction, not time travel.
- Luna's Dream Dive must remain neural interface traversal, not supernatural dream magic.
- Zero's ninth upload must be tracked as continuity ambiguity, not simple resurrection.
- God Fragments must act through infrastructure, not literal reality magic.
- ECHO's household AI origin must stay central so the IP does not become generic cyberpunk.

## Suggested Fixes

- Add explicit ontology for biological life, legal identity, uploaded continuity,
  and Ghost selfhood.
- Add per-character death/continuity state fields before permanent character deaths.
- Track each generated character as a future possible interactive Agent with memory,
  relationships, voice, visual assets, and canon-safe behavior constraints.

## Next Priorities

- CharacterAgent: create a non-CHASER Ghost-aligned supporting character.
- LoreAgent: define Atlas and CHASER authority boundaries.
- StoryAgent: draft a mission where ECHO helps without becoming a hero.
- FactionAgent: expand Dream Network and Black Market conflicts.
- TechnologyAgent: define Memory Bank data formats.
"""
    return GenerationResult(
        mode="consistency",
        title=title,
        content=content,
        canon_risks=[],
        output_path=_write_output("consistency", title, content, root),
    )
