"""Просмотр журнала аудита (admin/analyst)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from anomaly_ai.auth.rbac import require_analyst
from anomaly_ai.db.models import AuditLog
from anomaly_ai.db.session import get_session
from anomaly_ai.schemas.admin import AuditLogPage, AuditLogPublic, PaginationMeta

router = APIRouter(prefix="/admin/audit", tags=["admin", "audit"], dependencies=[Depends(require_analyst)])


@router.get("", response_model=AuditLogPage)
async def list_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    user_id: int | None = Query(default=None),
    action: str | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
) -> AuditLogPage:
    """Постраничный список записей аудита с фильтрами."""
    base = select(AuditLog)
    count_base = select(func.count()).select_from(AuditLog)
    if user_id is not None:
        base = base.where(AuditLog.user_id == user_id)
        count_base = count_base.where(AuditLog.user_id == user_id)
    if action is not None:
        base = base.where(AuditLog.action.ilike(f"%{action}%"))
        count_base = count_base.where(AuditLog.action.ilike(f"%{action}%"))

    total = (await session.execute(count_base)).scalar_one()
    stmt = base.order_by(AuditLog.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    rows = (await session.execute(stmt)).scalars().all()
    return AuditLogPage(
        items=[AuditLogPublic.model_validate(r, from_attributes=True) for r in rows],
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
            pages=(total + page_size - 1) // page_size if total else 0,
        ),
    )
