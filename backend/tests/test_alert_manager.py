"""Тесты pub-sub менеджера алертов."""

from __future__ import annotations

import asyncio

import pytest

from anomaly_ai.integrations.alert_manager import AlertManager, AlertPayload


@pytest.mark.asyncio
async def test_subscribe_receives_emit() -> None:
    mgr = AlertManager()
    queue = await mgr.subscribe()
    alert = AlertPayload(severity="high", module="waf", summary="SQLi")
    await mgr.emit(alert)
    received = await asyncio.wait_for(queue.get(), timeout=1.0)
    assert received.summary == "SQLi"
    await mgr.unsubscribe(queue)


@pytest.mark.asyncio
async def test_multiple_subscribers_each_get_alert() -> None:
    mgr = AlertManager()
    q1 = await mgr.subscribe()
    q2 = await mgr.subscribe()
    await mgr.emit(AlertPayload(severity="medium", module="net", summary="HTTP scan"))
    a1 = await asyncio.wait_for(q1.get(), timeout=1.0)
    a2 = await asyncio.wait_for(q2.get(), timeout=1.0)
    assert a1.summary == a2.summary == "HTTP scan"
