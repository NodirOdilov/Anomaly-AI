"""Audit middleware: каждый завершённый запрос пишется в ``audit_logs``.

Запись делается *асинхронно после* ответа клиенту, чтобы не блокировать
горячий путь. Ошибки записи логируются, но не пробрасываются клиенту.
"""

from __future__ import annotations

import asyncio
import contextlib

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from anomaly_ai.db.models import AuditLog
from anomaly_ai.db.session import session_scope
from anomaly_ai.observability.request_id import current_request_id

logger = structlog.get_logger(__name__)

# Пути, не подлежащие аудиту (high-volume, низкоценные).
SKIP_PATHS: set[str] = {"/metrics", "/health", "/health/live", "/health/ready"}


class AuditLogMiddleware(BaseHTTPMiddleware):
    """Запись каждого запроса в ``audit_logs``."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)

        if request.url.path in SKIP_PATHS:
            return response

        # Fire-and-forget: не ждём завершения записи.
        asyncio.create_task(self._write_log(request, response))
        return response

    @staticmethod
    async def _write_log(request: Request, response: Response) -> None:
        try:
            user_id = None
            # Попытаемся вытащить principal, если установлен в state.
            principal = getattr(request.state, "principal", None)
            if principal is not None and getattr(principal, "user_id", 0):
                user_id = principal.user_id

            entry = AuditLog(
                user_id=user_id,
                action=f"{request.method} {request.url.path}",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                ip=_client_ip(request),
                user_agent=request.headers.get("user-agent"),
                request_id=current_request_id(),
            )
            async with session_scope() as session:
                session.add(entry)
        except Exception as exc:  # noqa: BLE001 — best-effort
            logger.warning("audit.write_failed", error=str(exc))


def _client_ip(request: Request) -> str | None:
    """Достать IP клиента (с учётом прокси-заголовков)."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    real = request.headers.get("x-real-ip")
    if real:
        return real.strip()
    if request.client:
        return request.client.host
    return None


def safe_audit_path(path: str) -> bool:
    """Проверить, подлежит ли путь аудиту (для тестов)."""
    return path not in SKIP_PATHS


with contextlib.suppress(ImportError):
    pass


__all__ = ["AuditLogMiddleware", "SKIP_PATHS", "safe_audit_path"]
