from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from echo_engine.neural.octopus_export import export_octopus_agents


if __name__ == "__main__":
    written = export_octopus_agents()
    print(f"Exported {len(written)} files")
    for path in written[:12]:
        print(path)
    if len(written) > 12:
        print(f"... {len(written) - 12} more")
