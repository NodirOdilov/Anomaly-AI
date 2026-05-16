"""Тесты SIEM-форматирования (без сетевых вызовов)."""

from __future__ import annotations

from anomaly_ai.integrations.siem import build_cef_event, build_json_event


def test_json_event_structure() -> None:
    event = build_json_event(
        module="waf_payload",
        severity="high",
        summary="SQLi detected",
        payload={"confidence": 0.92, "type": "sql_injection"},
    )
    assert event["sourcetype"] == "anomaly_ai:waf_payload"
    assert event["event"]["severity"] == "high"
    assert event["event"]["details"]["confidence"] == 0.92


def test_cef_event_header_and_severity() -> None:
    line = build_cef_event(
        module="network_anomaly",
        severity="critical",
        summary="UDP flood detected",
        payload={"src": "10.0.0.1", "score": 0.99},
    )
    assert line.startswith("CEF:0|AnomalyAI|AnomalyAI-Detector|2.0|")
    # severity=critical → 10
    assert "|10|" in line
    # extensions
    assert "src=10.0.0.1" in line
    assert "score=0.99" in line


def test_cef_escapes_pipe_in_summary() -> None:
    line = build_cef_event(
        module="x",
        severity="low",
        summary="pipe|inside",
    )
    # `|` в имени должна быть экранирована.
    assert "pipe\\|inside" in line
