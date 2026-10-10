"""Octopus was renamed to Echo AI; the old names must keep working for deployed callers."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import httpx
from fastapi.testclient import TestClient

from echo_engine.api import PromoteCandidateRequest, app
from echo_engine.config import get_settings
from echo_engine.llm import LLMRequest, generate_candidate_content
from echo_engine.neural.echo_ai_ecosystem import load_echo_ai_ecosystem
from echo_engine.neural.echo_ai_export import (
    configured_echo_ai_agents_root,
    visual_asset_index_path,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_legacy_env_vars_are_read_as_fallbacks(monkeypatch):
    monkeypatch.delenv("ECHO_AI_RUNTIME_URL", raising=False)
    monkeypatch.delenv("ECHO_AI_AGENTS_ROOT", raising=False)
    monkeypatch.setenv("ECHO_OCTOPUS_RUNTIME_URL", "http://old-runtime.local")
    monkeypatch.setenv("ECHO_OCTOPUS_AGENTS_ROOT", "/srv/old-agents")
    monkeypatch.setenv("ECHO_OCTOPUS_RUNTIME_TIMEOUT_SECONDS", "42")
    get_settings.cache_clear()
    settings = get_settings()
    assert settings.echo_ai_runtime_url == "http://old-runtime.local"
    assert settings.echo_ai_agents_root == Path("/srv/old-agents")
    assert settings.echo_ai_runtime_timeout_seconds == 42

    monkeypatch.setenv("ECHO_AI_RUNTIME_URL", "http://new-runtime.local")
    get_settings.cache_clear()
    assert get_settings().echo_ai_runtime_url == "http://new-runtime.local"
    get_settings.cache_clear()


def test_octopus_model_provider_is_an_echo_ai_alias(monkeypatch, tmp_path):
    client_cls = httpx.Client
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"choices": [{"message": {"content": "# Generated"}}]})

    monkeypatch.setattr(
        httpx,
        "Client",
        lambda **_: client_cls(transport=httpx.MockTransport(handler)),
    )
    monkeypatch.setenv("ECHO_MODEL_BASE_URL", "https://relay.example/v1")
    request = LLMRequest(
        mode="lore",
        title="Alias",
        instructions="Write.",
        reference_draft="# Draft",
        root=tmp_path,
    )
    for provider in ["echo-ai", "octopus"]:
        monkeypatch.setenv("ECHO_MODEL_PROVIDER", provider)
        get_settings.cache_clear()
        assert generate_candidate_content(request) == "# Generated"
    assert len(requests) == 2
    get_settings.cache_clear()


def test_legacy_integration_routes_alias_the_echo_ai_routes(tmp_path, monkeypatch):
    target = tmp_path / "runtime_agents"
    monkeypatch.setenv("ECHO_AI_AGENTS_ROOT", str(target))
    get_settings.cache_clear()
    client = TestClient(app)

    assert (
        client.get("/api/integrations/octopus/plan").json()
        == client.get("/api/integrations/echo-ai/plan").json()
    )
    assert client.get("/api/integrations/octopus/status").json()["agents_root"] == str(target)
    response = client.post("/api/integrations/octopus/sync-agents", json={})
    assert response.status_code == 200
    assert (target / "echo_zero" / "profile.jsonc").exists()

    paths = client.get("/openapi.json").json()["paths"]
    assert paths["/api/integrations/octopus/plan"]["get"]["deprecated"] is True
    assert "deprecated" not in paths["/api/integrations/echo-ai/plan"]["get"]
    get_settings.cache_clear()


def test_promotion_request_accepts_legacy_refresh_field():
    body = PromoteCandidateRequest.model_validate(
        {"event_id": "x", "refresh_octopus_agents": False}
    )
    assert body.refresh_echo_ai_agents is False


def test_legacy_cli_command_and_flags_still_work(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "echo_engine.cli",
            "export-octopus-agents",
            "--sync-octopus-runtime",
            "--output-dir",
            str(tmp_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    assert str(tmp_path / "echo_zero" / "profile.jsonc") in payload["written"]
    assert "export-octopus-agents is deprecated, use export-echo-ai-agents" in result.stderr


def test_legacy_export_script_runs_the_new_one(tmp_path):
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "agents" / "export_octopus_agents.py")],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout.startswith("Exported ")
    assert (tmp_path / "outputs" / "echo_ai_agents" / "_shared" / "AGENTS.md").exists()


def test_legacy_asset_urls_still_resolve():
    client = TestClient(app)
    response = client.get("/assets/characters/001_zero/octopus_refs/front.png")
    assert response.status_code == 200
    assert (
        response.content
        == (
            REPO_ROOT / "assets" / "characters" / "001_zero" / "echo_ai_refs" / "front.png"
        ).read_bytes()
    )


def test_paths_fall_back_to_pre_rename_names(tmp_path, monkeypatch):
    (tmp_path / "integrations").mkdir()
    (tmp_path / "integrations" / "octopus_ecosystem.yaml").write_text(
        "ecosystem: octopus\n", encoding="utf-8"
    )
    assert load_echo_ai_ecosystem(tmp_path) == {"ecosystem": "octopus"}

    legacy_index = tmp_path / "assets" / "characters" / "octopus_visual_asset_index.yaml"
    legacy_index.parent.mkdir(parents=True)
    legacy_index.write_text("characters: {}\n", encoding="utf-8")
    assert visual_asset_index_path(tmp_path) == legacy_index

    echo_root = tmp_path / "workspace" / "echo-universe-engine"
    legacy_agents = tmp_path / "workspace" / "octopus-agent" / "agents"
    echo_root.mkdir(parents=True)
    legacy_agents.mkdir(parents=True)
    monkeypatch.delenv("ECHO_AI_AGENTS_ROOT", raising=False)
    monkeypatch.delenv("ECHO_OCTOPUS_AGENTS_ROOT", raising=False)
    get_settings.cache_clear()
    assert configured_echo_ai_agents_root(echo_root) == legacy_agents
    get_settings.cache_clear()
