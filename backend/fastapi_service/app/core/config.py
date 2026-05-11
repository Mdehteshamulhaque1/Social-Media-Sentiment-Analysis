from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentiment Service"
    DEBUG: bool = False
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/sentiment"
    REDIS_URL: str = "redis://redis:6379/0"

    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    HF_MODEL_NAME: str = "distilbert-base-uncased-finetuned-sst-2-english"

    class Config:
        env_file = ".env"


settings = Settings()
from functools import lru_cache
from typing import Annotated, Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Sentiment Intelligence Platform"
    environment: str = Field(default="development", validation_alias="APP_ENV")
    api_version: str = "v1"
    cors_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ]
    )
    cors_origin_regex: str | None = r"https://.*\\.vercel\\.app"
    database_url: str | None = Field(default=None, validation_alias="DATABASE_URL")
    mysql_url: str | None = Field(default=None, validation_alias="MYSQL_URL")
    postgres_dsn: str | None = Field(default=None, validation_alias="POSTGRES_DSN")
    redis_url: str = Field(default="redis://localhost:6379/0", validation_alias="REDIS_URL")
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 30
    refresh_token_days: int = 14
    nlp_model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str]:
        if value in (None, ""):
            return []
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return [str(origin).strip() for origin in value if str(origin).strip()]

    @property
    def resolved_database_url(self) -> str | None:
        return self.database_url or self.mysql_url or self.postgres_dsn


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
