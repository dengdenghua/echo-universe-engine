from __future__ import annotations

import os
import tempfile
from contextlib import suppress
from pathlib import Path

import yaml

from echo_engine.models import CanonStatus, CharacterCard


def atomic_write_text(path: Path, content: str, *, encoding: str = "utf-8") -> None:
    """原子写文本：写同目录临时文件后 os.replace 落地。

    避免直接 path.write_text 在写入中途崩溃/掉电时留下半截 JSON/YAML，
    从而损坏钱包、绑定、身份等状态文件。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding=encoding) as handle:
            handle.write(content)
        os.replace(tmp, path)
    except BaseException:
        with suppress(OSError):
            os.unlink(tmp)
        raise


ROOT_NAMES = {
    "bible": "*.md",
    "characters": "*.md",
    "factions": "*.md",
    "locations": "*.md",
    "technologies": "*.md",
    "stories": "*.md",
    "relationships": "*.yaml",
    "timeline": "*.yaml",
}


class CanonStore:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root or Path.cwd()

    def path(self, *parts: str) -> Path:
        return self.root.joinpath(*parts)

    def status(self) -> CanonStatus:
        counts = {
            name: len(list(self.path(name).glob(pattern))) if self.path(name).exists() else 0
            for name, pattern in ROOT_NAMES.items()
        }
        return CanonStatus(
            bible_files=counts["bible"],
            characters=counts["characters"],
            factions=counts["factions"],
            locations=counts["locations"],
            technologies=counts["technologies"],
            stories=counts["stories"],
            relationship_files=counts["relationships"],
            timeline_files=counts["timeline"],
        )

    def read_text_bundle(self, folders: list[str]) -> str:
        chunks: list[str] = []
        for folder in folders:
            root = self.path(folder)
            if not root.exists():
                continue
            for path in sorted(root.rglob("*")):
                if path.suffix.lower() not in {".md", ".yaml", ".yml", ".txt"}:
                    continue
                chunks.append(f"# {path.relative_to(self.root)}\n{path.read_text(encoding='utf-8')}")
        return "\n\n".join(chunks)

    def load_character_cards(self) -> list[CharacterCard]:
        cards: list[CharacterCard] = []
        for path in sorted(self.path("characters").glob("*.md")):
            text = path.read_text(encoding="utf-8")
            if "```yaml" not in text:
                continue
            yaml_text = text.split("```yaml", 1)[1].split("```", 1)[0]
            data = yaml.safe_load(yaml_text) or {}
            cards.append(CharacterCard.model_validate(data))
        return cards
