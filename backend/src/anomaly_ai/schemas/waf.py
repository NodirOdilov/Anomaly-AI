from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class WafPredictRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    payload: str = Field(..., min_length=1)


class WafPredictResult(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    payload: str
    is_attack: bool
    attack_type: str
    confidence: float
    severity: str
    recommendation: str | None = None
    model_version: str | None = None


class WafBatchRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    payloads: list[str] = Field(..., min_length=1)


class WafBatchResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    total: int
    attacks_detected: int
    results: list[WafPredictResult]
