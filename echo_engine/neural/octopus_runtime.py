from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx

from echo_engine.config import get_settings


@dataclass(frozen=True)
class OctopusReloadResult:
    configured: bool
    attempted: bool
    ok: bool
    endpoint: str | None = None
    status_code: int | None = None
    response: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


def configured_octopus_runtime_url() -> str | None:
    raw = get_settings().octopus_runtime_url
    if raw is None:
        return None
    normalized = raw.strip().rstrip("/")
    return normalized or None


def reload_octopus_runtime_agents() -> OctopusReloadResult:
    base_url = configured_octopus_runtime_url()
    if base_url is None:
        return OctopusReloadResult(configured=False, attempted=False, ok=False)

    settings = get_settings()
    endpoint = f"{base_url}/api/agents/reload"
    headers: dict[str, str] = {}
    if settings.octopus_runtime_api_key:
        headers["Authorization"] = f"Bearer {settings.octopus_runtime_api_key}"

    try:
        with httpx.Client(timeout=settings.octopus_runtime_timeout_seconds) as client:
            response = client.post(endpoint, headers=headers)
            body = _safe_json(response)
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        return OctopusReloadResult(
            configured=True,
            attempted=True,
            ok=False,
            endpoint=endpoint,
            status_code=exc.response.status_code,
            response=_safe_json(exc.response),
            error=str(exc),
        )
    except httpx.HTTPError as exc:
        return OctopusReloadResult(
            configured=True,
            attempted=True,
            ok=False,
            endpoint=endpoint,
            error=str(exc),
        )

    return OctopusReloadResult(
        configured=True,
        attempted=True,
        ok=True,
        endpoint=endpoint,
        status_code=response.status_code,
        response=body,
    )


def _safe_json(response: httpx.Response) -> dict[str, Any]:
    try:
        data = response.json()
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {"data": data}
