"""Environment configuration, loaded only when Settings is instantiated."""

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="TEXT2SQL_", env_file=".env", extra="ignore", frozen=True
    )

    database_url: SecretStr
    ollama_url: str = "http://127.0.0.1:11434"
    model: str = "qwen3:4b-instruct-2507-q4_K_M"
    embedding_model: str = "nomic-embed-text"
    max_iterations: int = Field(default=8, ge=1, le=30)
    max_tool_calls: int = Field(default=16, ge=1, le=60)
    max_rows: int = Field(default=100, ge=1, le=1000)
    statement_timeout_ms: int = Field(default=3000, ge=1, le=30000)
    model_timeout_seconds: float = Field(default=120, gt=0, le=600)
    few_shot_k: int = Field(default=3, ge=0, le=10)
