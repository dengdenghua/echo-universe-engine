from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from echo_engine.generators import (
    run_art_director_agent,
    run_character_agent,
    run_consistency_agent,
    run_faction_agent,
    run_lore_agent,
    run_relationship_agent,
    run_story_agent,
    run_technology_agent,
)
from echo_engine.neural.simulator import UniverseEvent, simulate_event
from echo_engine.neural.digital_life import run_daily_life_tick
from echo_engine.neural.octopus_ecosystem import render_octopus_ecosystem_plan
from echo_engine.store import CanonStore

app = FastAPI(title="ECHO Universe Engine", version="0.1.0")


class EventRunRequest(BaseModel):
    title: str = "Ghost Attack on Atlas"
    location: str = "Atlas"
    description: str = (
        "A Ghost contamination wave hits Atlas civic identity gates, causing citizens "
        "to remember lives from dead household AI cores."
    )
    pressure: str = "identity / Ghost personhood"
    stakes: str = "Atlas stability and White Ghost Team trust"


@app.get("/api/health")
def health() -> dict[str, object]:
    status = CanonStore().status()
    return {
        "status": "ok",
        "service": "echo-universe-engine",
        "canon": status.model_dump(),
    }


@app.get("/api/canon/status")
def canon_status():
    return CanonStore().status()


@app.post("/api/agents/character/run")
def character_run():
    return run_character_agent()


@app.post("/api/agents/lore/run")
def lore_run():
    return run_lore_agent()


@app.post("/api/agents/story/run")
def story_run():
    return run_story_agent()


@app.post("/api/agents/relationship/run")
def relationship_run():
    return run_relationship_agent()


@app.post("/api/agents/faction/run")
def faction_run():
    return run_faction_agent()


@app.post("/api/agents/technology/run")
def technology_run():
    return run_technology_agent()


@app.post("/api/agents/art-director/run")
def art_director_run():
    return run_art_director_agent()


@app.post("/api/agents/consistency/run")
def consistency_run():
    return run_consistency_agent()


@app.post("/api/neural/event/run")
def neural_event_run(body: EventRunRequest):
    return simulate_event(UniverseEvent(**body.model_dump()))


@app.post("/api/neural/daily-life/run")
def neural_daily_life_run():
    return run_daily_life_tick()


@app.get("/api/integrations/octopus/plan")
def octopus_integration_plan() -> dict[str, str]:
    return {"content": render_octopus_ecosystem_plan()}
