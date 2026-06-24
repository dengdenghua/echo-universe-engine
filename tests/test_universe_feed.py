from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

from echo_engine.bindings import bind_user_to_character
from echo_engine.neural.digital_life import run_daily_life_tick
from echo_engine.universe_feed import get_universe_feed_for_user


def seed_characters(root: Path) -> None:
    characters = root / "characters"
    characters.mkdir(parents=True, exist_ok=True)
    (characters / "001_zero.md").write_text(
        """# Zero

```yaml
id: "001"
name: Zero
codename: White Ghost
theme: Identity
relationships:
  Luna: "protective bond"
description: "Captain."
```
""",
        encoding="utf-8",
    )


def test_universe_feed_lazy_initializes_day_zero(tmp_path):
    seed_characters(tmp_path)
    bind_user_to_character(user_id="mobile-user-1", character_id="001", root=tmp_path)

    feed = get_universe_feed_for_user("mobile-user-1", root=tmp_path)

    assert feed.agent_id == "echo_zero"
    assert feed.character_name == "Zero"
    assert feed.day == 0
    assert feed.current_focus == "Identity"
    assert feed.latest_diary is None
    assert "Day 0:" in feed.memory[0]
    assert (tmp_path / "data" / "digital_life_state.yaml").exists()


def test_universe_feed_includes_daily_life_tick(tmp_path):
    seed_characters(tmp_path)
    bind_user_to_character(user_id="mobile-user-1", character_id="001", root=tmp_path)
    run_daily_life_tick(tmp_path)

    feed = get_universe_feed_for_user("mobile-user-1", root=tmp_path)

    assert feed.day == 1
    assert feed.latest_diary
    assert "signal noise" in feed.latest_diary
    assert feed.diary[-1]["text"] == feed.latest_diary


def test_universe_feed_api(tmp_path, api_client):
    seed_characters(tmp_path)
    bind_user_to_character(user_id="mobile-user-1", character_id="001", root=tmp_path)

    response = api_client.get("/api/universe/feed/mobile-user-1")

    assert response.status_code == 200
    body = response.json()
    assert body["agent_id"] == "echo_zero"
    assert body["character_name"] == "Zero"


def test_cli_universe_feed_outputs_json(tmp_path):
    seed_characters(tmp_path)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    subprocess.run(
        [
            sys.executable,
            "-m",
            "echo_engine.cli",
            "bind-character",
            "--user-id",
            "mobile-user-1",
            "--character-id",
            "001",
        ],
        check=True,
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "echo_engine.cli",
            "universe-feed",
            "--user-id",
            "mobile-user-1",
        ],
        check=True,
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert payload["agent_id"] == "echo_zero"
    assert payload["day"] == 0
