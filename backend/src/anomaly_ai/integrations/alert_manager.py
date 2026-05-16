"""Менеджер алертов: создание + рассылка подписчикам (WebSocket) + SIEM.

Архитектура pub-sub: WebSocket-роутер подписывается на :meth:`AlertManager.subscribe`,
бэкенд при детекте вызывает :meth:`AlertManager.emit`.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

import structlog

from anomaly_ai.common.config import get_settings
from anomaly_ai.integrations.siem import dispatcher_from_settings
from anomaly_ai.observability.metrics import alerts_emitted_total

logger = structlog.get_logger(__name__)


@dataclass
class AlertPayload:
    """Структура алерта (для рассылки и сохранения)."""

    severity: str
    module: str
    summary: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    id: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


class AlertManager:
    """In-memory pub-sub + опциональная отправка в SIEM.

    Для multi-instance деплоев замените на Redis Pub/Sub или NATS.
    """

    def __init__(self) -> None:
        self._subscribers: set[asyncio.Queue[AlertPayload]] = set()
        self._lock = asyncio.Lock()

    async def subscribe(self) -> asyncio.Queue[AlertPayload]:
        """Получить очередь, в которую будут падать новые алерты."""
        queue: asyncio.Queue[AlertPayload] = asyncio.Queue(maxsize=100)
        async with self._lock:
            self._subscribers.add(queue)
        return queue

    async def unsubscribe(self, queue: asyncio.Queue[AlertPayload]) -> None:
        async with self._lock:
            self._subscribers.discard(queue)

    async def emit(self, alert: AlertPayload) -> None:
        """Опубликовать алерт всем подписчикам и в SIEM (если настроен)."""
        alerts_emitted_total.labels(severity=alert.severity, module=alert.module).inc()
        logger.info(
            "alert.emit",
            severity=alert.severity,
            module=alert.module,
            summary=alert.summary,
        )

        async with self._lock:
            subscribers = list(self._subscribers)
        for queue in subscribers:
            try:
                queue.put_nowait(alert)
            except asyncio.QueueFull:
                logger.warning("alert.subscriber_queue_full")

        # Отправка в SIEM — fire-and-forget.
        settings = get_settings()
        if alert.payload.get("confidence", 1.0) >= settings.siem_min_confidence:
            dispatcher = dispatcher_from_settings()
            if dispatcher is not None:
                asyncio.create_task(
                    dispatcher.send(
                        module=alert.module,
                        severity=alert.severity,
                        summary=alert.summary,
                        payload=alert.payload,
                    ),
                )

    @property
    def subscriber_count(self) -> int:
        return len(self._subscribers)


# Глобальный синглтон.
alert_manager = AlertManager()


__all__ = ["AlertManager", "AlertPayload", "alert_manager"]
