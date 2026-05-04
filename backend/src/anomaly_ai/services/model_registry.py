from __future__ import annotations

from pathlib import Path

from anomaly_ai.common.config import get_settings
from anomaly_ai.common.paths import backend_root, resolve_under_root


def default_waf_model_path(root: Path | None = None) -> Path:
    base = root or backend_root()
    settings = get_settings()
    return resolve_under_root(f"{settings.model_dir}/waf_payload_model.joblib", base)


def default_network_model_path(root: Path | None = None) -> Path:
    base = root or backend_root()
    settings = get_settings()
    return resolve_under_root(f"{settings.model_dir}/network_anomaly_model.joblib", base)
