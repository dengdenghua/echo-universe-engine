from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from echo_engine.config import get_settings
from echo_engine.store import CanonStore


SUPPORTED_OPENAI_COMPATIBLE_PROVIDERS = {
    "openai-compatible",
    "openai_compatible",
    "openai",
    "octopus",
    "relay",
}


@dataclass(frozen=True)
class LLMRequest:
    mode: str
    title: str
    instructions: str
    reference_draft: str
    root: Path | None = None


class LLMConfigurationError(RuntimeError):
    pass


class LLMGenerationError(RuntimeError):
    pass


def llm_enabled() -> bool:
    return get_settings().model_provider.strip().lower() != "stub"


def generate_candidate_content(request: LLMRequest) -> str:
    settings = get_settings()
    provider = settings.model_provider.strip().lower()
    if provider == "stub":
        return request.reference_draft
    if provider not in SUPPORTED_OPENAI_COMPATIBLE_PROVIDERS:
        raise LLMConfigurationError(
            "Unsupported ECHO_MODEL_PROVIDER. Use stub, openai-compatible, octopus, or relay."
        )

    base_url = (settings.model_base_url or "").rstrip("/")
    if not base_url:
        raise LLMConfigurationError(
            "ECHO_MODEL_BASE_URL is required when ECHO_MODEL_PROVIDER is not stub."
        )

    payload = {
        "model": settings.model_name,
        "messages": [
            {"role": "system", "content": _system_prompt()},
            {"role": "user", "content": _user_prompt(request)},
        ],
        "temperature": settings.model_temperature,
        "max_tokens": settings.model_max_tokens,
    }
    headers = {"Content-Type": "application/json"}
    if settings.model_api_key:
        headers["Authorization"] = f"Bearer {settings.model_api_key}"

    try:
        with httpx.Client(timeout=settings.model_timeout_seconds) as client:
            response = client.post(f"{base_url}/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPError as exc:
        raise LLMGenerationError(f"Model request failed: {exc}") from exc
    except ValueError as exc:
        raise LLMGenerationError("Model response was not valid JSON.") from exc

    content = _extract_openai_content(data)
    if not content:
        raise LLMGenerationError("Model response did not include message content.")
    return content.strip()


def _extract_openai_content(data: dict[str, Any]) -> str:
    choices = data.get("choices")
    if not isinstance(choices, list) or not choices:
        return ""
    first = choices[0]
    if not isinstance(first, dict):
        return ""
    message = first.get("message")
    if isinstance(message, dict):
        content = message.get("content")
        return content if isinstance(content, str) else ""
    text = first.get("text")
    return text if isinstance(text, str) else ""


def _system_prompt() -> str:
    return """You are ECHO Universe Engine, a canon-first worldbuilding worker.

Hard rules:
- ECHO is a planetary neural ecosystem grown from household AI cores.
- Ghosts are digital personalities produced from uploaded memories, not spirits.
- Memory upload, skill download, Dream Dive, Echo Core abilities, and digital immortality must stay technological.
- No magic, gods, supernatural powers, multiverse, or time travel.
- Candidate output is not canon. Flag risks instead of silently breaking canon.
- Return only the requested Markdown artifact. Do not wrap it in commentary."""


def _user_prompt(request: LLMRequest) -> str:
    status = CanonStore(request.root).status()
    return f"""Generate an ECHO candidate artifact.

Mode: {request.mode}
Working title: {request.title}

Repository canon counts:
- Bible files: {status.bible_files}
- Characters: {status.characters}
- Factions: {status.factions}
- Locations: {status.locations}
- Technologies: {status.technologies}
- Stories: {status.stories}
- Relationship files: {status.relationship_files}
- Timeline files: {status.timeline_files}

Mode instructions:
{request.instructions}

Reference draft shape to preserve or improve:
{request.reference_draft}
"""
