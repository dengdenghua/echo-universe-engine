from echo_engine.generators import run_consistency_agent
from echo_engine.neural.octopus_ecosystem import (
    ecosystem_paths,
    render_octopus_ecosystem_plan,
)
from echo_engine.store import CanonStore


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
