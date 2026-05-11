from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables/.env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    project_name: str = Field(default="Sentiment Service", alias="PROJECT_NAME")
    debug: bool = Field(default=False, alias="DEBUG")
    app_env: str = Field(default="development", alias="APP_ENV")
    api_version: str = Field(default="v1", alias="API_VERSION")

    # Security
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=60 * 24, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_days: int = Field(default=14, alias="REFRESH_TOKEN_DAYS")

    # Infrastructure
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@db:5432/sentiment",
        alias="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")
    celery_broker_url: str = Field(default="redis://redis:6379/1", alias="CELERY_BROKER_URL")
    celery_result_backend: str = Field(default="redis://redis:6379/2", alias="CELERY_RESULT_BACKEND")

    # SQLAlchemy pool tuning
    sqlalchemy_echo: bool = Field(default=False, alias="SQLALCHEMY_ECHO")
    sqlalchemy_pool_size: int = Field(default=10, alias="SQLALCHEMY_POOL_SIZE")
    sqlalchemy_max_overflow: int = Field(default=20, alias="SQLALCHEMY_MAX_OVERFLOW")
    sqlalchemy_pool_timeout: int = Field(default=30, alias="SQLALCHEMY_POOL_TIMEOUT")
    sqlalchemy_pool_recycle: int = Field(default=1800, alias="SQLALCHEMY_POOL_RECYCLE")

    # NLP
    hf_model_name: str = Field(
        default="distilbert-base-uncased-finetuned-sst-2-english",
        alias="HF_MODEL_NAME",
    )

    # CORS
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ],
        alias="CORS_ORIGINS",
    )
    cors_origin_regex: str | None = Field(default=r"https://.*\.vercel\.app", alias="CORS_ORIGIN_REGEX")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str]:
        if value in (None, ""):
            return []
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return [str(origin).strip() for origin in value if str(origin).strip()]

    # Backward-compatible aliases used by older modules
    @property
    def PROJECT_NAME(self) -> str:
        return self.project_name

    @property
    def DEBUG(self) -> bool:
        return self.debug

    @property
    def SECRET_KEY(self) -> str:
        return self.secret_key

    @property
    def ALGORITHM(self) -> str:
        return self.algorithm

    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int:
        return self.access_token_expire_minutes

    @property
    def DATABASE_URL(self) -> str:
        return self.database_url

    @property
    def REDIS_URL(self) -> str:
        return self.redis_url

    @property
    def CELERY_BROKER_URL(self) -> str:
        return self.celery_broker_url

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return self.celery_result_backend

    @property
    def HF_MODEL_NAME(self) -> str:
        return self.hf_model_name

    @property
    def environment(self) -> str:
        return self.app_env

    @property
    def jwt_secret(self) -> str:
        return self.secret_key

    @property
    def jwt_algorithm(self) -> str:
        return self.algorithm

    @property
    def access_token_minutes(self) -> int:
        return self.access_token_expire_minutes

    @property
    def resolved_database_url(self) -> str:
        return self.database_url


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
