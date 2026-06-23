from echo_engine.generators import run_consistency_agent
from echo_engine.store import CanonStore


def test_canon_status_counts_initial_files():
    status = CanonStore().status()
    assert status.bible_files >= 5
    assert status.characters >= 8


def test_consistency_agent_writes_output(tmp_path):
    result = run_consistency_agent(tmp_path)
    assert result.mode == "consistency"
    assert result.output_path
