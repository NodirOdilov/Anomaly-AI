"""Health-чеки: liveness, readiness, агрегатный."""

from __future__ import annotations

from fastapi import APIRouter
from sqlalchemy import text

from anomaly_ai.common.config import get_settings
from anomaly_ai.db.session import AsyncSessionLocal
from anomaly_ai.version import __version__

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict:
    """Простой healthcheck (для Docker и Vercel)."""
    return {
        "status": "ok",
        "service": "Anomaly AI",
        "version": __version__,
        "backend": "FastAPI",
    }


@router.get("/health/live")
async def liveness() -> dict:
    """Liveness: процесс жив (всегда 200)."""
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness() -> dict:
    """Readiness: БД доступна. В serverless БД может быть отключена → degraded → 200."""
    settings = get_settings()
    db_ok = False
    db_error: str | None = None
    if not settings.is_serverless:
        try:
            async with AsyncSessionLocal() as session:
                await session.execute(text("SELECT 1"))
            db_ok = True
        except Exception as exc:  # noqa: BLE001
            db_error = str(exc)
    else:
        db_ok = True
    return {
        "status": "ready" if db_ok else "degraded",
        "checks": {"db": {"ok": db_ok, "error": db_error}},
    }
