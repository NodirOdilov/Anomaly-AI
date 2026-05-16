"""Главная точка входа FastAPI Anomaly AI v2.

Этот модуль:

1. Настраивает structlog (JSON в production, ANSI в dev).
2. Создаёт FastAPI с lifespan (БД + admin bootstrap).
3. Подключает middleware-стек: RequestId → Prometheus → CORS → Audit → SlowAPI.
4. Регистрирует все роутеры (v1: совместимые; v2: новые auth/admin/integrations).
5. Подключает Prometheus ``/metrics`` и Sentry (если настроен).
"""

from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

# === Конфигурация и логи (импортируем первыми) ===
from anomaly_ai.common.config import get_settings, merged_app_config
from anomaly_ai.common.exceptions import AppError
from anomaly_ai.observability.logging import configure_structlog, get_logger

configure_structlog()
logger = get_logger(__name__)

# === Middleware и lifespan ===
from anomaly_ai.api.lifespan import lifespan
from anomaly_ai.api.middleware import (
    AuditLogMiddleware,
    app_error_handler,
    build_limiter,
    rate_limit_exceeded_handler,
)
from anomaly_ai.observability.metrics import PrometheusMiddleware, metrics_response
from anomaly_ai.observability.request_id import RequestIdMiddleware

# === v1 (совместимые) роутеры ===
from anomaly_ai.api import (
    routes_health,
    routes_info,
    routes_models,
    routes_network,
    routes_reports,
    routes_waf,
)

# === v2 (новые) роутеры ===
from anomaly_ai.api.routers import (
    alerts as r_alerts,
    audit as r_audit,
    auth as r_auth,
    drift as r_drift,
    integrations as r_integrations,
    models_registry as r_models_registry,
    users as r_users,
)
from anomaly_ai.version import __version__

settings = get_settings()


# === Sentry (опционально) ===
def _init_sentry() -> None:
    if not settings.sentry_dsn:
        return
    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration

        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            environment=settings.app_env,
            traces_sample_rate=0.1,
            integrations=[FastApiIntegration()],
        )
        logger.info("sentry.initialized")
    except Exception as exc:  # noqa: BLE001
        logger.warning("sentry.init_failed", error=str(exc))


_init_sentry()


# === Создание приложения ===

app = FastAPI(
    title="Anomaly AI",
    version=__version__,
    description="ML-платформа обнаружения сетевых аномалий и веб-атак (v2.0)",
    docs_url="/api/swagger",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)


# === CORS ===

_on_vercel = os.getenv("VERCEL", "").lower() in {"1", "true"}
if _on_vercel:
    # На Vercel одном домене лендинг + console + API — открываем для всех.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    _cfg = merged_app_config()
    _origins = list(
        (_cfg.get("app") or {}).get("cors_origins")
        or settings.cors_origins_list
        or ["http://localhost:5173", "http://127.0.0.1:5173"],
    )
    _extra = os.getenv("CORS_ORIGINS_EXTRA", "").strip()
    if _extra:
        _origins.extend([o.strip() for o in _extra.split(",") if o.strip()])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID"],
    )


# === Наблюдаемость middleware ===
app.add_middleware(RequestIdMiddleware)
if settings.metrics_enabled:
    app.add_middleware(PrometheusMiddleware)

# === Аудит (только если есть БД) ===
if not settings.is_serverless:
    app.add_middleware(AuditLogMiddleware)


# === Rate limiting ===
limiter = build_limiter()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


# === Глобальные обработчики ошибок ===
app.add_exception_handler(AppError, app_error_handler)


@app.exception_handler(RequestValidationError)
async def validation_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"error": "ValidationError", "message": str(exc)},
    )


@app.exception_handler(HTTPException)
async def http_exc_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    detail = exc.detail
    if isinstance(detail, dict):
        return JSONResponse(status_code=exc.status_code, content=detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "HTTPError", "message": str(detail)},
    )


# === Prometheus /metrics ===
if settings.metrics_enabled:
    @app.get("/metrics", include_in_schema=False)
    async def metrics() -> object:
        return metrics_response()


# === Регистрация роутеров ===

# v1 (полная обратная совместимость)
app.include_router(routes_health.router)
app.include_router(routes_info.router, prefix="/api/v1")
app.include_router(routes_waf.router, prefix="/api/v1")
app.include_router(routes_network.router, prefix="/api/v1")
app.include_router(routes_reports.router, prefix="/api/v1")
app.include_router(routes_models.router, prefix="/api/v1")

# v2 (новые возможности)
app.include_router(r_auth.router, prefix="/api/v1")
app.include_router(r_users.router, prefix="/api/v1")
app.include_router(r_audit.router, prefix="/api/v1")
app.include_router(r_alerts.router, prefix="/api/v1")
app.include_router(r_drift.router, prefix="/api/v1")
app.include_router(r_integrations.router, prefix="/api/v1")
app.include_router(r_models_registry.router, prefix="/api/v1")
