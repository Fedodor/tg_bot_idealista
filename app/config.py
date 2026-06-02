"""
Application configuration loaded from environment variables via Pydantic Settings.

All secrets MUST live in .env — never hardcode them here.

Required variables:
    DATABASE_URL          — async PostgreSQL DSN  (postgresql+asyncpg://...)
    TELEGRAM_BOT_TOKEN    — BotFather token
    LOG_LEVEL             — DEBUG | INFO | WARNING | ERROR | CRITICAL
    OLLAMA_BASE_URL       — http://localhost:11434
    OLLAMA_MODEL          — e.g. llama3
"""
from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Database ──────────────────────────────────────────────────────────────
    database_url: str = Field(
        ...,
        description="Async PostgreSQL DSN — postgresql+asyncpg://user:pass@host:port/db",
    )

    # ── Telegram ──────────────────────────────────────────────────────────────
    telegram_bot_token: str = Field(..., description="Token from @BotFather")

    # ── Logging ───────────────────────────────────────────────────────────────
    log_level: str = Field("INFO", description="Root log level")

    # ── AI / Ollama ───────────────────────────────────────────────────────────
    ollama_base_url: str = Field(
        "http://localhost:11434", description="Ollama server base URL"
    )
    ollama_model: str = Field("phi3", description="Ollama model name")

    # ── Redis ─────────────────────────────────────────────────────────────────
    redis_url: str = Field("redis://localhost:6379/0", description="Redis DSN")

    # ── RapidAPI ──────────────────────────────────────────────────────────────
    rapidapi_key: str | None = Field(None, alias="RAPID_API", description="API Key for RapidAPI")
    rapidapi_host: str = Field("idealista-real-estate.p.rapidapi.com", description="RapidAPI service host")


# Singleton — import this everywhere instead of re-instantiating
settings = Settings()  # type: ignore[call-arg]
