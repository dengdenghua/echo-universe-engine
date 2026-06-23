from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, time
import logging
from pathlib import Path
import subprocess
import time as time_module

from echo_engine.config import get_settings
from echo_engine.generators import (
    run_character_agent,
    run_consistency_agent,
    run_faction_agent,
    run_lore_agent,
    run_relationship_agent,
    run_story_agent,
    run_technology_agent,
)
from echo_engine.neural.digital_life import run_daily_life_tick

logger = logging.getLogger("echo_engine.scheduler")

Task = tuple[str, time, Callable[[], object]]


TASKS: list[Task] = [
    ("daily character", time(9, 0), run_character_agent),
    ("daily digital life", time(9, 30), run_daily_life_tick),
    ("daily lore", time(13, 0), run_lore_agent),
    ("daily technology", time(13, 10), run_technology_agent),
    ("daily faction", time(13, 20), run_faction_agent),
    ("daily story", time(18, 0), run_story_agent),
    ("daily relationship", time(23, 0), run_relationship_agent),
    ("daily canon audit", time(23, 10), run_consistency_agent),
]


def due_task_keys(now: datetime) -> list[tuple[str, Callable[[], object]]]:
    today = now.date().isoformat()
    current = now.time()
    due: list[tuple[str, Callable[[], object]]] = []
    for name, scheduled_at, runner in TASKS:
        if current.hour == scheduled_at.hour and current.minute == scheduled_at.minute:
            due.append((f"{today}:{name}", runner))
    return due


def run_once() -> None:
    for name, _, runner in TASKS:
        logger.info("running startup task: %s", name)
        runner()
        auto_commit(name)


def auto_commit(task_name: str) -> None:
    settings = get_settings()
    if not settings.auto_git_commit:
        return

    paths = [item.strip() for item in settings.git_commit_paths.split(",") if item.strip()]
    existing_paths = [path for path in paths if Path(path).exists()]
    if not existing_paths:
        logger.info("auto commit skipped; no configured paths exist")
        return

    try:
        subprocess.run(["git", "add", *existing_paths], check=True)
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], check=False)
        if diff.returncode == 0:
            logger.info("auto commit skipped; no staged changes")
            return
        subprocess.run(["git", "commit", "-m", f"echo: {task_name}"], check=True)
        logger.info("auto committed task output: %s", task_name)
    except (OSError, subprocess.CalledProcessError) as exc:
        logger.warning("auto commit failed for %s: %s", task_name, exc)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    settings = get_settings()
    if not settings.scheduler_enabled:
        logger.info("scheduler disabled; set ECHO_SCHEDULER_ENABLED=true to run")
        return

    interval = max(30, settings.scheduler_interval_seconds)
    ran: set[str] = set()
    if settings.scheduler_run_on_start:
        run_once()

    logger.info("scheduler started with %ss interval", interval)
    while True:
        now = datetime.now()
        for key, runner in due_task_keys(now):
            if key in ran:
                continue
            logger.info("running scheduled task: %s", key)
            runner()
            auto_commit(key)
            ran.add(key)
        time_module.sleep(interval)


if __name__ == "__main__":
    main()
