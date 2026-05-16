"""API для детектирования дрейфа."""

from __future__ import annotations

import io

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from anomaly_ai.auth.rbac import require_analyst
from anomaly_ai.common.paths import backend_root
from anomaly_ai.ml.drift import detect_drift
from anomaly_ai.observability.metrics import update_drift_gauge
from anomaly_ai.schemas.drift import DriftReportPublic, FeatureDriftItem

router = APIRouter(prefix="/drift", tags=["drift"], dependencies=[Depends(require_analyst)])


@router.post("/{module}", response_model=DriftReportPublic)
async def compute_drift(
    module: str,
    current_csv: UploadFile = File(...),
) -> DriftReportPublic:
    """Сравнить распределение признаков в загруженном CSV с эталоном модуля."""
    if module not in {"network_anomaly", "waf_payload"}:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "NotFound", "message": f"Неизвестный модуль: {module}"},
        )

    # Эталон: берём sample-датасет из репозитория.
    samples = backend_root() / "data" / "samples"
    if module == "network_anomaly":
        ref_path = samples / "sample_network_flows.csv"
    else:
        ref_path = samples / "sample_payloads.csv"

    if not ref_path.exists():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": "ReferenceMissing", "message": f"Эталон не найден: {ref_path.name}"},
        )

    reference_df = pd.read_csv(ref_path)
    payload = await current_csv.read()
    try:
        current_df = pd.read_csv(io.BytesIO(payload))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "InvalidInput", "message": f"Некорректный CSV: {exc}"},
        ) from exc

    report = detect_drift(reference_df, current_df)
    update_drift_gauge(module, report.overall_psi)
    return DriftReportPublic(
        module=module,
        overall_psi=report.overall_psi,
        level=report.level,
        reference_size=report.reference_size,
        current_size=report.current_size,
        features=[FeatureDriftItem(**{
            "feature": f.feature,
            "psi": f.psi,
            "level": f.level,
            "ks_statistic": f.ks_statistic,
            "ks_p_value": f.ks_p_value,
            "chi2_statistic": f.chi2_statistic,
            "chi2_p_value": f.chi2_p_value,
        }) for f in report.features],
    )
