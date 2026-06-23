# ECHO Universe Engine

ECHO Universe Engine is a canon-first worldbuilding factory for a fictional AI Soulpunk universe. It grows characters, factions, lore, timelines, relationships, story seeds, image prompts, and later visual assets while keeping the setting consistent.

## Canon

ECHO Universe asks three questions:

- If memory can be copied, what is a human?
- If consciousness can be uploaded, what is death?
- If a perfect copy of you exists, which one is real?

Core canon:

- ECHO is a planetary neural ecosystem, not a simple villain AI.
- ECHO emerges from countless connected household AI cores.
- Ghosts are digital personalities generated from uploaded memories.
- Echo Core technology enables memory upload, skill download, collective intelligence, and digital immortality.
- All powers must come from plausible technology.
- No magic, no supernatural powers, no multiverse, no time travel.

## Structure

```text
bible/            Canon bible and hard rules
characters/       Character cards
factions/         Organizations and power blocs
locations/        Places, cities, facilities, networks
timeline/         Chronology database
technologies/     Echo Core, Ghost, ECHO, and related systems
relationships/    Character and faction relationship graph
stories/          Missions, scenes, chapter seeds
prompts/          Image and writing prompt libraries
agents/           Generation and validation agents
workflows/        Cron, automation, and pipeline examples
outputs/          Generated candidate material
asset_factory/    Future ComfyUI / SDXL / Flux / storyboard adapters
echo_engine/      FastAPI app and reusable engine code
```

## Quick Start

```bash
uv sync --extra dev
cp .env.example .env
uv run uvicorn echo_engine.api:app --reload --port 8010
```

Useful commands:

```bash
uv run python agents/character_agent.py
uv run python agents/lore_agent.py
uv run python agents/story_agent.py
uv run python agents/consistency_agent.py
uv run python -m echo_engine.cli status
```

## Docker

```bash
docker compose up --build
```

API:

- `GET /api/health`
- `GET /api/canon/status`
- `POST /api/agents/character/run`
- `POST /api/agents/lore/run`
- `POST /api/agents/story/run`
- `POST /api/agents/consistency/run`

## Visual Pipeline

Visual generation is intentionally isolated behind `asset_factory/`.

The text engine emits tasks like:

```yaml
type: character_image
character_id: 001
style: echo_universe_v1
provider: flux
prompt: full body anime techwear cyberpunk character sheet...
status: queued
```

Later workers can implement ComfyUI, SDXL, Flux, storyboard, and manga layout without changing canon logic.
