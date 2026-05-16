"""Rate limiting через slowapi.

Использует ip-адрес как ключ. При наличии Redis URL — хранение в Redis,
иначе in-memory (для dev и одно-инстансных деплоев).
"""

from __future__ import annotations

from fastapi import Request, status
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from anomaly_ai.common.config import get_settings


def build_limiter() -> Limiter:
    """Создать настроенный лимитер."""
    settings = get_settings()
    storage_uri = settings.redis_url or "memory://"
    return Limiter(
        key_func=get_remote_address,
        storage_uri=storage_uri,
        default_limits=[settings.rate_limit_default],
        headers_enabled=True,
        strategy="moving-window",
    )


async def rate_limit_exceeded_handler(_request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Привести ответ к нашему формату ``{error, message}``."""
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error": "RateLimitExceeded",
            "message": f"Превышен лимит запросов: {exc.detail}",
        },
        headers={"Retry-After": "60"},
    )


__all__ = ["build_limiter", "rate_limit_exceeded_handler"]
