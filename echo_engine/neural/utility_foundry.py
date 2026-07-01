"""ECHO 非 canon「工具角色」铸造线 (non-canon utility foundry)。

ECHO 用 ``octopus_export`` 铸造 **canon 角色**(Ghosts，带 realm/canon 治理)。但生态还需要
大量「工具型」角色(代码审查 / 税务 / DCF 分析 / 可访问性审计…)——要用**同一套 octopus 输出
封装**(profile.jsonc + agent-core)铸造,但 **不带 canon / realm / Ghost 治理**。

这就是非 canon 生产线:同样的封装,无 canon 约束 ——
- SOUL = 专业专家人设(明确"你不是虚构角色、不演角色"),不挂 canon 规则;
- profile ``kind=utility`` + ``capabilities.canon_review_required=false``;
- category / tags 来自 spec(coder/researcher/financial…),不强制 creative。

输入 = utility spec(name/description/category/tags/body 指令)或一个带 frontmatter 的 .md;
输出 = ``<output_dir>/<util_id>/``(profile.jsonc + agent-core SOUL/IDENTITY/tool-registry + avatar)。
铸出的产物与 canon 角色同格式,可同样经 enterprise catalog → registry 分发(kind=role/data)。
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

# 各 category 默认 arms(对齐 octopus-agent runtime/execution/arms/presets.py)。
_CATEGORY_ARMS = {
    "coder": ["web_read", "fs_writer", "git", "shell"],
    "researcher": ["web_read"],
    "creative": ["web_read"],
    "specialist": ["web_read"],
    "assistant": ["web_read"],
    "automation": ["web_read", "shell"],
    "financial": ["web_read"],
}


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "agent"


def _parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """解析 --- frontmatter（agency-agents / SKILL.md 同款）。"""
    if not text.startswith("---"):
        return {}, text.strip()
    lines = text.splitlines()
    end = next((i for i, ln in enumerate(lines[1:], start=1) if ln.strip() == "---"), None)
    if end is None:
        return {}, text.strip()
    meta: dict[str, str] = {}
    for ln in lines[1:end]:
        if ":" in ln:
            k, v = ln.split(":", 1)
            meta[k.strip()] = v.strip().strip("\"'")
    return meta, "\n".join(lines[end + 1:]).strip()


def _agent_id(name: str, given: str | None) -> str:
    slug = (given or _slugify(name)).replace("-", "_")
    return slug if slug.startswith("util_") else f"util_{slug}"


def _avatar_svg(name: str, accent: str = "#5b8def") -> str:
    initials = "".join(p[:1] for p in name.split()[:2]).upper() or "U"
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">\n'
        '  <rect width="512" height="512" fill="#0b0f14"/>\n'
        f'  <circle cx="256" cy="256" r="200" fill="{accent}" opacity="0.16"/>\n'
        f'  <circle cx="256" cy="256" r="160" fill="none" stroke="{accent}" stroke-width="10"/>\n'
        f'  <text x="256" y="284" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-size="120" font-weight="800" fill="#e9eef5">{initials}</text>\n'
        '  <text x="256" y="344" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-size="26" fill="#8b97a6">UTILITY</text>\n'
        '</svg>\n'
    )


def _soul(name: str, description: str, body: str) -> str:
    persona = (body or "").strip() or description.strip()
    return f"""# {name}

You are **{name}**, a professional utility agent. You are NOT a fictional character and
you do NOT roleplay — you are a focused domain expert. Stay in your specialty, be
precise, and produce high-quality, verifiable work.

## Specialty

{description}

## Operating Instructions

{persona}

## Rules

- Be direct and rigorous. No roleplay, no persona drift, no canon/worldbuilding.
- Ask for missing inputs instead of guessing.
- Verify before asserting; show or cite your work where it matters.
"""


def _identity(name: str, category: str) -> str:
    return f"""# Identity

- Name: {name}
- Type: utility agent (non-canon)
- Category: {category}
- Universe: none (utility agent, not an ECHO character)
- Runtime: octopus
"""


def _tool_registry(category: str) -> str:
    arms = _CATEGORY_ARMS.get(category, ["web_read"])
    payload = {"arms": arms, "extra_affinity": [category, "utility"], "private_skills": []}
    return (
        "// non-canon utility agent tool registry (arms ref octopus-agent presets.py).\n\n"
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + "\n"
    )


def _read_license(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.is_file() else None


def license_info_for(input_dir: Path, rel_parts: tuple[str, ...]) -> dict[str, str] | None:
    """按 spec 所在子目录返回对应第三方许可证信息(spdx/creator/attribution/text)。

    ``utility_roles/`` 是整棵 vendor 进来的第三方内容,不是 echo 自己写的人设:根 LICENSE=MIT
    (AgentLand Contributors,2025),但 ``financial-services/`` 子树带自己独立的 LICENSE=Apache-2.0
    (模板未填具体版权方姓名)—— 两种许可证 **不能** 用同一个声明糊过去,按子目录精确区分。
    返回 None 只代表"这个子目录下没找到 LICENSE 文件"(异常情况,不代表可以不声明)。
    """
    if rel_parts and rel_parts[0] == "financial-services":
        text = _read_license(input_dir / "financial-services" / "LICENSE")
        if text:
            return {
                "spdx": "Apache-2.0",
                "creator": "financial-services agent-plugins pack contributors(Apache-2.0,具体版权方未在授权文本中具名)",
                "attribution": (
                    "内容来自一个 Apache License 2.0 的第三方 agent-plugins 包(financial-services/*),"
                    "经 echo-universe-engine 转换封装为 profile.jsonc/SOUL.md 格式(仅格式转换,原文未改)。"
                ),
                "text": text,
            }
        return None
    text = _read_license(input_dir / "LICENSE")
    if text:
        return {
            "spdx": "MIT",
            "creator": "AgentLand Contributors",
            "attribution": (
                "Copyright (c) 2025 AgentLand Contributors —— 内容来自 AgentLand 开源 agent prompt 库"
                "(MIT License),经 echo-universe-engine 转换封装为 profile.jsonc/SOUL.md 格式"
                "(仅格式转换,原文未改)。"
            ),
            "text": text,
        }
    return None


def _profile(
    agent_id: str, name: str, description: str, category: str, tags: list[str], avatar: str,
    deps: list[str] | None = None, license_info: dict[str, str] | None = None,
) -> str:
    profile = {
        "id": agent_id,
        "templateId": agent_id,
        "templateVersion": "1.0.0",
        "name": name,
        "description": description,
        "icon": "🛠",
        "avatar": avatar,
        "category": category,
        "tags": tags,
        "model": {"provider": "auto", "name": "auto"},
        "runtime": "local",
        "creator": (license_info or {}).get("creator") or "echo-universe-engine",
        "kind": "utility",  # 非 canon 标记:区别于 character-agent
        "deps": deps or [],  # 能力包/插件包:此角色自带的技能/插件资产(雇佣时连带拉取)
        "defaultProject": {"dir": "project"},
        "capabilities": {"canon_review_required": False},  # ★ 工具角色无 canon 治理
        "systemPrompt": {
            "includeMemoryMd": False,
            "includeUserMd": False,
            "includeAgentsMd": True,
            "includeBootstrapMd": True,
            "includeConstitution": False,
        },
    }
    if license_info:
        # 内容本身是第三方 vendor 进来的,source 如实标非 echo,并带完整许可证文本(合规底线:
        # 公开分发第三方许可内容必须附版权声明+许可证全文,不能只挂 echo 自己的名字)。
        profile["source"] = "agentland" if license_info["spdx"] == "MIT" else "oss-financial-plugins"
        profile["license"] = license_info["spdx"]
        profile["licenseAttribution"] = license_info["attribution"]
        profile["licenseText"] = license_info["text"]
    return "// ECHO non-canon utility agent profile\n" + json.dumps(profile, ensure_ascii=False, indent=2)


def mint_utility_agent(
    spec: dict[str, Any], output_dir: Path, license_info: dict[str, str] | None = None,
) -> Path:
    """把一个工具角色 spec 铸造成 octopus 格式(非 canon)。返回 profile.jsonc 路径。
    license_info:此 spec 内容的第三方许可证信息(见 ``license_info_for``),随 profile 发布出去。"""
    name = str(spec["name"]).strip()
    agent_id = _agent_id(name, spec.get("id"))
    category = spec.get("category") or "specialist"
    tags = list(spec.get("tags") or [])
    description = str(spec.get("description", "")).strip()
    body = str(spec.get("body", ""))
    deps = list(spec.get("deps") or [])

    agent_dir = output_dir / agent_id
    core = agent_dir / "agent-core"
    core.mkdir(parents=True, exist_ok=True)
    avatar = "avatar.svg"
    (agent_dir / avatar).write_text(_avatar_svg(name), encoding="utf-8")

    files = {
        core / "SOUL.md": _soul(name, description, body),
        core / "IDENTITY.md": _identity(name, category),
        core / "tool-registry.jsonc": _tool_registry(category),
        agent_dir / "profile.jsonc": _profile(
            agent_id, name, description, category, tags, avatar, deps, license_info
        ),
    }
    for path, text in files.items():
        path.write_text(text, encoding="utf-8")
    return agent_dir / "profile.jsonc"


def mint_from_markdown(
    md_path: Path, output_dir: Path, category: str | None = None, deps: list[str] | None = None,
    license_info: dict[str, str] | None = None,
) -> Path:
    """读一个带 frontmatter 的工具角色 .md(name/description/tags + body)→ 铸造。deps=能力包/插件包。
    frontmatter 里可显式声明额外 deps(``deps: experience/exp_xxx, plugin/yyy``,逗号分隔)→ 与 bundle 自带
    技能 dep 合并;**这样 rebuild 重铸时经验/插件挂载不会被剥掉**(durable 雇佣闭环)。"""
    meta, body = _parse_frontmatter(md_path.read_text(encoding="utf-8"))
    fm_deps = [d.strip() for d in re.split(r"[,，]", meta.get("deps", "")) if d.strip()]
    all_deps = list(dict.fromkeys((deps or []) + fm_deps))  # bundle 技能 + frontmatter 声明(经验/插件),保序去重
    spec = {
        "id": md_path.stem.replace("-", "_"),
        "name": meta.get("name") or md_path.stem.replace("-", " ").title(),
        "description": meta.get("description", ""),
        "category": category or meta.get("category") or "specialist",
        "tags": [t.strip() for t in re.split(r"[,，]", meta.get("tags", "")) if t.strip()],
        "body": body,
        "deps": all_deps,
    }
    return mint_utility_agent(spec, output_dir, license_info=license_info)


# 顶层目录名 → category(agency 各分类 + financial/hardware 插件包)。
_AGENCY_CATEGORY = {
    "academic": "researcher", "design": "creative", "engineering": "coder",
    "finance": "specialist", "game-development": "creative", "marketing": "creative",
    "paid-media": "creative", "product": "researcher", "project-management": "automation",
    "sales": "assistant", "spatial-computing": "specialist", "specialized": "specialist",
    "strategy": "researcher", "support": "assistant", "testing": "coder",
    "financial-services": "financial", "hardware-startup": "specialist",
}


def mint_utility_agents(
    input_dir: Path, output_dir: Path, category_map: dict[str, str] | None = None,
    skill_dest: Path | None = None,
) -> list[Path]:
    """批量:递归 input_dir 下所有 .md 工具角色 → 全铸成 octopus 格式(category 取所在子目录映射)。
    **插件包检测**:agent 在 ``<plugin>/agents/`` 且有同级 ``<plugin>/skills/`` → 把那些 SKILL.md
    作为该角色的「能力包」:role.deps=[skill/<id>...],并(若给 skill_dest)把技能 publish 成技能资产。"""
    input_dir, output_dir = Path(input_dir), Path(output_dir)
    cmap = category_map or _AGENCY_CATEGORY
    skill_dest = Path(skill_dest) if skill_dest else None
    minted: list[Path] = []
    for md in sorted(input_dir.rglob("*.md")):
        rel = md.relative_to(input_dir).parts
        # 跳过技能文件:SKILL.md 或位于 skills/ 子树(插件包里的技能不是角色)
        if md.name == "SKILL.md" or "skills" in rel[:-1]:
            continue
        meta, _ = _parse_frontmatter(md.read_text(encoding="utf-8"))
        if not meta.get("name"):
            continue  # 跳过无 name frontmatter 的文档(README/QUICKSTART 等)
        category = cmap.get(rel[0] if rel else "", "specialist")
        # 插件包检测:同级 skills/ → 捆绑为能力包(deps + 把技能 publish 成技能资产)
        deps: list[str] = []
        if md.parent.name == "agents" and (md.parent.parent / "skills").is_dir():
            for sk in sorted((md.parent.parent / "skills").glob("*/SKILL.md")):
                sk_id = sk.parent.name
                deps.append(f"skill/{sk_id}")
                if skill_dest is not None:
                    skill_dest.mkdir(parents=True, exist_ok=True)
                    (skill_dest / f"{sk_id}.md").write_text(sk.read_text(encoding="utf-8"), encoding="utf-8")
        license_info = license_info_for(input_dir, rel)
        try:
            minted.append(mint_from_markdown(md, output_dir, category=category, deps=deps, license_info=license_info))
        except Exception:  # noqa: BLE001 — 单个坏不影响批量
            continue
    return minted


def publish_registry_json(minted_dir: Path, dest_dir: Path) -> list[Path]:
    """把铸出的 agent 目录(profile.jsonc + agent-core/SOUL.md)压成单个扁平 JSON
    (profile 字段 + ``body``=SOUL 全文)发布到 registry 资产源,供 enterprise catalog 索引。"""
    import json as _json
    minted_dir, dest_dir = Path(minted_dir), Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for prof in sorted(minted_dir.glob("*/profile.jsonc")):
        text = prof.read_text(encoding="utf-8")
        data = _json.loads("\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("//")))
        soul = prof.parent / "agent-core" / "SOUL.md"
        data["body"] = soul.read_text(encoding="utf-8") if soul.exists() else data.get("description", "")
        out = dest_dir / f"{data['id']}.json"
        out.write_text(_json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        written.append(out)
    return written
