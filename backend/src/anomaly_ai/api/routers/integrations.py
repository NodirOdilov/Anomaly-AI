"""Эндпоинты управления интеграциями (SIEM + Threat Intel)."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from anomaly_ai.auth.rbac import require_admin, require_analyst
from anomaly_ai.db.models import SiemEndpoint
from anomaly_ai.db.session import get_session
from anomaly_ai.integrations.siem import SiemDispatcher
from anomaly_ai.integrations.threat_intel import ThreatIntelService

router = APIRouter(prefix="/integrations", tags=["integrations"])


# === SIEM ===


class SiemEndpointCreate(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    url: str
    format: str = Field(default="json", pattern="^(json|cef)$")
    token: str | None = None
    min_confidence: float = Field(default=0.85, ge=0.0, le=1.0)


class SiemEndpointPublic(BaseModel):
    id: int
    name: str
    url: str
    format: str
    min_confidence: float
    is_active: bool
    last_success_at: datetime | None
    last_error: str | None
    created_at: datetime


@router.get(
    "/siem",
    response_model=list[SiemEndpointPublic],
    dependencies=[Depends(require_analyst)],
)
async def list_siem(session: AsyncSession = Depends(get_session)) -> list[SiemEndpointPublic]:
    rows = (await session.execute(select(SiemEndpoint).order_by(SiemEndpoint.created_at.desc()))).scalars().all()
    return [SiemEndpointPublic.model_validate(r, from_attributes=True) for r in rows]


@router.post(
    "/siem",
    response_model=SiemEndpointPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
async def create_siem(
    body: SiemEndpointCreate,
    session: AsyncSession = Depends(get_session),
) -> SiemEndpointPublic:
    row = SiemEndpoint(
        name=body.name,
        url=body.url,
        format=body.format,
        token=body.token,
        min_confidence=body.min_confidence,
    )
    session.add(row)
    await session.flush()
    return SiemEndpointPublic.model_validate(row, from_attributes=True)


@router.post(
    "/siem/{endpoint_id}/test",
    dependencies=[Depends(require_admin)],
)
async def test_siem(
    endpoint_id: int,
    session: AsyncSession = Depends(get_session),
) -> dict:
    row = await session.get(SiemEndpoint, endpoint_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    dispatcher = SiemDispatcher(url=row.url, fmt=row.format, token=row.token)
    ok = await dispatcher.send(
        module="test",
        severity="low",
        summary="Тестовое событие от Anomaly AI",
        payload={"test": True, "timestamp": datetime.now(timezone.utc).isoformat()},
    )
    if ok:
        row.last_success_at = datetime.now(timezone.utc)
        row.last_error = None
    else:
        row.last_error = "Не удалось отправить тестовое событие"
    return {"ok": ok}


@router.delete(
    "/siem/{endpoint_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
async def delete_siem(
    endpoint_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    row = await session.get(SiemEndpoint, endpoint_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await session.delete(row)


# === Threat Intel ===


class ThreatLookupRequest(BaseModel):
    indicator_type: str = Field(pattern="^(ip|domain|hash|url)$")
    indicator: str = Field(min_length=1, max_length=512)


@router.post(
    "/threat-intel/lookup",
    dependencies=[Depends(require_analyst)],
)
async def threat_lookup(
    body: ThreatLookupRequest,
    session: AsyncSession = Depends(get_session),
) -> dict:
    service = ThreatIntelService(session)
    verdict = await service.lookup(indicator=body.indicator, indicator_type=body.indicator_type)
    return {
        "indicator": verdict.indicator,
        "indicator_type": verdict.indicator_type,
        "matched": verdict.matched,
        "severity": verdict.severity,
        "source": verdict.source,
        "description": verdict.description,
    }


@router.post(
    "/threat-intel/import",
    dependencies=[Depends(require_admin)],
)
async def threat_import(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
) -> dict:
    payload = await file.read()
    text = payload.decode("utf-8")
    service = ThreatIntelService(session)
    count = await service.import_csv(text)
    return {"imported": count}
