from __future__ import annotations

from functools import lru_cache

from fastapi import HTTPException, status

from anomaly_ai.common.exceptions import ModelArtifactError, ModelNotFoundError
from anomaly_ai.network_anomaly.service import NetworkAnomalyService
from anomaly_ai.services.artifact_loader import load_network_artifact, load_waf_artifact
from anomaly_ai.services.model_registry import default_network_model_path, default_waf_model_path
from anomaly_ai.waf_payload.service import WafPayloadService


@lru_cache
def _waf_service_cached() -> WafPayloadService:
    path = default_waf_model_path()
    artifact = load_waf_artifact(path)
    return WafPayloadService(artifact)


@lru_cache
def _network_service_cached() -> NetworkAnomalyService:
    path = default_network_model_path()
    artifact = load_network_artifact(path)
    return NetworkAnomalyService(artifact)


def get_waf_service() -> WafPayloadService:
    try:
        return _waf_service_cached()
    except ModelNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": exc.code, "message": exc.message},
        ) from exc
    except ModelArtifactError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": exc.code, "message": exc.message},
        ) from exc


def get_network_service() -> NetworkAnomalyService:
    try:
        return _network_service_cached()
    except ModelNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"error": exc.code, "message": exc.message},
        ) from exc
    except ModelArtifactError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": exc.code, "message": exc.message},
        ) from exc


def clear_model_caches() -> None:
    """Test helper: reset cached services after writing new artifacts."""
    _waf_service_cached.cache_clear()
    _network_service_cached.cache_clear()
