from __future__ import annotations

from pydantic import BaseModel, Field


class CharacterCard(BaseModel):
    id: str
    name: str
    codename: str | None = None
    age: str | None = None
    faction: str | None = None
    rank: str | None = None
    status: str = "Alive"
    role: str | None = None
    theme: str | None = None
    abilities: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    relationships: dict[str, str] = Field(default_factory=dict)
    description: str = ""
    secret: str | None = None
    future: str | None = None
    visual_design: str | None = None
    illustration_prompt: str | None = None


class GenerationResult(BaseModel):
    mode: str
    title: str
    content: str
    canon_risks: list[str] = Field(default_factory=list)
    output_path: str | None = None


class CanonStatus(BaseModel):
    bible_files: int
    characters: int
    factions: int
    locations: int
    technologies: int
    stories: int
    relationship_files: int
    timeline_files: int
