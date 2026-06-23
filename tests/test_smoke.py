from echo_engine.generators import run_consistency_agent
from echo_engine.neural.octopus_ecosystem import (
    ecosystem_paths,
    render_octopus_ecosystem_plan,
)
from echo_engine.scheduler import auto_commit, due_task_keys
from echo_engine.store import CanonStore
from datetime import datetime
from fastapi.testclient import TestClient

from echo_engine.api import app


def test_canon_status_counts_initial_files():
    status = CanonStore().status()
    assert status.bible_files >= 5
    assert status.characters >= 8


def test_consistency_agent_writes_output(tmp_path):
    result = run_consistency_agent(tmp_path)
    assert result.mode == "consistency"
    assert result.output_path


def test_octopus_ecosystem_plan_loads():
    plan = render_octopus_ecosystem_plan()
    paths = ecosystem_paths()
    assert "Octopus Ecosystem Integration Plan" in plan
    assert "character_agents" in plan
    assert "octopus_agent" in paths


def test_scheduler_due_task_keys():
    due = due_task_keys(datetime(2147, 1, 1, 9, 30))
    assert [name for name, _ in due] == ["2147-01-01:daily digital life"]


def test_auto_commit_disabled_does_nothing():
    auto_commit("test")


def test_api_serves_console_and_characters():
    client = TestClient(app)
    assert client.get("/").status_code == 200
    response = client.get("/api/canon/characters")
    assert response.status_code == 200
    assert len(response.json()) >= 8
