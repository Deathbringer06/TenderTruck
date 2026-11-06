from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")

    # App
    app_name: str = "TenderTruck"
    app_version: str = "0.1.0"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str = "postgresql+psycopg://app:app@localhost:5433/tendertruck"

    # Auth
    secret_key: str = "dev-secret-change-me"
    algorithm: str = "HS256"
    access_token_minutes: int = 60 * 24

    # Pagination
    page_size_default: int = 20
    page_size_max: int = 100

    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:5180"]

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # Idempotency
    idempotency_ttl_hours: int = 24

    # Anti-sniping
    anti_snipe_extend_minutes: int = 2
    anti_snipe_max_extensions: int = 10


settings = Settings()
