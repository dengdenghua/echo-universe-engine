import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from echo_engine.generators import run_character_agent

if __name__ == "__main__":
    result = run_character_agent()
    print(result.content)
    print(f"\nSaved: {result.output_path}")
