from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from anomaly_ai.api import routes_health, routes_info, routes_models, routes_network, routes_reports, routes_waf
from anomaly_ai.api.middleware import app_error_handler
from anomaly_ai.common.config import merged_app_config
from anomaly_ai.common.exceptions import AppError
from anomaly_ai.common.logging_config import configure_logging
from anomaly_ai.version import __version__

configure_logging()

# Swagger lives under /api/* so SPA marketing docs can use /docs without clashing.
app = FastAPI(
    title="Anomaly AI",
    version=__version__,
    docs_url="/api/swagger",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# На Vercel переменная VERCEL задаётся платформой. Разрешаем любой Origin без cookie —
# так лендинг, /console и API на одном домене (и на *.vercel.app, и на своём домене)
# работают без ручных CORS_ORIGINS в настройках проекта.
_on_vercel = os.getenv("VERCEL", "").lower() in ("1", "true")
if _on_vercel:
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
        or ["http://localhost:5173", "http://127.0.0.1:5173"]
    )
    _extra = os.getenv("CORS_ORIGINS", "").strip()
    if _extra:
        _origins.extend([o.strip() for o in _extra.split(",") if o.strip()])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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


app.include_router(routes_health.router)
app.include_router(routes_info.router, prefix="/api/v1")
app.include_router(routes_waf.router, prefix="/api/v1")
app.include_router(routes_network.router, prefix="/api/v1")
app.include_router(routes_reports.router, prefix="/api/v1")
app.include_router(routes_models.router, prefix="/api/v1")
