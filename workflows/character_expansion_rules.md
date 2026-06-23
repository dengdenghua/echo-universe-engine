# Character Expansion Rules

ECHO Universe should scale from 8 anchor characters to 50 characters in Month 1, then 300+ characters by Month 6.

The goal is not to generate random profiles. Every character must create new pressure on identity, memory, Ghost personhood, ECHO infrastructure, or the main cast.

## Character Tiers

## S Tier

Use for season anchors, faction faces, major antagonists, and characters who can carry a spin-off.

Requirements:

- clear ideological conflict
- unique silhouette
- season-level secret or wound
- relationship to at least three major entities
- ability with hard cost
- long-term Agent potential
- visual prompt
- quote

Month 1 target:

10 S-tier characters.

## A Tier

Use for major supporting characters, arc antagonists, faction operators, Ghost Court figures, Memory Bank executives, CHASER specialists, Mars leaders, and Black Zone brokers.

Requirements:

- faction role
- specific story function
- relationship hook
- ability or institutional power
- canon risk note

Month 1 target:

20 A-tier characters.

## B Tier

Use for case characters, witnesses, one-arc Ghosts, family AI custodians, technicians, local leaders, and victims whose cases reveal the world.

Requirements:

- one strong moral problem
- one relationship hook
- one worldbuilding detail
- minimal visual marker

Month 1 target:

20 B-tier characters.

## 300 Character Distribution

```text
CHASER: 50
Ghost / Ghost Union: 50
Atlas / ECHO Council: 50
Black Zone / Memory Bank: 50
Dream Network / Abyss: 50
Mars / Free Orbitals / independent: 50
```

## Required Character Card Fields

```yaml
id:
name:
zh_name:
codename:
tier:
age:
apparent_age:
origin:
faction:
rank:
status:
biological_state:
legal_identity_state:
uploaded_continuity_state:
ghost_selfhood_state:
role:
theme:
voice:
beliefs:
goals:
fears:
abilities:
limitations:
relationships:
memory_hooks:
agent_hooks:
description:
secret:
future:
quote:
visual_design:
illustration_prompt:
canon_risks:
```

## Identity State Requirement

Every important character must track:

- biological life
- legal identity
- uploaded continuity
- Ghost selfhood

This keeps ECHO from simplifying identity into alive/dead.

## Ability Rules

Every ability must have:

- infrastructure explanation
- activation condition
- cost
- failure mode
- countermeasure
- story limitation

No ability can solve its own central conflict.

## Visual Rules

Every character needs:

- faction silhouette
- white/black/industrial relationship
- one restrained accent color
- Echo Core or interface marker
- no fantasy costume elements
- no generic neon punk default

## Relationship Rules

Each new character should connect to at least two of:

- a main cast member
- a faction
- a location
- a technology
- a legal identity problem
- a Ghost ecology problem

## Agent Readiness

Characters intended for long-running Agent use need:

- voice
- beliefs
- goals
- fears
- relationship weights
- memory hooks
- forbidden actions
- daily behavior seed

## Generation Ban List

Do not generate:

- magic users
- chosen-one clones without cost
- multiverse variants
- time travelers
- generic cyberpunk street thugs with no identity hook
- villains who are evil only because AI
- characters whose ability has no infrastructure explanation

## Character Batch Rule

For every 10 new characters:

- 2 should be CHASER or adjacent
- 2 should be Ghost or Ghost Union
- 2 should be Atlas / Memory Bank / ECHO Council
- 1 should be Black Zone
- 1 should be Dream Network / Abyss
- 1 should be Mars / Orbital
- 1 should be independent civilian or case witness

## Canon Promotion

Generated characters enter `outputs/character/` first.

They promote to `characters/` only after:

- ConsistencyAgent review
- relationship hooks confirmed
- ability constraints checked
- visual prompt accepted
- identity states completed
