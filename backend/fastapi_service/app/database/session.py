from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ..core.config import settings
from .base import Base


def _build_async_engine() -> AsyncEngine:
    """Create a reusable async SQLAlchemy engine for PostgreSQL."""
    return create_async_engine(
        settings.database_url,
        echo=settings.sqlalchemy_echo,
        pool_pre_ping=True,
        pool_size=settings.sqlalchemy_pool_size,
        max_overflow=settings.sqlalchemy_max_overflow,
        pool_timeout=settings.sqlalchemy_pool_timeout,
        pool_recycle=settings.sqlalchemy_pool_recycle,
        future=True,
    )


engine: AsyncEngine = _build_async_engine()

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: yields an async DB session and closes it safely."""
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    """Initialize database schema for bootstrapping/local development."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Dispose engine connections on app shutdown."""
    await engine.dispose()
