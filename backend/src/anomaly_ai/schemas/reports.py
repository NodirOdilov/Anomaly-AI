from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ModuleMetrics(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    false_positive_rate: float
    false_negative_rate: float
    notes: str | None = None


class ReportsSummaryResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    network_anomaly: ModuleMetrics
    waf_payload: ModuleMetrics


class ModelStatusItem(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    loaded: bool
    version: str | None = None
    model_type: str | None = None
    path: str | None = None
    message: str | None = None


class ModelsStatusResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    network_anomaly: ModelStatusItem
    waf_payload: ModelStatusItem
