from __future__ import annotations

from pathlib import Path
from typing import Any

from anomaly_ai.schemas.reports import ModuleMetrics, ReportsSummaryResponse
from anomaly_ai.services.artifact_loader import (
    ModelArtifactError,
    ModelNotFoundError,
    load_network_artifact,
    load_waf_artifact,
)
from anomaly_ai.services.model_registry import default_network_model_path, default_waf_model_path


def _zero_metrics(model_name: str, notes: str | None = None) -> ModuleMetrics:
    return ModuleMetrics(
        model=model_name,
        accuracy=0.0,
        precision=0.0,
        recall=0.0,
        f1=0.0,
        false_positive_rate=0.0,
        false_negative_rate=0.0,
        notes=notes,
    )


def _metrics_from_artifact(artifact: dict[str, Any], fallback_model: str) -> ModuleMetrics:
    m = artifact.get("metrics") or {}
    return ModuleMetrics(
        model=fallback_model,
        accuracy=float(m.get("accuracy", 0.0)),
        precision=float(m.get("precision", 0.0)),
        recall=float(m.get("recall", 0.0)),
        f1=float(m.get("f1", 0.0)),
        false_positive_rate=float(m.get("false_positive_rate", 0.0)),
        false_negative_rate=float(m.get("false_negative_rate", 0.0)),
        notes="Загружено из обученного артефакта; при обучении только на sample data это demo/baseline.",
    )


def build_summary(root: Path | None = None) -> ReportsSummaryResponse:
    waf_path = default_waf_model_path(root)
    net_path = default_network_model_path(root)

    waf = _zero_metrics(
        "TfidfVectorizer + LogisticRegression",
        notes="Артефакт на диске не найден — выполните `python -m anomaly_ai.waf_payload.train`.",
    )
    net = _zero_metrics(
        "RandomForestClassifier (MinMaxScaler pipeline)",
        notes="Артефакт на диске не найден — выполните `python -m anomaly_ai.network_anomaly.train`.",
    )

    try:
        waf_art = load_waf_artifact(waf_path)
        waf = _metrics_from_artifact(waf_art, "TfidfVectorizer + LogisticRegression")
    except (ModelNotFoundError, ModelArtifactError, OSError):
        pass

    try:
        net_art = load_network_artifact(net_path)
        net = _metrics_from_artifact(net_art, "RandomForestClassifier")
    except (ModelNotFoundError, ModelArtifactError, OSError):
        pass

    return ReportsSummaryResponse(network_anomaly=net, waf_payload=waf)
