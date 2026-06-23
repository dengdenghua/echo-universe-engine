from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from echo_engine.neural.simulator import UniverseEvent, simulate_event


if __name__ == "__main__":
    event = UniverseEvent(
        title="Ghost Attack on Atlas",
        location="Atlas",
        description=(
            "A Ghost contamination wave hits Atlas civic identity gates, causing citizens "
            "to remember lives from dead household AI cores."
        ),
        pressure="identity / Ghost personhood",
        stakes="Atlas stability and White Ghost Team trust",
    )
    result = simulate_event(event)
    print(result.content)
    print(f"\nSaved: {result.output_path}")
