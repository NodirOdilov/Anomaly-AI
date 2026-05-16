"""Алерты: REST + WebSocket для real-time подписки."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from anomaly_ai.auth.dependencies import AuthPrincipal, get_current_principal
from anomaly_ai.auth.jwt import JwtError, decode_token
from anomaly_ai.auth.rbac import require_analyst
from anomaly_ai.common.config import get_settings
from anomaly_ai.db.models import Alert, AlertStatus, User
from anomaly_ai.db.session import get_session, session_scope
from anomaly_ai.integrations.alert_manager import alert_manager
from anomaly_ai.schemas.admin import AlertAckRequest, AlertPublic, PaginationMeta

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=dict, dependencies=[Depends(require_analyst)])
async def list_alerts(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    status_filter: str | None = Query(default=None, alias="status"),
    session: AsyncSession = Depends(get_session),
) -> dict:
    base = select(Alert)
    count_base = select(func.count()).select_from(Alert)
    if status_filter:
        try:
            st = AlertStatus(status_filter)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"error": "ValidationError", "message": f"Неизвестный статус: {status_filter}"},
            ) from exc
        base = base.where(Alert.status == st)
        count_base = count_base.where(Alert.status == st)

    total = (await session.execute(count_base)).scalar_one()
    stmt = base.order_by(Alert.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    rows = (await session.execute(stmt)).scalars().all()
    return {
        "items": [AlertPublic.model_validate(r, from_attributes=True).model_dump() for r in rows],
        "meta": PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
            pages=(total + page_size - 1) // page_size if total else 0,
        ).model_dump(),
    }


@router.patch("/{alert_id}", response_model=AlertPublic, dependencies=[Depends(require_analyst)])
async def acknowledge_alert(
    alert_id: int,
    body: AlertAckRequest,
    principal: AuthPrincipal = Depends(get_current_principal),
    session: AsyncSession = Depends(get_session),
) -> AlertPublic:
    alert = await session.get(Alert, alert_id)
    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "NotFound", "message": "Алерт не найден"},
        )
    alert.status = AlertStatus(body.status)
    alert.notes = body.notes
    alert.acknowledged_by = principal.user_id or None
    alert.acknowledged_at = datetime.now(timezone.utc)
    return AlertPublic.model_validate(alert, from_attributes=True)


# === WebSocket для live-алертов ===


@router.websocket("/ws")
async def alerts_stream(websocket: WebSocket, token: str | None = Query(default=None)) -> None:
    """Подписка на live-алерты.

    Аутентификация: JWT в query-параметре ``?token=...`` (WebSocket не поддерживает
    стандартные Authorization-заголовки во всех клиентах). В dev (``AUTH_REQUIRED=false``)
    токен не обязателен.
    """
    settings = get_settings()
    user_id: int | None = None

    if settings.auth_required:
        if not token:
            await websocket.close(code=4401, reason="missing token")
            return
        try:
            claims = decode_token(token, expected_type="access")
            user_id = int(claims.sub)
        except JwtError:
            await websocket.close(code=4401, reason="invalid token")
            return

    await websocket.accept()
    queue = await alert_manager.subscribe()
    try:
        while True:
            try:
                alert = await asyncio.wait_for(queue.get(), timeout=30.0)
                await websocket.send_text(alert.to_json())
            except TimeoutError:
                # Heartbeat
                await websocket.send_json({"type": "ping", "user_id": user_id})
    except WebSocketDisconnect:
        pass
    finally:
        await alert_manager.unsubscribe(queue)
