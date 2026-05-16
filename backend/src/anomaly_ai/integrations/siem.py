"""Отправка событий в SIEM (Splunk HEC, ArcSight, QRadar, ELK).

Поддержаны два формата:

- **JSON** — для Splunk HEC, ELK, Datadog.
- **CEF** (Common Event Format) — для ArcSight, QRadar и совместимых.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

import httpx
import structlog
from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from anomaly_ai.common.config import get_settings

logger = structlog.get_logger(__name__)

SiemFormat = Literal["json", "cef"]

CEF_VERSION = "0"
DEVICE_VENDOR = "AnomalyAI"
DEVICE_PRODUCT = "AnomalyAI-Detector"
DEVICE_VERSION = "2.0"


def build_json_event(
    *,
    module: str,
    severity: str,
    summary: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Сформировать JSON-событие для Splunk HEC / ELK."""
    return {
        "time": datetime.now(UTC).isoformat(),
        "source": "anomaly-ai",
        "sourcetype": f"anomaly_ai:{module}",
        "event": {
            "module": module,
            "severity": severity,
            "summary": summary,
            "details": payload or {},
        },
    }


def build_cef_event(
    *,
    module: str,
    severity: str,
    summary: str,
    payload: dict[str, Any] | None = None,
    signature_id: str | None = None,
) -> str:
    """Сформировать CEF-строку.

    Формат: ``CEF:0|Vendor|Product|Version|SignatureID|Name|Severity|Extensions``
    """
    sev_map = {"low": 3, "medium": 6, "high": 8, "critical": 10}
    sev_num = sev_map.get(severity.lower(), 5)
    sig = signature_id or f"AA-{module.upper()}-001"

    header = "|".join([
        f"CEF:{CEF_VERSION}",
        DEVICE_VENDOR,
        DEVICE_PRODUCT,
        DEVICE_VERSION,
        sig,
        _cef_escape_header(summary),
        str(sev_num),
    ])

    extensions: list[str] = [f"cs1Label=module cs1={_cef_escape_value(module)}"]
    for k, v in (payload or {}).items():
        extensions.append(f"{_cef_escape_value(str(k))}={_cef_escape_value(str(v))}")
    return f"{header}|{' '.join(extensions)}"


def _cef_escape_header(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|")


def _cef_escape_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace("=", "\\=").replace("\n", "\\n")


class SiemDispatcher:
    """Асинхронная отправка событий в SIEM с retry-логикой."""

    def __init__(
        self,
        url: str,
        *,
        fmt: SiemFormat = "json",
        token: str | None = None,
        timeout_seconds: float = 5.0,
        max_attempts: int = 3,
    ) -> None:
        self.url = url
        self.fmt = fmt
        self.token = token
        self.timeout_seconds = timeout_seconds
        self.max_attempts = max_attempts

    async def send(
        self,
        *,
        module: str,
        severity: str,
        summary: str,
        payload: dict[str, Any] | None = None,
    ) -> bool:
        """Послать событие. Возвращает True при успехе."""
        if self.fmt == "json":
            body: Any = build_json_event(
                module=module, severity=severity, summary=summary, payload=payload,
            )
            content_type = "application/json"
        else:
            body = build_cef_event(
                module=module, severity=severity, summary=summary, payload=payload,
            )
            content_type = "text/plain"

        headers = {"Content-Type": content_type}
        if self.token:
            # Splunk HEC использует "Splunk <token>"; для других — Bearer.
            headers["Authorization"] = (
                f"Splunk {self.token}" if "splunk" in self.url.lower() else f"Bearer {self.token}"
            )

        try:
            async for attempt in AsyncRetrying(
                stop=stop_after_attempt(self.max_attempts),
                wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
                retry=retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException)),
                reraise=True,
            ):
                with attempt:
                    async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                        resp = await client.post(
                            self.url,
                            json=body if self.fmt == "json" else None,
                            content=body if self.fmt == "cef" else None,
                            headers=headers,
                        )
                        resp.raise_for_status()
                        logger.info(
                            "siem.event_sent",
                            module=module,
                            severity=severity,
                            status=resp.status_code,
                            attempts=attempt.retry_state.attempt_number,
                        )
                        return True
        except Exception as exc:
            logger.error("siem.send_failed", module=module, error=str(exc))
            return False
        return False


def dispatcher_from_settings() -> SiemDispatcher | None:
    """Создать диспатчер из ENV-настроек или вернуть None."""
    settings = get_settings()
    if not settings.siem_webhook_url:
        return None
    return SiemDispatcher(
        url=settings.siem_webhook_url,
        fmt=settings.siem_webhook_format,
        token=settings.siem_webhook_token,
    )


__all__ = [
    "SiemDispatcher",
    "SiemFormat",
    "build_cef_event",
    "build_json_event",
    "dispatcher_from_settings",
]
