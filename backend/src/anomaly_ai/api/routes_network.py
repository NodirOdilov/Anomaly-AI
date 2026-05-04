from __future__ import annotations

import io
from typing import Any

import pandas as pd
from fastapi import APIRouter, Depends, File, UploadFile

from anomaly_ai.api.dependencies import get_network_service
from anomaly_ai.common.exceptions import InvalidInputError
from anomaly_ai.schemas.network import NetworkCsvResponse, NetworkPredictResponse
from anomaly_ai.network_anomaly.service import NetworkAnomalyService

router = APIRouter(prefix="/network", tags=["network"])


@router.post("/predict", response_model=NetworkPredictResponse)
def predict_network(
    body: dict[str, Any],
    service: NetworkAnomalyService = Depends(get_network_service),
) -> NetworkPredictResponse:
    if not body:
        raise InvalidInputError("JSON body должен содержать признаки сетевого потока")
    return service.predict_row(body)


@router.post("/upload-csv", response_model=NetworkCsvResponse)
async def upload_network_csv(
    file: UploadFile = File(...),
    service: NetworkAnomalyService = Depends(get_network_service),
) -> NetworkCsvResponse:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise InvalidInputError("Загрузите файл формата .csv")
    raw = await file.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InvalidInputError("CSV должен быть в кодировке UTF-8") from exc
    try:
        df = pd.read_csv(io.StringIO(text))
    except Exception as exc:  # noqa: BLE001
        raise InvalidInputError(f"Некорректный CSV: {exc}") from exc
    if df.empty:
        raise InvalidInputError("CSV не содержит строк")
    try:
        return service.predict_csv(df, label_column="Label")
    except InvalidInputError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise InvalidInputError(f"Не удалось выполнить оценку CSV: {exc}") from exc
