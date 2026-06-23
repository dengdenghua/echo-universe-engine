from __future__ import annotations

from fastapi import FastAPI

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
from echo_engine.store import CanonStore

app = FastAPI(title="ECHO Universe Engine", version="0.1.0")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


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
