"""
SQLAlchemy async engine and session factory.

Rules (from AGENTS.md):
  - Always use AsyncSession — never synchronous sessions.
  - Never create sessions inline — always use `get_session()`.
  - Engine is created once from DATABASE_URL in config.
"""
from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=False,          # set True temporarily for SQL debug; never in prod
    pool_pre_ping=True,  # drop stale connections before use
    pool_size=10,
    max_overflow=20,
)

AsyncSessionFactory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Async context-manager / dependency that yields an AsyncSession.

    Usage:
        async with get_session() as session:
            result = await session.execute(...)

    In FastAPI-style dependencies you would use it as a generator;
    in direct code use `async with`.
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
