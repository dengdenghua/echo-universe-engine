from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

from fastapi.testclient import TestClient

from echo_engine.api import app
from echo_engine.bindings import (
    BindingError,
    bind_user_to_character,
    get_user_binding,
    release_user_binding,
)
from echo_engine.config import get_settings


def seed_characters(root):
    characters = root / "characters"
    characters.mkdir(parents=True, exist_ok=True)
    (characters / "001_zero.md").write_text(
        """# Zero

```yaml
id: "001"
name: Zero
codename: White Ghost
description: "Captain."
```
""",
        encoding="utf-8",
    )
    (characters / "008_luna.md").write_text(
        """# Luna

```yaml
id: "008"
name: Luna
codename: Dream Walker
description: "Dream walker."
```
""",
        encoding="utf-8",
    )


def test_bind_user_to_character_writes_binding(tmp_path):
    seed_characters(tmp_path)
    binding = bind_user_to_character(user_id="mobile-user-1", character_id="001", root=tmp_path)

    assert binding.user_id == "mobile-user-1"
    assert binding.character_id == "001"
    assert binding.agent_id == "echo_zero"
    assert binding.character_name == "Zero"
    saved = get_user_binding("mobile-user-1", root=tmp_path)
    assert saved == binding
    assert (tmp_path / "data" / "user_bindings.json").exists()


def test_rebinding_preserves_created_at_and_updates_character(tmp_path):
    seed_characters(tmp_path)
    first = bind_user_to_character(user_id="mobile-user-1", character_id="001", root=tmp_path)
    second = bind_user_to_character(user_id="mobile-user-1", character_id="Luna", root=tmp_path)

    assert second.created_at == first.created_at
    assert second.character_id == "008"
    assert second.agent_id == "echo_luna"
    assert second.updated_at >= first.updated_at


def test_release_user_binding_marks_released(tmp_path):
    seed_characters(tmp_path)
    bind_user_to_character(user_id="mobile-user-1", character_id="001", root=tmp_path)
    released = release_user_binding("mobile-user-1", root=tmp_path)

    assert released.status == "released"
    assert get_user_binding("mobile-user-1", root=tmp_path).status == "released"


def test_bind_user_rejects_unknown_character(tmp_path):
    seed_characters(tmp_path)
    try:
        bind_user_to_character(user_id="mobile-user-1", character_id="missing", root=tmp_path)
    except BindingError as exc:
        assert "character not found" in str(exc)
    else:
        raise AssertionError("expected BindingError")


def test_bindings_api_roundtrip(tmp_path, monkeypatch):
    seed_characters(tmp_path)
    monkeypatch.chdir(tmp_path)
    get_settings.cache_clear()
    client = TestClient(app)

    created = client.post(
        "/api/bindings",
        json={"user_id": "mobile-user-1", "character_id": "001", "source": "mobile"},
    )
    assert created.status_code == 200
    assert created.json()["agent_id"] == "echo_zero"

    fetched = client.get("/api/bindings/mobile-user-1")
    assert fetched.status_code == 200
    assert fetched.json()["character_name"] == "Zero"

    listed = client.get("/api/bindings")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    released = client.delete("/api/bindings/mobile-user-1")
    assert released.status_code == 200
    assert released.json()["status"] == "released"
    get_settings.cache_clear()


def test_cli_bind_character_outputs_binding(tmp_path):
    seed_characters(tmp_path)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
    result = subprocess.run(
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
        capture_output=True,
        cwd=tmp_path,
        env=env,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert payload["agent_id"] == "echo_zero"
