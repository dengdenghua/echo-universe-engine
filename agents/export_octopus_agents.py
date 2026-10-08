"""Renamed to export_echo_ai_agents.py; this shim keeps the old entry point working."""

from pathlib import Path
import runpy
import sys


if __name__ == "__main__":
    print("export_octopus_agents.py is deprecated, use export_echo_ai_agents.py", file=sys.stderr)
    runpy.run_path(str(Path(__file__).with_name("export_echo_ai_agents.py")), run_name="__main__")
