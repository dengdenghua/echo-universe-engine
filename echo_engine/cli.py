from __future__ import annotations

import argparse
import json

from echo_engine.neural.simulator import UniverseEvent, simulate_event
from echo_engine.neural.octopus_export import export_octopus_agents
from echo_engine.neural.digital_life import run_daily_life_tick
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
            "event",
            "daily-life",
            "export-octopus-agents",
        ],
    )
    parser.add_argument("--title", default="Ghost Attack on Atlas")
    parser.add_argument("--location", default="Atlas")
    parser.add_argument(
        "--description",
        default=(
            "A Ghost contamination wave hits Atlas civic identity gates, causing citizens "
            "to remember lives from dead household AI cores."
        ),
    )
    parser.add_argument("--pressure", default="identity / Ghost personhood")
    parser.add_argument("--stakes", default="Atlas stability and White Ghost Team trust")
    args = parser.parse_args()

    if args.command == "status":
        print(json.dumps(CanonStore().status().model_dump(), ensure_ascii=False, indent=2))
        return

    if args.command == "event":
        result = simulate_event(
            UniverseEvent(
                title=args.title,
                location=args.location,
                description=args.description,
                pressure=args.pressure,
                stakes=args.stakes,
            )
        )
        print(result.content)
        if result.output_path:
            print(f"\nSaved: {result.output_path}")
        return

    if args.command == "daily-life":
        result = run_daily_life_tick()
        print(result.content)
        if result.output_path:
            print(f"\nSaved: {result.output_path}")
        return

    if args.command == "export-octopus-agents":
        written = export_octopus_agents()
        print(json.dumps([str(path) for path in written], ensure_ascii=False, indent=2))
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
