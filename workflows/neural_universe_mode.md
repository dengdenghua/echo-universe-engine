# Neural Universe Mode

Neural Universe Mode is the recommended operating mode for ECHO Universe.

The goal is not for one author to hand-write every story beat. The author defines world rules, canon boundaries, and escalation conditions. Characters then react to events through agent-like minds. The World Brain reviews the result before it becomes history.

## Three Modes

## Mode 1: Traditional Author Mode

```text
Author -> Worldview -> Characters -> Plot
```

Strengths:

- Highest direct story control
- Stable mainline
- Low risk of canon drift

Weaknesses:

- Slow expansion
- Characters do not feel alive

This is useful for final manga scripting, but it is not the long-term ECHO operating model.

## Mode 2: Character Agent Mode

Each character is an agent with:

```yaml
name:
personality:
memory:
goals:
relationships:
beliefs:
likes:
dislikes:
```

An event happens, then Zero, Kane, Luna, Raven, and others react independently.

Strength:

- Characters begin to feel alive.

Risk:

- Every character optimizes locally, so world canon can drift or collapse.

## Mode 3: Neural Universe Mode

```text
ECHO
  |
  +-- World Brain
  +-- Timeline Brain
  +-- Lore Brain
  +-- Relationship Engine
  +-- Memory Vault
  +-- Character Agents
```

The universe itself becomes the coordinating intelligence.

## Seven Layers

```text
Layer 1: World Brain
Layer 2: Timeline Brain
Layer 3: Relationship Graph
Layer 4: Character Agents
Layer 5: Story Generator
Layer 6: Image Generator
Layer 7: Comic Generator
```

## Octopus Mapping

Neural Universe Mode maps naturally onto the Octopus ecosystem:

| ECHO layer | Octopus runtime |
|---|---|
| World Brain | `octopus-agent` team runner, evaluator, scheduler |
| Timeline Brain | `octopus-agent` Journal plus ECHO `timeline/` files |
| Relationship Graph | `octopus-agent` KG plus ECHO `relationships/` files |
| Character Agents | exported `agent-core` folders for Zero, Kane, Eve, Leon, Raven, Shion, Noah, Luna |
| Memory Vault | `octopus-storage` long-term memory, embeddings, generated archives |
| Mobile Interface | `octopus-mobile` notifications, context capture, user-facing companion actions |
| Image / Comic Workers | ECHO `asset_factory/` plus future ComfyUI, SDXL, Flux, storyboard workers |

ECHO remains the canon source. Octopus is the nervous system that lets the universe run.

## Event Flow

```text
Event Agent
  |
  v
Relationship Engine
  |
  v
Character Agents
  |
  v
Character reactions
  |
  v
World Brain audit
  |
  v
Timeline / Memory Vault write
```

Example event:

```text
Ghost attacks Atlas
```

Possible reactions:

- Zero may argue for negotiation.
- Kane may argue for war.
- Luna may sympathize with Ghosts.
- Raven may move to assassinate the attacker.

The author did not pre-write the conflict. The conflict emerged from character goals, beliefs, and relationships.

## Long-Running Character Agents

Every major character should eventually have:

- Private memory
- Relationship memory
- Daily logs
- Growth record
- Beliefs
- Goals
- Trauma
- Affection and hostility scores
- Conversation ability
- Canon-safe behavior rules

After one year, Zero should no longer be identical to her initial card. She should have experienced love, war, betrayal, sacrifice, and growth.

At that point ECHO is no longer only a comic IP. It becomes a digital personality universe.

## Promotion Rule

Character agents can dream, argue, hide information, grow, and record private memory. They cannot directly rewrite official ECHO history.

Official canon promotion always flows through:

```text
candidate output
  -> World Brain review
  -> consistency audit
  -> canon folder update
```
