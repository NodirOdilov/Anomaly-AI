"""Просмотр реестра моделей и hot-swap активной версии."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from anomaly_ai.auth.rbac import require_admin, require_viewer
from anomaly_ai.ml.registry import get_default_registry

router = APIRouter(prefix="/ml/registry", tags=["ml", "registry"])


@router.get("", dependencies=[Depends(require_viewer)])
async def list_modules() -> list[str]:
    return get_default_registry().list_modules()


@router.get("/{module}", dependencies=[Depends(require_viewer)])
async def list_versions(module: str) -> list[dict]:
    entries = get_default_registry().list_versions(module)
    return [
        {
            "version": e.version,
            "is_active": e.is_active,
            "metrics": e.metrics,
            "metadata": e.metadata,
            "artifact_path": str(e.artifact_path),
        }
        for e in entries
    ]


@router.post(
    "/{module}/promote/{version}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
async def promote(module: str, version: str) -> None:
    try:
        get_default_registry().activate(module, version)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "NotFound", "message": str(exc)},
        ) from exc
