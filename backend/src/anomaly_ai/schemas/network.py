from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class NetworkPredictResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    prediction: str
    confidence: float
    severity: str
    recommendation: str
    model_version: str


class NetworkRowResult(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    row: int
    prediction: str
    confidence: float


class NetworkCsvResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    total_flows: int
    benign: int
    suspicious: int
    top_prediction: str
    results: list[NetworkRowResult]
