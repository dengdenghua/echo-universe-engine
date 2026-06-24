from __future__ import annotations

import httpx
from fastapi.testclient import TestClient

from echo_engine.api import app
from echo_engine.config import get_settings
from echo_engine.neural.octopus_runtime import reload_octopus_runtime_agents


def test_reload_octopus_runtime_agents_posts_bulk_reload(monkeypatch):
    requests: list[httpx.Request] = []
    client_cls = httpx.Client

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"ok": True, "added": 8, "replaced": 0, "total": 8})

    monkeypatch.setenv("ECHO_OCTOPUS_RUNTIME_URL", "http://runtime.local")
    monkeypatch.setenv("ECHO_OCTOPUS_RUNTIME_API_KEY", "admin-key")
    monkeypatch.setattr(
        httpx,
        "Client",
        lambda **_: client_cls(transport=httpx.MockTransport(handler)),
    )
    get_settings.cache_clear()

    result = reload_octopus_runtime_agents()

    assert result.ok is True
    assert result.endpoint == "http://runtime.local/api/agents/reload"
    assert result.response["total"] == 8
    assert requests[0].headers["authorization"] == "Bearer admin-key"
    get_settings.cache_clear()


def test_api_sync_can_reload_octopus_runtime(tmp_path, monkeypatch):
    client_cls = httpx.Client

    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"ok": True, "added": 8, "replaced": 0, "total": 8})

    monkeypatch.setenv("ECHO_OCTOPUS_AGENTS_ROOT", str(tmp_path / "agents"))
    monkeypatch.setenv("ECHO_OCTOPUS_RUNTIME_URL", "http://runtime.local")
    monkeypatch.setattr(
        httpx,
        "Client",
        lambda **_: client_cls(transport=httpx.MockTransport(handler)),
    )
    get_settings.cache_clear()

    response = TestClient(app).post(
        "/api/integrations/octopus/sync-agents",
        json={"reload_runtime": True},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["reload"]["ok"] is True
    assert body["reload"]["response"]["total"] == 8
    get_settings.cache_clear()
