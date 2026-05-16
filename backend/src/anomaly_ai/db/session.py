"""Async-движок SQLAlchemy + фабрика сессий.

При первом обращении создаёт engine с параметрами из :class:`Settings`.
В тестах вызывайте :func:`reset_engine` для пересоздания между сессиями.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from anomaly_ai.common.config import get_settings

logger = logging.getLogger(__name__)

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def create_engine() -> AsyncEngine:
    """Создать (или вернуть существующий) async-движок."""
    global _engine, _session_factory
    if _engine is not None:
        return _engine

    settings = get_settings()
    kwargs: dict[str, Any] = {
        "echo": settings.database_echo,
        "future": True,
    }
    # SQLite не поддерживает pool_size — фильтруем.
    if not settings.database_url.startswith("sqlite"):
        kwargs["pool_size"] = settings.database_pool_size
        kwargs["pool_pre_ping"] = True

    _engine = create_async_engine(settings.database_url, **kwargs)
    _session_factory = async_sessionmaker(_engine, expire_on_commit=False, class_=AsyncSession)
    logger.info("db.engine_created url=%s", _mask_url(settings.database_url))
    return _engine


def AsyncSessionLocal() -> AsyncSession:
    """Создать новую сессию (нужно вручную закрывать)."""
    if _session_factory is None:
        create_engine()
    assert _session_factory is not None
    return _session_factory()


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    """Контекст-менеджер с автоматическим commit/rollback.

    Использование::

        async with session_scope() as session:
            session.add(user)
            # commit вызывается автоматически при выходе без ошибок
    """
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency для инъекции сессии в роутеры."""
    async with session_scope() as session:
        yield session


async def init_db() -> None:
    """Создать таблицы (для dev/test без Alembic). В prod используйте миграции."""
    from anomaly_ai.db import models  # noqa: F401 — регистрирует модели в metadata
    from anomaly_ai.db.base import Base

    engine = create_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("db.tables_created")


async def reset_engine() -> None:
    """Закрыть движок (для тестов и graceful shutdown)."""
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
    _engine = None
    _session_factory = None


def _mask_url(url: str) -> str:
    """Скрыть пароль в URL для безопасного логирования."""
    if "@" not in url:
        return url
    scheme_user, _, host = url.partition("@")
    scheme, _, user = scheme_user.partition("://")
    if ":" in user:
        user_only = user.split(":")[0]
        return f"{scheme}://{user_only}:***@{host}"
    return url
