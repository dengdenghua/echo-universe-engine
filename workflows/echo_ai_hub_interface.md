# Echo AI Hub Interface

Echo AI integration should exist as a reserved runtime interface, not as a primary user-facing surface.

## Product Rule

ECHO OS should feel like a universe console, not an engineering control panel.

Keep Echo AI controls available for development and automation, but hide them from the default Hub view until the runtime is production-ready.

## Default Visibility

Visible by default:

- World Brain
- Character Agents
- Universe Forge
- Asset Locks
- Memory Stream

Hidden by default:

- Echo AI Runtime
- raw adapter contract
- model routing details
- execution traces
- scheduler internals

In the local WebUI, append this query parameter to expose runtime controls:

```text
http://127.0.0.1:8010/?runtime=1
```

## Reserved API Surface

Keep these API surfaces stable:

```text
GET /api/integrations/echo-ai/plan
POST /api/neural/event/run
POST /api/neural/daily-life/run
```

Future Echo AI execution endpoints should follow this shape:

```text
POST /api/integrations/echo-ai/events/run
POST /api/integrations/echo-ai/characters/{character_id}/tick
POST /api/integrations/echo-ai/story-room/run
GET  /api/integrations/echo-ai/status
```

## Responsibility Split

ECHO owns:

- canon files
- character cards
- visual locks
- timeline rules
- consistency gates
- candidate outputs

Echo AI owns:

- multi-agent execution
- character reaction fan-out
- private character memory
- roleplay continuity
- model routing
- background scheduling

## Canon Gate

Echo AI output must not write directly into canon folders.

Allowed flow:

```text
Echo AI run
  -> ECHO outputs/
  -> ConsistencyAgent review
  -> World Brain approval
  -> canon promotion
```

This keeps character agents alive without letting them corrupt the universe bible.
