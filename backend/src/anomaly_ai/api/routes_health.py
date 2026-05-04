from __future__ import annotations

from fastapi import APIRouter

from anomaly_ai.version import __version__

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "Anomaly AI",
        "version": __version__,
        "backend": "FastAPI",
    }
