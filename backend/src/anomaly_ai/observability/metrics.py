"""Prometheus метрики для бэкенда Anomaly AI.

Экспонируются на :func:`metrics_response` (роутер ``/metrics`` подключает её).
"""

from __future__ import annotations

import time

from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

# Своя регистрация — избегаем конфликтов с дефолтным реестром в тестах.
registry = CollectorRegistry(auto_describe=True)

# === HTTP метрики ===

http_requests_total = Counter(
    "anomaly_ai_http_requests_total",
    "Общее число HTTP-запросов",
    ["method", "path", "status"],
    registry=registry,
)

http_request_duration_seconds = Histogram(
    "anomaly_ai_http_request_duration_seconds",
    "Длительность HTTP-запросов",
    ["method", "path"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
    registry=registry,
)

http_requests_in_progress = Gauge(
    "anomaly_ai_http_requests_in_progress",
    "Количество активных HTTP-запросов",
    ["method"],
    registry=registry,
)

# === Метрики предсказаний ===

predictions_total = Counter(
    "anomaly_ai_predictions_total",
    "Общее число предсказаний",
    ["module", "prediction", "is_attack"],
    registry=registry,
)

prediction_confidence = Histogram(
    "anomaly_ai_prediction_confidence",
    "Распределение confidence предсказаний",
    ["module"],
    buckets=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0),
    registry=registry,
)

# === Дрейф моделей ===

model_drift_score = Gauge(
    "anomaly_ai_model_drift_score",
    "Текущий drift score (PSI) для модели",
    ["module"],
    registry=registry,
)

model_active_version = Gauge(
    "anomaly_ai_model_active_version_info",
    "Активная версия модели (информационная метрика — всегда 1)",
    ["module", "version"],
    registry=registry,
)

# === Аутентификация ===

auth_logins_total = Counter(
    "anomaly_ai_auth_logins_total",
    "Попытки логина",
    ["result"],  # success | failure
    registry=registry,
)

# === Алерты ===

alerts_emitted_total = Counter(
    "anomaly_ai_alerts_emitted_total",
    "Сгенерированные алерты",
    ["severity", "module"],
    registry=registry,
)


# === Middleware ===


def _normalize_path(request: Request) -> str:
    """Возвращает шаблон пути роута (без параметров), либо сам путь."""
    route = request.scope.get("route")
    if route is not None and hasattr(route, "path"):
        return route.path  # type: ignore[no-any-return]
    return request.url.path


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Учёт HTTP-запросов в гистограммах и счётчиках."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        method = request.method
        http_requests_in_progress.labels(method=method).inc()
        start = time.perf_counter()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            elapsed = time.perf_counter() - start
            path = _normalize_path(request)
            http_request_duration_seconds.labels(method=method, path=path).observe(elapsed)
            http_requests_total.labels(method=method, path=path, status=str(status_code)).inc()
            http_requests_in_progress.labels(method=method).dec()


def metrics_response() -> Response:
    """Эндпоинт ``/metrics`` — Prometheus text-format."""
    payload = generate_latest(registry)
    return Response(content=payload, media_type=CONTENT_TYPE_LATEST)


# === Удобные хелперы для бизнес-кода ===


def record_prediction_metric(
    *,
    module: str,
    prediction: str,
    is_attack: bool,
    confidence: float,
) -> None:
    predictions_total.labels(
        module=module, prediction=prediction, is_attack=str(is_attack).lower(),
    ).inc()
    prediction_confidence.labels(module=module).observe(confidence)


def update_drift_gauge(module: str, score: float) -> None:
    model_drift_score.labels(module=module).set(score)


def mark_active_model(module: str, version: str) -> None:
    model_active_version.labels(module=module, version=version).set(1)


__all__ = [
    "PrometheusMiddleware",
    "alerts_emitted_total",
    "auth_logins_total",
    "mark_active_model",
    "metrics_response",
    "predictions_total",
    "record_prediction_metric",
    "registry",
    "update_drift_gauge",
]
