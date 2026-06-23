from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="ECHO_", extra="ignore")

    root: Path = Field(default_factory=lambda: Path.cwd())
    model_provider: str = "stub"
    model_name: str = "local-stub"
    database_path: Path = Path("data/echo.sqlite3")
    vector_backend: str = "none"
    asset_provider: str = "none"


@lru_cache
def get_settings() -> Settings:
    return Settings()
