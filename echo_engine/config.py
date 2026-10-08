from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _echo_ai_env(name: str) -> AliasChoices:
    """ECHO_AI_<name>, still accepting the pre-rename ECHO_OCTOPUS_<name> as a fallback."""
    return AliasChoices(f"ECHO_AI_{name}", f"ECHO_OCTOPUS_{name}")


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
    echo_ai_agents_root: Path | None = Field(None, validation_alias=_echo_ai_env("AGENTS_ROOT"))
    echo_ai_runtime_url: str | None = Field(None, validation_alias=_echo_ai_env("RUNTIME_URL"))
    echo_ai_runtime_api_key: str | None = Field(
        None, validation_alias=_echo_ai_env("RUNTIME_API_KEY")
    )
    echo_ai_runtime_timeout_seconds: float = Field(
        15, validation_alias=_echo_ai_env("RUNTIME_TIMEOUT_SECONDS")
    )
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
