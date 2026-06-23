# Digital Life Mode

Digital Life Mode is the long-term target for ECHO character agents.

The character is no longer only a design sheet. Each major character becomes a persistent agent with:

- Memory
- Friends and relationship pressure
- Diary
- Growth record
- Daily activity
- Beliefs
- Goals
- Canon-safe behavior constraints

## Daily Tick

Every day, each character receives a small life update.

Examples:

```text
Zero: studies ECHO and hears a new voice in the network.
Kane: trains and quietly checks Zero's vital logs.
Luna: contacts a Ghost child in Dream Network.
Raven: executes a silent mission in Black Zone.
```

These are not automatically canon. They are candidate life logs until reviewed.

## Octopus Runtime Shape

In the first local version, `echo_engine.neural.digital_life` simulates daily ticks and writes candidate memory.

In the Octopus version, each major character becomes a long-running agent exported into:

```text
outputs/octopus_agents/<character_id>/agent-core/
```

Then `octopus-agent` can run each personality with:

- `SOUL.md` as inner voice and behavior
- `IDENTITY.md` as stable character identity
- `MEMORY.md` as long-term memory
- `AGENTS.md` as canon safety rules
- `profile.jsonc` as runtime metadata

`octopus-storage` should eventually persist memory, diary entries, embeddings, generated art, and searchable event archives. `octopus-mobile` can become the interaction layer for notifications, mobile review, and future companion-style contact with characters.

## State Model

Each character state tracks:

```yaml
id:
name:
codename:
day:
current_focus:
beliefs:
goals:
friends:
memory:
diary:
growth:
```

## Growth Rule

Character change should be slow, legible, and event-driven.

One year later, Zero should not be identical to day-one Zero. But she should still be recognizably Zero.

## Canon Safety

Digital life updates cannot:

- Kill major characters without explicit canon promotion
- Reveal season-level secrets too early
- Break power constraints
- Contradict timeline
- Convert metaphors into magic

The World Brain must audit major changes.

## Author Role

The author no longer hand-writes every event. The author sets:

- hard world rules
- season secrets
- forbidden changes
- canon promotion criteria
- emotional direction of the IP

The characters live inside those boundaries.
