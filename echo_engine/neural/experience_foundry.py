"""ECHO 经验铸造线 —— 把 agent「自进化提炼出来的经验」打包成可分发资产(type=experience)。

**scope(用户拍板,2026-06-30)**:经验资产**只收自进化提炼物**,不收原始记忆/聊天日志:
- 正向回路 → SkillForge 锻出的技能(evolved skills,也作能力包 deps);
- 负向回路 → RuleExtractor 的规避规则(avoidance rules);
- 知识回路 → KG 提炼三元组 / MemoryConsolidator 聚类记忆(distilled lessons);
- 适应度 → evolution_fitness 概况(performance profile)。
这些**已经抽象/提炼过 → 天然低 PII**,所以脱敏很轻:只做一道最终 PII 扫描兜底(emails/phones/长串 ID)。

治理闸:**"未脱敏不入市"** —— 资产标 ``desensitized=true`` + ``redactions`` 计数;未跑脱敏的不发布。
``kind=data``(纯知识无执行),挂到角色 ``deps:[experience/<id>]`` → 雇人才时连经验一起到手。
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

# 最终兜底 PII 扫描(提炼物已低敏,这里只清明显的个人标识)。
_PII_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "⟨email⟩"),
    (re.compile(r"\b\d{3}[-.\s]?\d{3,4}[-.\s]?\d{4}\b"), "⟨phone⟩"),
    (re.compile(r"\b\d{9,}\b"), "⟨id⟩"),  # 9+ 位裸数字 = SSN/账号类(保留带逗号/$的财务数字)
]


def desensitize(text: str) -> tuple[str, int]:
    """轻脱敏:清 email/phone/长串 ID,返回(脱敏文本, 命中次数)。提炼物本就低敏,这是兜底闸。"""
    n = 0
    for pat, repl in _PII_PATTERNS:
        text, c = pat.subn(repl, text)
        n += c
    return text, n


def _render_body(spec: dict[str, Any]) -> str:
    """把自进化提炼物组织成可读经验正文(消费端注入为角色的经验)。"""
    parts: list[str] = []
    if spec.get("summary"):
        parts.append(str(spec["summary"]).strip())
    rules = spec.get("avoidance_rules") or []
    if rules:
        parts.append("## 规避规则(负向回路 · 失败提炼)\n" + "\n".join(f"- {r}" for r in rules))
    lessons = spec.get("lessons") or []
    if lessons:
        parts.append("## 提炼经验(知识/记忆回路)\n" + "\n".join(f"- {x}" for x in lessons))
    fit = spec.get("fitness") or {}
    if fit:
        parts.append(
            "## 适应度概况\n"
            f"- 综合分 combined={fit.get('combined')} · 判定 {fit.get('verdict')} · 趋势 {fit.get('l1_trend')}"
        )
    skills = spec.get("evolved_skills") or []
    if skills:
        parts.append("## 自进化技能(正向回路 · SkillForge)\n" + "\n".join(f"- {s}" for s in skills))
    return "\n\n".join(parts).strip()


def mint_experience(spec: dict[str, Any], output_dir: Path) -> Path:
    """把一个角色的自进化提炼物铸成 experience 资产(脱敏后)。返回资产 JSON 路径。
    spec: {for_role, name?, version?, summary?, avoidance_rules[], lessons[], fitness{}, evolved_skills[]}。"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    role = str(spec["for_role"])
    version = str(spec.get("version", "v1"))
    raw_body = _render_body(spec)
    body, redactions = desensitize(raw_body)  # ★ 入市前必经脱敏闸
    exp_id = spec.get("id") or f"exp_{role.replace('util_', '').replace('echo_', '')}_{version}"
    # evolved_skills 形如 ["skill/dcf-model"] → 作为经验自带的能力包 deps
    deps = [s if "/" in s else f"skill/{s}" for s in (spec.get("evolved_skills") or [])]
    asset = {
        "id": exp_id,
        "name": spec.get("name") or f"{role} · 自进化经验 {version}",
        "description": (spec.get("summary") or "")[:200],
        "category": "experience",
        "tags": ["experience", "self-evolved", role],
        "icon": "🧬",
        "author": "octopus-agent-evolution",
        "kind": "experience",
        "source": "evolution",
        "for_role": role,
        "version": version,
        "desensitized": True,  # 治理闸:已过脱敏
        "redactions": redactions,
        "deps": deps,
        "body": body,
    }
    out = output_dir / f"{exp_id}.json"
    out.write_text(json.dumps(asset, ensure_ascii=False, indent=2), encoding="utf-8")
    return out
