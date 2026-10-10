# Deployment

ECHO Universe Engine should deploy as an independent service. Echo AI services can run beside it, but ECHO keeps canon ownership.

## Recommended Topology

```text
echo-universe-engine
  FastAPI service, canon folders, generated candidate outputs

echo-scheduler
  optional container that runs daily universe ticks

echo-ai
  future runtime brain for multi-agent execution, Journal, KG, model routing

echo-storage
  future long-term memory, embeddings, documents, images, generated assets

echo-mobile
  future mobile review, notifications, embodied interaction gateway
```

## Local Production Start

```bash
cp .env.example .env
docker compose up --build -d
```

API:

```text
http://localhost:8010/api/health
http://localhost:8010/api/canon/status
http://localhost:8010/api/integrations/echo-ai/plan
```

## Enable Built-In Scheduler

The scheduler is optional because production may use cron, systemd timers, or Echo AI instead.

```bash
docker compose --profile scheduler up --build -d
```

Important environment variables:

```text
ECHO_SCHEDULER_ENABLED=true
ECHO_SCHEDULER_INTERVAL_SECONDS=300
ECHO_SCHEDULER_RUN_ON_START=false
ECHO_AUTO_GIT_COMMIT=false
ECHO_GIT_COMMIT_PATHS=data,outputs,assets
```

Set `ECHO_AUTO_GIT_COMMIT=true` only when the deployed checkout has a configured git identity and the server should commit generated candidate material automatically.

## Persistent Volumes

These folders should be mounted on the server:

```text
data/
outputs/
assets/
bible/
characters/
factions/
locations/
timeline/
technologies/
relationships/
stories/
prompts/
integrations/
```

Generated material first lands in `outputs/`. It is candidate material until World Brain review promotes it into canon folders.

## Automatic Git Commit

Host cron can commit after every run, as shown in `workflows/cron.example`.

The built-in scheduler can also commit generated material:

```bash
ECHO_AUTO_GIT_COMMIT=true
ECHO_GIT_COMMIT_PATHS=data,outputs,assets
```

The scheduler intentionally commits candidate output folders, not the whole repository. Canon folders should be changed by explicit review or a future World Brain promotion workflow.

## Deployment Rule

Deploy ECHO independently. Reuse Echo AI as runtime infrastructure.

```text
ECHO owns canon.
Echo AI runs agents.
Storage remembers.
Mobile interacts.
```
