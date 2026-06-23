from __future__ import annotations

import argparse
import json

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


def main() -> None:
    parser = argparse.ArgumentParser(prog="echo-engine")
    parser.add_argument(
        "command",
        choices=[
            "status",
            "character",
            "lore",
            "story",
            "relationship",
            "faction",
            "technology",
            "art",
            "consistency",
        ],
    )
    args = parser.parse_args()

    if args.command == "status":
        print(json.dumps(CanonStore().status().model_dump(), ensure_ascii=False, indent=2))
        return

    runners = {
        "character": run_character_agent,
        "lore": run_lore_agent,
        "story": run_story_agent,
        "relationship": run_relationship_agent,
        "faction": run_faction_agent,
        "technology": run_technology_agent,
        "art": run_art_director_agent,
        "consistency": run_consistency_agent,
    }
    result = runners[args.command]()
    print(result.content)
    if result.output_path:
        print(f"\nSaved: {result.output_path}")


if __name__ == "__main__":
    main()
