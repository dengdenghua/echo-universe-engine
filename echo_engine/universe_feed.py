from __future__ import annotations

from pathlib import Path
from typing import Any

from echo_engine.bindings import get_user_binding
from echo_engine.models import CharacterCard, UniverseFeed
from echo_engine.neural.digital_life import (
    life_states_exist,
    load_or_seed_life_states,
    save_life_states,
    seed_life_state,
)
from echo_engine.store import CanonStore


class UniverseFeedError(ValueError):
    pass


def get_universe_feed_for_user(user_id: str, root: Path | None = None) -> UniverseFeed:
    binding = get_user_binding(user_id, root=root)
    if binding is None:
        raise UniverseFeedError(f"user binding not found: {user_id}")
    if binding.status != "active":
        raise UniverseFeedError(f"user binding is not active: {user_id}")

    base = root or Path.cwd()
    cards = CanonStore(root).load_character_cards()
    card = _find_card(cards, binding.character_id)
    state_existed = life_states_exist(base)
    states = load_or_seed_life_states(base, cards)
    card_missing = card.id not in states
    if card_missing:
        states[card.id] = seed_life_state(card)
    state = states[card.id]
    # 纯读不写盘：只有在首次惰性初始化（状态文件缺失）或绑定角色尚未入库时才落盘。
    # 否则每次 GET /api/universe/feed 都会写 data/digital_life_state.yaml，在 root
    # 回退到 Path.cwd() 时（如 TestClient 工作线程跨用例残留）会把假状态泄漏进真实 data/。
    if not state_existed or card_missing:
        save_life_states(base, states)

    diary = _string_dict_list(state.get("diary"))
    growth = _string_dict_list(state.get("growth"))
    return UniverseFeed(
        user_id=binding.user_id,
        binding=binding,
        character_id=card.id,
        agent_id=binding.agent_id,
        character_name=card.name,
        codename=card.codename or card.name,
        status=card.status,
        day=int(state.get("day", 0)),
        current_focus=str(state.get("current_focus") or card.theme or "identity"),
        beliefs=_string_list(state.get("beliefs")),
        goals=_string_list(state.get("goals")),
        friends={
            str(key): str(value)
            for key, value in (state.get("friends") or {}).items()
            if key is not None
        },
        memory=_string_list(state.get("memory")),
        diary=diary,
        growth=growth,
        latest_diary=diary[-1]["text"] if diary else None,
        latest_growth=growth[-1]["text"] if growth else None,
    )


def _find_card(cards: list[CharacterCard], character_id: str) -> CharacterCard:
    for card in cards:
        if card.id == character_id:
            return card
    raise UniverseFeedError(f"bound character not found: {character_id}")


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item is not None]


def _string_dict_list(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []
    rows: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        rows.append({str(key): str(val) for key, val in item.items() if val is not None})
    return rows
