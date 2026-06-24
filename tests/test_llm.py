from __future__ import annotations

import httpx

from echo_engine.config import get_settings
from echo_engine.generators import run_lore_agent
from echo_engine.llm import LLMRequest, generate_candidate_content


def test_stub_provider_returns_reference_draft(monkeypatch):
    monkeypatch.setenv("ECHO_MODEL_PROVIDER", "stub")
    get_settings.cache_clear()
    result = generate_candidate_content(
        LLMRequest(
            mode="story",
            title="Demo",
            instructions="Return the draft.",
            reference_draft="# Demo\n\nDraft",
        )
    )
    assert result == "# Demo\n\nDraft"
    get_settings.cache_clear()


def test_openai_compatible_provider_posts_chat_completion(monkeypatch, tmp_path):
    requests: list[httpx.Request] = []
    client_cls = httpx.Client

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200,
            json={
                "choices": [
                    {
                        "message": {
                            "content": "# Generated\n\nCanon-safe model output.",
                        }
                    }
                ]
            },
        )

    monkeypatch.setenv("ECHO_MODEL_PROVIDER", "openai-compatible")
    monkeypatch.setenv("ECHO_MODEL_BASE_URL", "https://relay.example/v1")
    monkeypatch.setenv("ECHO_MODEL_API_KEY", "test-token")
    monkeypatch.setenv("ECHO_MODEL_NAME", "echo-test")
    monkeypatch.setattr(
        httpx,
        "Client",
        lambda **_: client_cls(transport=httpx.MockTransport(handler)),
    )
    get_settings.cache_clear()

    result = run_lore_agent(tmp_path)

    assert result.content == "# Generated\n\nCanon-safe model output."
    assert requests
    request = requests[0]
    assert str(request.url) == "https://relay.example/v1/chat/completions"
    assert request.headers["authorization"] == "Bearer test-token"
    assert '"model":"echo-test"' in request.content.decode()
    get_settings.cache_clear()
