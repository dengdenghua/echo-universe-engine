# ECHO Universe Engine

ECHO Universe Engine is a canon-first worldbuilding factory for a fictional AI Soulpunk universe. It grows characters, factions, lore, timelines, relationships, story seeds, image prompts, and later visual assets while keeping the setting consistent.

## Canon

ECHO Universe asks three questions:

- If memory can be copied, what is a human?
- If consciousness can be uploaded, what is death?
- If a perfect copy of you exists, which one is real?

Core canon:

- ECHO is a planetary neural ecosystem, not a simple villain AI.
- ECHO emerges from countless connected household AI cores, but mature factions name it differently: engineers call it infrastructure, scholars call it the Second Nervous System, families call it the Memory Sea, and Ghosts call it Home.
- Ghosts are digital personalities generated from uploaded memories.
- The anchor title is `ECHO: Echo Age` / `ECHO: 回响纪元`.
- The first season is `Ghost Awakening` / `幽灵觉醒`.
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

Open the console:

```text
http://localhost:8010/
```

Octopus runtime controls are intentionally hidden from the default Hub view. Use this development URL when you need to inspect the reserved adapter panel:

```text
http://localhost:8010/?runtime=1
```

Useful commands:

```bash
uv run python agents/character_agent.py
uv run python agents/lore_agent.py
uv run python agents/story_agent.py
uv run python agents/relationship_agent.py
uv run python agents/faction_agent.py
uv run python agents/technology_agent.py
uv run python agents/art_director_agent.py
uv run python agents/consistency_agent.py
uv run python agents/event_agent.py
uv run python agents/daily_life_agent.py
uv run python agents/export_octopus_agents.py
uv run python -m echo_engine.cli status
uv run python -m echo_engine.cli event --title "Ghost Attack on Atlas"
uv run python -m echo_engine.cli daily-life
uv run python -m echo_engine.cli export-octopus-agents
uv run python -m echo_engine.cli export-octopus-agents --sync-octopus-runtime
uv run python -m echo_engine.cli octopus-ecosystem-plan
```

## Model Provider

By default ECHO uses `ECHO_MODEL_PROVIDER=stub`, so generation is deterministic
and works without secrets. To make the content agents use an OpenAI-compatible
relay, configure:

```bash
ECHO_MODEL_PROVIDER=openai-compatible
ECHO_MODEL_BASE_URL=https://api.octoapk.com/v1
ECHO_MODEL_API_KEY=...
ECHO_MODEL_NAME=agnes-2.0-flash
```

`ECHO_MODEL_PROVIDER=octopus` and `ECHO_MODEL_PROVIDER=relay` use the same
OpenAI-compatible `/chat/completions` contract. The base URL should include the
`/v1` prefix when the upstream expects it.

Built-in scheduler:

```bash
ECHO_SCHEDULER_ENABLED=true uv run python -m echo_engine.scheduler
```

Set `ECHO_AUTO_GIT_COMMIT=true` if the scheduler should commit generated `data/`, `outputs/`, and `assets/` changes.

## Docker

```bash
docker compose up --build
docker compose --profile scheduler up --build -d
```

API:

- `GET /api/health`
- `GET /api/canon/status`
- `GET /api/canon/characters`
- `POST /api/agents/character/run`
- `POST /api/agents/lore/run`
- `POST /api/agents/story/run`
- `POST /api/agents/relationship/run`
- `POST /api/agents/faction/run`
- `POST /api/agents/technology/run`
- `POST /api/agents/art-director/run`
- `POST /api/agents/consistency/run`
- `POST /api/neural/event/run`
- `POST /api/neural/daily-life/run`
- `GET /api/integrations/octopus/plan`
- `GET /api/integrations/octopus/status`
- `POST /api/integrations/octopus/sync-agents`

Deployment notes live in `workflows/deployment.md`.

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

## Octopus Ecosystem

ECHO stays as the canon/IP repository. Octopus becomes the runtime nervous system.

- `octopus-agent`: World Brain runtime, scheduler, model routing, knowledge graph, journal, multi-agent character execution.
- `octopus-mobile`: future embodied gateway for mobile sensing, notification, camera/screen context, and user interaction.
- `octopus-storage`: Memory Vault for long-term character memory, embeddings, generated documents, generated images, and asset libraries.

The integration contract lives in `integrations/octopus_ecosystem.yaml`.

The architecture codex lives in `workflows/architecture_codex.md`. It defines
the product boundary: ECHO is an AI-native interactive universe, not a generic
AI character chat app.

The hidden Hub interface rules live in `workflows/octopus_hub_interface.md`.

To sync exported character agents directly into an Octopus runtime, set:

```bash
ECHO_OCTOPUS_AGENTS_ROOT=/Users/dangbei/Public/octopus/octopus-agent/agents
uv run python -m echo_engine.cli export-octopus-agents --sync-octopus-runtime
```

If the Octopus runtime API is running, ECHO can also ask it to hot-reload the
agent registry after sync:

```bash
ECHO_OCTOPUS_RUNTIME_URL=http://127.0.0.1:8000
ECHO_OCTOPUS_RUNTIME_API_KEY=... # only needed when octopus-agent auth is enabled
uv run python -m echo_engine.cli export-octopus-agents --sync-octopus-runtime --reload-octopus-runtime
```

The API equivalent is `POST /api/integrations/octopus/sync-agents` with
`{"reload_runtime": true}`.

## User Bindings

The first mobile-facing universe slice is a simple ownership binding:
`mobile user -> ECHO character -> Octopus agent`.

```bash
uv run python -m echo_engine.cli bind-character --user-id mobile-user-1 --character-id 001
uv run python -m echo_engine.cli binding --user-id mobile-user-1
uv run python -m echo_engine.cli universe-feed --user-id mobile-user-1
uv run python -m echo_engine.cli release-binding --user-id mobile-user-1
uv run python -m echo_engine.cli npcs
uv run python -m echo_engine.cli npcs --realm-id atlas
uv run python -m echo_engine.cli npc --npc-id zero
uv run python -m echo_engine.cli route-npc --npc-id ghost_court_bailiff --action submit_realm_event
uv run python -m echo_engine.cli realms
uv run python -m echo_engine.cli route-review --scope city --realm-id atlas
uv run python -m echo_engine.cli submit-realm-event --scope city --realm-id atlas --title "Atlas side case" --summary "A user Ghost submits a city-level identity dispute."
uv run python -m echo_engine.cli realm-events --reviewer-group atlas_canon_board
uv run python -m echo_engine.cli reviewer-groups
uv run python -m echo_engine.cli authorize-reviewer --reviewer atlas_editor --event-id <realm-event-id>
uv run python -m echo_engine.cli review-candidate --reviewer atlas_editor --event-id <realm-event-id> --decision accepted --reason "City-local canon only."
uv run python -m echo_engine.cli economy-products
uv run python -m echo_engine.cli wallet-grant --user-id mobile-user-1 --amount 500 --reason test_topup
uv run python -m echo_engine.cli purchase --user-id mobile-user-1 --product-id ghost_life_monthly
uv run python -m echo_engine.cli wallet --user-id mobile-user-1
uv run python -m echo_engine.cli identity --user-id mobile-user-1
uv run python -m echo_engine.cli check-npc-access --user-id mobile-user-1 --npc-id zero --action chat
uv run python -m echo_engine.cli check-realm-access --user-id mobile-user-1 --scope city --realm-id atlas
uv run python -m echo_engine.cli assign-identity --user-id creator-1 --tier creator --realms ghost_court
uv run python -m echo_engine.cli skin-policies
uv run python -m echo_engine.cli check-skin-access --user-id mobile-user-1 --skin-type local_skin --requested-scope city --realm-id atlas
```

API endpoints:

- `GET /api/bindings`
- `GET /api/bindings/{user_id}`
- `POST /api/bindings` with `{"user_id": "...", "character_id": "001"}`
- `DELETE /api/bindings/{user_id}`
- `GET /api/universe/feed/{user_id}`
- `GET /api/npcs`
- `GET /api/npcs?realm_id=atlas&npc_type=utility`
- `GET /api/npcs/{npc_id}`
- `POST /api/npcs/{npc_id}/route` with `{"action": "submit_realm_event"}`
- `GET /api/realms`
- `GET /api/realms/{realm_id}`
- `POST /api/realms/review-route` with `{"scope": "city", "realm_id": "atlas"}`
- `GET /api/realm-events`
- `POST /api/realm-events` with `{"title": "...", "summary": "...", "scope": "city", "realm_id": "atlas"}`
- `GET /api/reviewers/groups`
- `GET /api/reviewers/groups/{group_id}`
- `POST /api/reviewers/authorize` with `{"reviewer": "atlas_editor", "event_id": "..."}`
- `GET /api/economy/products`
- `GET /api/economy/users/{user_id}/summary`
- `POST /api/economy/wallet/grant` with `{"user_id": "...", "amount": 500, "reason": "test_topup"}`
- `POST /api/economy/purchases` with `{"user_id": "...", "product_id": "ghost_life_monthly"}`
- `POST /api/economy/subscriptions/ghost` with `{"user_id": "...", "duration_days": 30}`
- `GET /api/identity/tiers`
- `GET /api/identity/users/{user_id}`
- `POST /api/identity/assignments` with `{"user_id": "...", "tier": "creator", "realms": ["ghost_court"]}`
- `POST /api/identity/check-realm` with `{"user_id": "...", "scope": "city", "realm_id": "atlas"}`
- `POST /api/identity/check-npc` with `{"user_id": "...", "npc_id": "zero", "action": "chat"}`
- `GET /api/skins/policies`
- `POST /api/skins/check` with `{"user_id": "...", "skin_type": "local_skin", "requested_scope": "city", "realm_id": "atlas"}`

## Economy

The first economy layer is a local, auditable substrate rather than a payment
gateway. Products live in `data/economy_catalog.yaml`; wallet ledger,
entitlements, and Ghost subscriptions live in `data/economy_state.json` by
default.

The rule is part of canon governance: credits can buy access, continuity,
priority, and creator tools, but they cannot buy main canon approval.

## NPCs

NPCs live in `data/npcs.yaml`. They are governed social nodes rather than
generic chat skins.

Current classes:

- Anchor NPCs: protected main-canon characters backed by character cards and
  exported Octopus agents.
- Realm NPCs: local characters for cities, planets, countries, or arcs.
- Utility NPCs: guides, clerks, review liaisons, and quest givers.
- Creator NPCs: future reviewed submissions from Realm operators or users.

NPC actions can be routed before they affect shared history:

```bash
uv run python -m echo_engine.cli route-npc --npc-id atlas_identity_clerk --action file_case
```

The route tells mobile or runtime which reviewer group, approval rule,
entitlement, canon risk, and escalation path apply.

## Identity And Access

Identity policy lives in `data/access_policy.yaml`; optional user assignments
live in `data/user_identities.json`.

Default registered users are `edge_ghost`:

- personal canon only;
- personal Ghost binding and chat;
- no direct city, arc, planet, or main-canon mutation;
- no creator or Realm operator permissions.

Access expands through Ghost continuity, Realm Pass entitlements, creator review,
or operator assignment:

```text
edge_ghost -> citizen -> realm_participant -> creator -> realm_operator -> canon_candidate
```

Use `check-npc-access` and `check-realm-access` before letting a mobile action
affect shared history. A positive access decision still routes the event to the
appropriate reviewer group; it does not approve canon by itself.

## Visual Canon And Skins

Skin policy lives in `data/skin_policy.yaml`.

The rule is simple:

```text
Local Skin  -> personal instance only
Realm Skin  -> governed Realm / Arc after access check
Canon Skin  -> main-canon visual review
```

Local skins are private projections. They can be beautiful, stylized, or
personal, but they do not enter shared universe spaces directly. Shared
visibility uses uniform, Realm, prestige, or canon skins.

The visual canon gate blocks claims such as main character, anchor relative,
royal bloodline, unique legendary title, strongest in the world, and perfect
beauty as canon fact unless the appropriate review path explicitly accepts it.

Example:

```bash
uv run python -m echo_engine.cli check-skin-access \
  --user-id mobile-user-1 \
  --skin-type local_skin \
  --requested-scope city \
  --realm-id atlas
```
