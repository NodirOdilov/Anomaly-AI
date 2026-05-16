from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter

from anomaly_ai.schemas.reports import ModelsStatusResponse, ModelStatusItem
from anomaly_ai.services.artifact_loader import (
    ModelArtifactError,
    ModelNotFoundError,
    load_network_artifact,
    load_waf_artifact,
)
from anomaly_ai.services.model_registry import default_network_model_path, default_waf_model_path

router = APIRouter(prefix="/models", tags=["models"])


def _status_for(path: Path, loader, model_type: str) -> ModelStatusItem:
    if not path.exists():
        return ModelStatusItem(
            loaded=False,
            model_type=model_type,
            path=str(path),
            message="Артефакт не найден",
        )
    try:
        art = loader(path)
        return ModelStatusItem(
            loaded=True,
            version=str(art.get("version")),
            model_type=str(art.get("model_type")),
            path=str(path),
        )
    except ModelArtifactError as exc:
        return ModelStatusItem(loaded=False, model_type=model_type, path=str(path), message=exc.message)
    except ModelNotFoundError as exc:
        return ModelStatusItem(loaded=False, model_type=model_type, path=str(path), message=exc.message)


@router.get("/status", response_model=ModelsStatusResponse)
def models_status() -> ModelsStatusResponse:
    waf_path = default_waf_model_path()
    net_path = default_network_model_path()
    return ModelsStatusResponse(
        waf_payload=_status_for(waf_path, load_waf_artifact, "waf_payload_detector"),
        network_anomaly=_status_for(net_path, load_network_artifact, "network_anomaly_detector"),
    )
