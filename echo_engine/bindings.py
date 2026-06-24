from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from echo_engine.generators import _slugify
from echo_engine.models import CharacterCard, UserCharacterBinding
from echo_engine.store import CanonStore, atomic_write_text


BINDINGS_PATH = Path("data/user_bindings.json")


class BindingError(ValueError):
    pass


def bind_user_to_character(
    *,
    user_id: str,
    character_id: str,
    root: Path | None = None,
    source: str = "mobile",
) -> UserCharacterBinding:
    clean_user_id = _clean_required(user_id, "user_id")
    clean_character_id = _clean_required(character_id, "character_id")
    card = _find_character(root, clean_character_id)
    now = _now()
    bindings = _load_bindings(root)
    previous = bindings.get(clean_user_id)
    created_at = previous.created_at if previous else now
    binding = UserCharacterBinding(
        user_id=clean_user_id,
        character_id=card.id,
        agent_id=agent_id_for_character(card),
        character_name=card.name,
        status="active",
        created_at=created_at,
        updated_at=now,
        source=source or "mobile",
    )
    bindings[clean_user_id] = binding
    _save_bindings(bindings, root)
    return binding


def get_user_binding(user_id: str, root: Path | None = None) -> UserCharacterBinding | None:
    clean_user_id = _clean_required(user_id, "user_id")
    return _load_bindings(root).get(clean_user_id)


def list_user_bindings(root: Path | None = None) -> list[UserCharacterBinding]:
    return sorted(_load_bindings(root).values(), key=lambda item: item.updated_at, reverse=True)


def release_user_binding(user_id: str, root: Path | None = None) -> UserCharacterBinding:
    clean_user_id = _clean_required(user_id, "user_id")
    bindings = _load_bindings(root)
    binding = bindings.get(clean_user_id)
    if binding is None:
        raise BindingError(f"user binding not found: {clean_user_id}")
    updated = binding.model_copy(update={"status": "released", "updated_at": _now()})
    bindings[clean_user_id] = updated
    _save_bindings(bindings, root)
    return updated


def agent_id_for_character(card: CharacterCard) -> str:
    return f"echo_{_slugify(card.name).replace('-', '_')}"


def _find_character(root: Path | None, character_id: str) -> CharacterCard:
    for card in CanonStore(root).load_character_cards():
        if card.id == character_id or card.name.lower() == character_id.lower():
            return card
    raise BindingError(f"character not found: {character_id}")


def _load_bindings(root: Path | None = None) -> dict[str, UserCharacterBinding]:
    path = _bindings_path(root)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise BindingError(f"invalid user bindings file: {path}") from exc
    if not isinstance(data, dict):
        return {}
    raw_bindings = data.get("bindings", {})
    if not isinstance(raw_bindings, dict):
        return {}
    return {
        str(user_id): UserCharacterBinding.model_validate(binding)
        for user_id, binding in raw_bindings.items()
        if isinstance(binding, dict)
    }


def _save_bindings(bindings: dict[str, UserCharacterBinding], root: Path | None = None) -> None:
    path = _bindings_path(root)
    payload: dict[str, Any] = {
        "schema": "echo_user_bindings_v1",
        "bindings": {
            user_id: binding.model_dump(mode="json")
            for user_id, binding in sorted(bindings.items())
        },
    }
    atomic_write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def _bindings_path(root: Path | None = None) -> Path:
    base = root or Path.cwd()
    return base / BINDINGS_PATH


def _clean_required(value: str, field_name: str) -> str:
    clean = str(value or "").strip()
    if not clean:
        raise BindingError(f"{field_name} is required")
    return clean


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
