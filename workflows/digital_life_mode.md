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
