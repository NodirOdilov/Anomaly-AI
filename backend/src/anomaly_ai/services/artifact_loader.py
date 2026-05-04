from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib

from anomaly_ai.common.exceptions import ModelArtifactError, ModelNotFoundError

_REQUIRED_KEYS = frozenset(
    {"project", "model", "features", "labels", "model_type", "version", "created_at", "metrics"}
)


def _validate_artifact(data: dict[str, Any], expected_type: str) -> None:
    missing = _REQUIRED_KEYS - data.keys()
    if missing:
        raise ModelArtifactError(f"Artifact missing keys: {sorted(missing)}")
    if data.get("model_type") != expected_type:
        raise ModelArtifactError(
            f"Expected model_type={expected_type!r}, got {data.get('model_type')!r}"
        )
    if not str(data.get("version", "")).strip():
        raise ModelArtifactError("Artifact version is empty")
    if data.get("model") is None:
        raise ModelArtifactError("Artifact model object is missing")


def load_artifact(path: Path, expected_type: str) -> dict[str, Any]:
    if not path.exists():
        raise ModelNotFoundError(f"Model artifact not found: {path}")
    try:
        data = joblib.load(path)
    except Exception as exc:  # noqa: BLE001
        raise ModelArtifactError(f"Failed to load artifact: {exc}") from exc
    if not isinstance(data, dict):
        raise ModelArtifactError("Artifact file must contain a dict bundle")
    _validate_artifact(data, expected_type)
    return data


def load_waf_artifact(path: Path) -> dict[str, Any]:
    return load_artifact(path, "waf_payload_detector")


def load_network_artifact(path: Path) -> dict[str, Any]:
    return load_artifact(path, "network_anomaly_detector")
