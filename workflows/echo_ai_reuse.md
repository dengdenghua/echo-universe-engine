# Octopus Reuse Plan

ECHO Universe should remain a standalone IP repository, while Octopus-Agent provides the runtime nervous system.

```text
octopus-agent
  runtime, scheduling, memory, knowledge graph, model routing, multi-agent execution

echo-universe-engine
  canon, characters, factions, timeline, stories, visual assets, universe pipeline
```

## Reusable Octopus Components

| ECHO layer | Octopus component | Reuse strategy |
|---|---|---|
| World Brain | `GraphRuntime`, team runner, generator/evaluator topology | Use to execute event workflows and canon audits |
| Timeline Brain | `Journal`, scheduler | Use as append-only history and daily/monthly evolution log |
| Relationship Graph | `KnowledgeGraph` / `SqliteKnowledgeGraph` | Store character relationships as triples |
| Character Agents | `agents/<id>/agent-core/SOUL.md`, `IDENTITY.md`, `MEMORY.md` | Export Zero/Kane/etc. into Octopus agent folders |
| Memory Vault | agent `MEMORY.md`, runtime memory, journal | Store long-term character growth and event memory |
| Event Agent | `TeamRunner`, subagents, parallel agents, blackboard | Fan out one event to many characters and aggregate reactions |
| Model Routing | OpenAI/Anthropic/MultiModelRouter | Use cheap models for minor reactions, strong models for World Brain |
| Scheduler | `BackgroundRunner` and cron | Run daily lives, event ticks, audits, and monthly bible upgrades |

## Octopus Ecosystem Split

ECHO should reuse the wider Octopus ecosystem without becoming a subfolder of it.

| System | ECHO role | What it should run |
|---|---|---|
| `echo-universe-engine` | Canon source | Bible, characters, timeline, relationships, stories, prompts, candidate outputs |
| `octopus-agent` | Runtime brain | World Brain review, Character Agent execution, scheduler, KG, Journal, model routing |
| `octopus-mobile` | Embodied gateway | Future mobile notifications, camera/screen context, field interaction, companion UI |
| `octopus-storage` | Memory vault | Long-term memory, embeddings, documents, images, generated assets, searchable archives |

This keeps the IP clean. Octopus can execute the universe, but only ECHO canon folders decide what becomes official.

## Recommended Integration Shape

Do not merge ECHO canon directly into Octopus core code.

Instead:

1. Keep `/Users/dangbei/Public/octopus/echo-universe-engine` as the canon repository.
2. Add an Octopus adapter that can export ECHO characters into an Octopus agents root.
3. Let Octopus run character agents and event simulations.
4. Write generated outputs back into ECHO `outputs/` first.
5. Promote reviewed material into canon folders.

The machine-readable contract for this split lives in:

```text
integrations/octopus_ecosystem.yaml
```

Use it as the single source for paths, layer ownership, flow status, and canon boundaries.

## First Milestone

Minimum viable neural universe:

```text
event yaml/json
  -> local event simulation
  -> character reactions
  -> world brain audit
  -> outputs/events/*.md
```

Then:

```text
event yaml/json
  -> Octopus character agents
  -> KnowledgeGraph relationship update
  -> Journal history write
  -> ECHO canon candidate
```

## Digital Life Runtime

The long-term target is one persistent Octopus agent per major ECHO character:

```text
Zero Agent
Kane Agent
Eve Agent
Leon Agent
Raven Agent
Shion Agent
Noah Agent
Luna Agent
```

Each agent owns private memory and diary drafts, but World Brain owns canon promotion.

```text
daily tick
  -> character private memory
  -> relationship pressure
  -> diary candidate
  -> World Brain review
  -> timeline / canon promotion only if approved
```
