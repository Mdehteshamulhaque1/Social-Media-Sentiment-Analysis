from __future__ import annotations

from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from backend.fastapi_service.app.core.config import settings


def _build_engine(database_url: str):
    engine_kwargs: dict[str, Any] = {"poolclass": NullPool, "future": True}
    if database_url.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}
    return create_engine(database_url, **engine_kwargs)


database_url = settings.resolved_database_url
engine = _build_engine(database_url) if database_url else None
SessionLocal = (
    sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    if engine is not None
    else None
)


def get_db() -> Generator:
    if SessionLocal is None:
        raise RuntimeError("Database is not configured")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
