"""Lifespan-логика приложения: bootstrap БД, начальный админ, graceful shutdown."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from sqlalchemy import select

from anomaly_ai.auth.password import hash_password
from anomaly_ai.common.config import get_settings
from anomaly_ai.db.models import User, UserRole
from anomaly_ai.db.session import create_engine, init_db, reset_engine, session_scope

logger = structlog.get_logger(__name__)


async def _bootstrap_admin() -> None:
    """Создать первого admin, если БД пустая. Идемпотентно."""
    settings = get_settings()
    async with session_scope() as session:
        existing = await session.execute(select(User).limit(1))
        if existing.scalar_one_or_none() is not None:
            return
        admin = User(
            email=settings.bootstrap_admin_email,
            full_name="Default Admin",
            hashed_password=hash_password(settings.bootstrap_admin_password),
            role=UserRole.ADMIN,
            is_active=True,
        )
        session.add(admin)
        logger.info("auth.bootstrap_admin_created", email=admin.email)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """FastAPI lifespan: setup перед стартом, teardown при остановке."""
    settings = get_settings()

    # На Vercel не инициализируем БД (serverless без persistent FS).
    if not settings.is_serverless:
        try:
            create_engine()
            if settings.app_env in {"development", "test"}:
                # В dev — авто-создание таблиц для удобства (без Alembic).
                await init_db()
            await _bootstrap_admin()
        except Exception as exc:
            logger.warning("lifespan.db_init_skipped", error=str(exc))

    logger.info("app.started", env=settings.app_env, version=settings.app_version)
    try:
        yield
    finally:
        if not settings.is_serverless:
            await reset_engine()
        logger.info("app.stopped")
