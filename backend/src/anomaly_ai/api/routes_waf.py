from __future__ import annotations

from fastapi import APIRouter, Depends

from anomaly_ai.api.dependencies import get_waf_service
from anomaly_ai.common.exceptions import InvalidInputError
from anomaly_ai.schemas.waf import WafBatchRequest, WafBatchResponse, WafPredictRequest, WafPredictResult
from anomaly_ai.waf_payload.service import WafPayloadService

router = APIRouter(prefix="/waf", tags=["waf"])


@router.post("/predict", response_model=WafPredictResult)
def predict_waf(
    body: WafPredictRequest,
    service: WafPayloadService = Depends(get_waf_service),
) -> WafPredictResult:
    if not body.payload.strip():
        raise InvalidInputError("Payload не должен быть пустым")
    return service.predict(body.payload)


@router.post("/batch-predict", response_model=WafBatchResponse)
def batch_predict_waf(
    body: WafBatchRequest,
    service: WafPayloadService = Depends(get_waf_service),
) -> WafBatchResponse:
    if any(not p.strip() for p in body.payloads):
        raise InvalidInputError("Каждый payload должен быть непустым")
    results = service.predict_batch(body.payloads)
    attacks = sum(1 for r in results if r.is_attack)
    trimmed: list[WafPredictResult] = []
    for r in results:
        trimmed.append(
            WafPredictResult(
                payload=r.payload,
                is_attack=r.is_attack,
                attack_type=r.attack_type,
                confidence=r.confidence,
                severity=r.severity,
                recommendation=None,
                model_version=None,
            )
        )
    return WafBatchResponse(total=len(results), attacks_detected=attacks, results=trimmed)
