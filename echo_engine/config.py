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
    model_base_url: str | None = None
    model_api_key: str | None = None
    model_timeout_seconds: float = 60
    model_temperature: float = 0.7
    model_max_tokens: int = 2400
    database_path: Path = Path("data/echo.sqlite3")
    journal_path: Path = Path("data/echo_journal.jsonl")
    economy_state_path: Path = Path("data/economy_state.json")
    octopus_agents_root: Path | None = None
    octopus_runtime_url: str | None = None
    octopus_runtime_api_key: str | None = None
    octopus_runtime_timeout_seconds: float = 15
    vector_backend: str = "none"
    asset_provider: str = "none"
    scheduler_enabled: bool = False
    scheduler_interval_seconds: int = 300
    scheduler_run_on_start: bool = False
    auto_git_commit: bool = False
    git_commit_paths: str = "data,outputs,assets"


@lru_cache
def get_settings() -> Settings:
    return Settings()
