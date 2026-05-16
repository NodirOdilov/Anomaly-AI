"""Структурированное логирование на structlog.

В production пишет JSON в stdout (для агрегаторов: Loki, ELK, Datadog).
В dev — цветные читабельные строки.
"""

from __future__ import annotations

import logging
import sys
from typing import Any

import structlog

from anomaly_ai.common.config import get_settings


def configure_structlog() -> None:
    """Один раз настроить structlog при старте приложения."""
    settings = get_settings()
    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Базовая конфигурация stdlib logging — structlog поверх него.
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
    )

    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if settings.log_json or settings.is_production:
        renderer: Any = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=[*shared_processors, renderer],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Получить именованный logger."""
    return structlog.get_logger(name)


__all__ = ["configure_structlog", "get_logger"]
