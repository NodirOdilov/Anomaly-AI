"""Админский CRUD пользователей."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from anomaly_ai.auth.rbac import require_admin
from anomaly_ai.db.models import User, UserRole
from anomaly_ai.db.session import get_session
from anomaly_ai.schemas.admin import PaginationMeta, UserUpdateRequest
from anomaly_ai.schemas.auth import UserPublic

router = APIRouter(prefix="/admin/users", tags=["admin", "users"], dependencies=[Depends(require_admin)])


@router.get("", response_model=dict)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Постраничный список пользователей."""
    total = (await session.execute(select(func.count()).select_from(User))).scalar_one()
    stmt = (
        select(User)
        .order_by(User.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    items = (await session.execute(stmt)).scalars().all()
    return {
        "items": [UserPublic.model_validate(u, from_attributes=True).model_dump() for u in items],
        "meta": PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
            pages=(total + page_size - 1) // page_size if total else 0,
        ).model_dump(),
    }


@router.patch("/{user_id}", response_model=UserPublic)
async def update_user(
    user_id: int,
    body: UserUpdateRequest,
    session: AsyncSession = Depends(get_session),
) -> UserPublic:
    """Обновить роль/активность пользователя."""
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "NotFound", "message": "Пользователь не найден"},
        )
    if body.full_name is not None:
        user.full_name = body.full_name
    if body.role is not None:
        try:
            user.role = UserRole(body.role)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"error": "ValidationError", "message": f"Неизвестная роль: {body.role}"},
            ) from exc
    if body.is_active is not None:
        user.is_active = body.is_active
    return UserPublic.model_validate(user, from_attributes=True)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    """Удалить пользователя."""
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await session.delete(user)
