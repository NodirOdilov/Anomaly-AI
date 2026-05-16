"""Глобальные обработчики ошибок приложения."""

from __future__ import annotations

from fastapi import Request, status
from fastapi.responses import JSONResponse

from anomaly_ai.common.exceptions import AppError, ModelArtifactError, ModelNotFoundError


async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    """Маппинг :class:`AppError` иерархии на HTTP-статусы."""
    code = getattr(exc, "code", "AppError")
    status_code = status.HTTP_400_BAD_REQUEST
    if isinstance(exc, ModelNotFoundError):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    if isinstance(exc, ModelArtifactError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return JSONResponse(status_code=status_code, content={"error": code, "message": exc.message})


__all__ = ["app_error_handler"]
