"""Тесты файлового реестра моделей."""

from __future__ import annotations

from pathlib import Path

from anomaly_ai.ml.registry import ModelRegistry


def test_register_and_activate(tmp_path: Path) -> None:
    registry = ModelRegistry(root=tmp_path)
    entry_v1 = registry.register(
        "waf_payload",
        "1.0.0",
        artifact_bytes=b"fake_artifact_v1",
        metadata={"metrics": {"accuracy": 0.9}},
        activate=True,
    )
    assert entry_v1.is_active is True
    assert entry_v1.artifact_path.exists()

    registry.register(
        "waf_payload",
        "1.1.0",
        artifact_bytes=b"fake_artifact_v2",
        metadata={"metrics": {"accuracy": 0.94}},
    )
    assert {e.version for e in registry.list_versions("waf_payload")} == {"1.0.0", "1.1.0"}
    assert registry.get_active("waf_payload").version == "1.0.0"

    registry.activate("waf_payload", "1.1.0")
    assert registry.get_active("waf_payload").version == "1.1.0"


def test_list_modules_empty(tmp_path: Path) -> None:
    assert ModelRegistry(root=tmp_path).list_modules() == []
