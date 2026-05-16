"""Middleware и contextvar для отслеживания ``X-Request-ID``."""

from __future__ import annotations

import uuid
from contextvars import ContextVar

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

HEADER_NAME = "X-Request-ID"
_request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)


def current_request_id() -> str | None:
    """Вернуть request_id текущего запроса (или None вне HTTP-контекста)."""
    return _request_id_var.get()


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Прокидывает ``X-Request-ID`` через весь request/response цикл.

    - Если клиент прислал заголовок — используется он.
    - Иначе генерируется uuid4.
    - Сохраняется в contextvar и в structlog binding.
    - Добавляется в Response.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        incoming = request.headers.get(HEADER_NAME)
        rid = incoming or uuid.uuid4().hex
        token = _request_id_var.set(rid)
        structlog.contextvars.bind_contextvars(request_id=rid)

        try:
            response = await call_next(request)
        finally:
            _request_id_var.reset(token)
            structlog.contextvars.unbind_contextvars("request_id")

        response.headers[HEADER_NAME] = rid
        return response


__all__ = ["HEADER_NAME", "RequestIdMiddleware", "current_request_id"]
