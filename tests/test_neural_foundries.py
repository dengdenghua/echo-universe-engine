"""neural/ 铸造线与模拟器的模块级测试。

覆盖此前零测试的:utility_foundry(工具角色铸造)、experience_foundry(经验铸造)、
simulator(世界事件模拟)、models(核心 pydantic 契约不变量)。

隔离约定:所有写盘都进 tmp_path,不触碰真实 data/ 与 canon 目录。
"""

from __future__ import annotations

import json

import pytest

from echo_engine.models import CharacterCard, GenerationResult
from echo_engine.neural.experience_foundry import desensitize, mint_experience
from echo_engine.neural.simulator import (
    CharacterReaction,
    UniverseEvent,
    _react,
    _render_event,
    _world_brain_audit,
    simulate_event,
)
from echo_engine.neural.utility_foundry import (
    _agent_id,
    _parse_frontmatter,
    _slugify,
    license_info_for,
    mint_from_markdown,
    mint_utility_agent,
    mint_utility_agents,
    publish_registry_json,
)


def _character_md(card_id: str, name: str, abilities: list[str] | None = None) -> str:
    yaml_block = {
        "id": card_id,
        "name": name,
        "abilities": abilities or ["Echo Core"],
    }
    import yaml as _yaml

    return f"# {name}\n\n```yaml\n{_yaml.safe_dump(yaml_block, allow_unicode=True, sort_keys=False)}```\n"


# ── utility_foundry: 纯函数 ──────────────────────────────────


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Tax DCF Analyst!", "tax-dcf-analyst"),
        ("  -- ведун --", "agent"),  # 非法字符全被替换,strip 后为空 → 兜底
        ("", "agent"),
    ],
)
def test_slugify(text, expected):
    assert _slugify(text) == expected


@pytest.mark.parametrize(
    ("name", "given", "expected"),
    [
        ("DCF Pro", None, "util_dcf_pro"),
        ("DCF Pro", "util_custom", "util_custom"),
        ("X", "already_util_x", "util_already_util_x"),  # 无 util_ 前缀一律补
    ],
)
def test_agent_id_prefix_rules(name, given, expected):
    assert _agent_id(name, given) == expected


def test_parse_frontmatter_quoted_and_plain():
    text = '---\nname: "Tax Bot"\ntags: a, b\n---\n\nbody here'
    meta, body = _parse_frontmatter(text)
    assert meta["name"] == "Tax Bot"
    assert body == "body here"


def test_parse_frontmatter_missing_or_unterminated():
    assert _parse_frontmatter("no frontmatter") == ({}, "no frontmatter")
    assert _parse_frontmatter("---\nname: x\nbody without close") == ({}, "---\nname: x\nbody without close")


# ── utility_foundry: 铸造 ────────────────────────────────────


def test_mint_utility_agent_layout_and_profile(tmp_path):
    profile_path = mint_utility_agent(
        {"name": "DCF Analyst", "description": "d valuation", "category": "financial", "tags": ["dcf"]},
        tmp_path,
    )
    agent_dir = profile_path.parent
    assert agent_dir.name == "util_dcf_analyst" or agent_dir.name.startswith("util_")
    for rel in ("agent-core/SOUL.md", "agent-core/IDENTITY.md", "agent-core/tool-registry.jsonc", "avatar.svg"):
        assert (agent_dir / rel).exists(), rel
    profile = json.loads(
        "\n".join(
            ln for ln in profile_path.read_text(encoding="utf-8").splitlines()
            if not ln.lstrip().startswith("//")
        )
    )
    assert profile["kind"] == "utility"
    assert profile["capabilities"]["canon_review_required"] is False
    assert profile["category"] == "financial"
    assert profile["creator"] == "echo-universe-engine"
    soul = (agent_dir / "agent-core" / "SOUL.md").read_text(encoding="utf-8")
    assert "NOT a fictional character" in soul
    registry_text = (agent_dir / "agent-core" / "tool-registry.jsonc").read_text(encoding="utf-8")
    registry = json.loads(
        "\n".join(ln for ln in registry_text.splitlines() if not ln.lstrip().startswith("//"))
    )
    assert registry["arms"] == ["web_read"]  # financial 默认 arms


def test_mint_utility_agent_injects_third_party_license(tmp_path):
    info = {"spdx": "MIT", "creator": "AgentLand", "attribution": "attr", "text": "LICENSE TEXT"}
    profile_path = mint_utility_agent(
        {"name": "R", "description": "d"}, tmp_path, license_info=info
    )
    profile = json.loads(
        "\n".join(
            ln for ln in profile_path.read_text(encoding="utf-8").splitlines()
            if not ln.lstrip().startswith("//")
        )
    )
    assert profile["source"] == "agentland"
    assert profile["license"] == "MIT"
    assert profile["licenseText"] == "LICENSE TEXT"
    assert profile["creator"] == "AgentLand"  # license creator 覆盖默认


def test_mint_from_markdown_frontmatter_and_deps_merge(tmp_path):
    md = tmp_path / "role.md"
    md.write_text(
        "---\nname: Tax Helper\ndescription: 帮报税\ntags: tax, 财务\ndeps: experience/exp_t1，plugin/p2\n---\n\nDo the taxes.",
        encoding="utf-8",
    )
    profile_path = mint_from_markdown(md, tmp_path / "out", deps=["experience/exp_t1", "builtin"])
    profile = json.loads(
        "\n".join(
            ln for ln in profile_path.read_text(encoding="utf-8").splitlines()
            if not ln.lstrip().startswith("//")
        )
    )
    assert profile["name"] == "Tax Helper"
    assert profile["tags"] == ["tax", "财务"]
    # bundle deps + frontmatter deps,保序去重,中文逗号也切
    assert profile["deps"] == ["experience/exp_t1", "builtin", "plugin/p2"]
    soul = (profile_path.parent / "agent-core" / "SOUL.md").read_text(encoding="utf-8")
    assert "Do the taxes." in soul  # body 覆盖 description 作为操作指令


def test_license_info_for_financial_services_override(tmp_path):
    (tmp_path / "financial-services").mkdir()
    (tmp_path / "financial-services" / "LICENSE").write_text("APACHE TEXT", encoding="utf-8")
    (tmp_path / "LICENSE").write_text("MIT TEXT", encoding="utf-8")
    fin = license_info_for(tmp_path, ("financial-services", "x.md"))
    assert fin["spdx"] == "Apache-2.0" and fin["text"] == "APACHE TEXT"
    root_level = license_info_for(tmp_path, ("academic", "x.md"))
    assert root_level["spdx"] == "MIT" and root_level["text"] == "MIT TEXT"
    assert license_info_for(tmp_path / "void", ("academic",)) is None


def test_mint_utility_agents_batch_rules(tmp_path):
    inp = tmp_path / "in"
    (inp / "academic").mkdir(parents=True)
    (inp / "academic" / "README.md").write_text("---\ntitle: not a role\n---\n", encoding="utf-8")
    (inp / "academic" / "researcher.md").write_text(
        "---\nname: Deep Research\ndescription: r\n---\nbody", encoding="utf-8"
    )
    # 插件包:plugin/agents/role.md + plugin/skills/sk1/SKILL.md → role 应带 skill dep
    plug = inp / "financial-services" / "tax-plugin"
    (inp / "financial-services").mkdir(parents=True)
    (inp / "financial-services" / "LICENSE").write_text("APACHE TEXT", encoding="utf-8")
    (plug / "agents").mkdir(parents=True)
    (plug / "agents" / "role.md").write_text("---\nname: Tax Plug\ndescription: t\n---\n", encoding="utf-8")
    (plug / "skills" / "sk1").mkdir(parents=True)
    (plug / "skills" / "sk1" / "SKILL.md").write_text("---\nname: sk1\n---\n", encoding="utf-8")
    skill_dest = tmp_path / "published-skills"

    minted = mint_utility_agents(inp, tmp_path / "out", skill_dest=skill_dest)
    ids = sorted(p.parent.name for p in minted)
    # id 取自文件 stem,不是 name frontmatter
    assert "util_researcher" in ids
    assert "util_role" in ids
    assert not any("readme" in i for i in ids)  # 无 name 的文档跳过

    tax_profile = json.loads(
        "\n".join(
            ln for ln in (tmp_path / "out" / "util_role" / "profile.jsonc").read_text(encoding="utf-8").splitlines()
            if not ln.lstrip().startswith("//")
        )
    )
    assert tax_profile["deps"] == ["skill/sk1"]  # 插件包技能自动挂 dep
    assert (skill_dest / "sk1.md").exists()  # 技能被 publish
    assert tax_profile["license"] == "Apache-2.0"  # financial-services 子树独立许可证


def test_publish_registry_json_flattens_minted_agents(tmp_path):
    minted_dir = tmp_path / "out"
    mint_utility_agent({"name": "Flat Role", "description": "d"}, minted_dir)
    dest = tmp_path / "registry"
    written = publish_registry_json(minted_dir, dest)
    assert len(written) == 1
    data = json.loads(written[0].read_text(encoding="utf-8"))
    assert data["id"] == "util_flat_role"
    assert "NOT a fictional character" in data["body"]  # SOUL 全文注入


# ── experience_foundry ────────────────────────────────────────


@pytest.mark.parametrize(
    ("text", "hits"),
    [
        ("mail me at a.b@corp.io ok", 1),
        ("call 138-1234-5678 or 12345678901", 2),
        ("account 123456789 leaked", 1),  # 9 位裸数字 → id
        ("revenue $1,234,567 stays", 0),  # 财务数字保留
        ("clean text", 0),
    ],
)
def test_desensitize_patterns(text, hits):
    out, n = desensitize(text)
    assert n == hits
    if hits:
        assert "⟨" in out


def test_mint_experience_asset_contract(tmp_path):
    out = mint_experience(
        {
            "for_role": "util_dcf",
            "summary": "contact admin@x.io",
            "avoidance_rules": ["never trust r2"],
            "lessons": ["模型假设要对照年报"],
            "fitness": {"combined": 0.82, "verdict": "improving", "l1_trend": "up"},
            "evolved_skills": ["dcf-model", "skill/already"],
        },
        tmp_path,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["id"] == "exp_dcf_v1"
    assert data["desensitized"] is True
    assert data["redactions"] == 1
    assert "admin@x.io" not in data["body"]
    assert "⟨email⟩" in data["body"]
    assert data["deps"] == ["skill/dcf-model", "skill/already"]
    assert data["tags"] == ["experience", "self-evolved", "util_dcf"]
    assert "规避规则" in data["body"] and "never trust r2" in data["body"]
    assert "综合分 combined=0.82" in data["body"]


def test_mint_experience_custom_version_and_truncated_description(tmp_path):
    out = mint_experience(
        {"for_role": "echo_writer", "version": "v3", "summary": "长" * 300},
        tmp_path,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["id"] == "exp_writer_v3"
    assert len(data["description"]) == 200


# ── simulator ────────────────────────────────────────────────


def test_react_known_vs_generic_character():
    zero = CharacterCard(id="001", name="Zero", codename="Ghost Zero", abilities=["Echo Sync"])
    reaction = _react(zero, UniverseEvent(title="t", location="l", description="d"))
    assert isinstance(reaction, CharacterReaction)
    assert "Project E-01" in reaction.canon_risk
    assert reaction.name == "Zero / Ghost Zero"

    generic = CharacterCard(id="099", name="Nobody", theme="duty")
    fallback = _react(generic, UniverseEvent(title="t", location="l", description="d"))
    assert "theme: duty" in fallback.stance
    assert fallback.canon_risk == "Validate ability constraints before canon promotion."


def test_world_brain_audit_conditional_lines():
    event = UniverseEvent(title="t", location="l", description="The God Fragment stirs")
    audit = _world_brain_audit(event, [])
    assert any("God Fragment" in a for a in audit)
    e01 = CharacterReaction(
        character_id="x", name="n", stance="s", action="a", emotional_turn="e",
        relationship_pressure="r", canon_risk="Project E-01 reveal",
    )
    audit2 = _world_brain_audit(UniverseEvent(title="t", location="l", description="d"), [e01])
    assert any("season-level reveal" in a for a in audit2)
    plain = _world_brain_audit(UniverseEvent(title="t", location="l", description="d"), [])
    assert len(plain) == 3


def test_render_event_sections():
    event = UniverseEvent(title="Breach", location="Node 7", description="d", pressure="trust", stakes="canon")
    reactions = [
        CharacterReaction(
            character_id="1", name="Zero / Z", stance="st", action="ac",
            emotional_turn="em", relationship_pressure="rp", canon_risk="cr",
        ),
    ]
    text = _render_event(event, reactions, ["audit line"])
    assert "# Neural Event: Breach" in text
    assert "- Location: Node 7" in text
    assert "### Zero / Z" in text
    assert "- audit line" in text
    assert "## Next Writes" in text


def test_simulate_event_end_to_end_writes_candidate(tmp_path):
    (tmp_path / "characters").mkdir()
    (tmp_path / "characters" / "zero.md").write_text(
        _character_md("001", "Zero", ["Echo Sync"]), encoding="utf-8"
    )
    result = simulate_event(
        UniverseEvent(title="Signal Leak", location="Node 7", description="reality flickers"),
        root=tmp_path,
    )
    assert isinstance(result, GenerationResult)
    assert result.mode == "event"
    assert result.title == "Neural Event: Signal Leak"
    assert result.output_path and result.output_path.startswith("outputs/event/")
    assert "\\" not in result.output_path  # as_posix:journal 路径跨平台一致
    written = (tmp_path / result.output_path).read_text(encoding="utf-8")
    assert "Zero / " in written  # 命名角色反应已渲染
    # description 含 "reality" → world brain audit 追加 God Fragment 条款行
    assert "If God Fragment logic appears" in written
    # journal 候选已记录到隔离 root
    from echo_engine.journal import journal

    events = journal(tmp_path).read_all(event_type="candidate_output")
    assert any(e.title == "Neural Event: Signal Leak" for e in events)


# ── models: 契约不变量 ───────────────────────────────────────


def test_character_card_minimal_and_defaults():
    card = CharacterCard(id="001", name="Zero")
    assert card.status == "Alive"
    assert card.abilities == [] and card.relationships == {}
    assert CharacterCard.model_validate({"id": "1", "name": "n"}) == CharacterCard(id="1", name="n")


def test_generation_result_defaults():
    res = GenerationResult(mode="event", title="t", content="c")
    assert res.canon_risks == [] and res.output_path is None
