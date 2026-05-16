"""Высокоуровневые операции аутентификации (login, register, refresh).

Используется роутером :mod:`anomaly_ai.api.routers.auth`. Возвращает ORM-объекты
или готовые токены; HTTP-маппинг делается в роутере.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from anomaly_ai.auth.jwt import (
    JwtError,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from anomaly_ai.auth.password import hash_password, verify_password
from anomaly_ai.common.exceptions import AppError
from anomaly_ai.db.models import RefreshToken, User, UserRole


class AuthError(AppError):
    """Ошибка аутентификации/регистрации."""

    code = "AuthError"


async def register_user(
    session: AsyncSession,
    *,
    email: str,
    password: str,
    full_name: str | None = None,
    role: UserRole = UserRole.VIEWER,
) -> User:
    """Создать нового пользователя. Бросает AuthError если email занят."""
    existing = await session.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        raise AuthError(f"Пользователь с email '{email}' уже существует")

    user = User(
        email=email,
        full_name=full_name,
        hashed_password=hash_password(password),
        role=role,
        is_active=True,
    )
    session.add(user)
    await session.flush()
    return user


async def authenticate(session: AsyncSession, *, email: str, password: str) -> User:
    """Проверить email+пароль. Бросает AuthError если данные неверны."""
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise AuthError("Неверный email или пароль")
    if not verify_password(password, user.hashed_password):
        raise AuthError("Неверный email или пароль")

    user.last_login_at = datetime.now(timezone.utc)
    return user


async def issue_token_pair(
    session: AsyncSession,
    *,
    user: User,
    user_agent: str | None = None,
    ip: str | None = None,
) -> tuple[str, str, int, int]:
    """Выпустить пару access+refresh и сохранить refresh в БД.

    Возвращает ``(access_token, refresh_token, access_expires_in, refresh_expires_in)``
    в секундах.
    """
    from anomaly_ai.common.config import get_settings

    settings = get_settings()
    access = create_access_token(user.id, user.role.value)
    refresh, jti, refresh_exp = create_refresh_token(user.id, user.role.value)

    session.add(
        RefreshToken(
            user_id=user.id,
            jti=jti,
            expires_at=refresh_exp,
            user_agent=user_agent,
            ip=ip,
        ),
    )
    return (
        access,
        refresh,
        settings.jwt_access_ttl_minutes * 60,
        settings.jwt_refresh_ttl_days * 86400,
    )


async def refresh_access_token(
    session: AsyncSession,
    *,
    refresh_token_raw: str,
) -> tuple[str, int]:
    """Обновить access-токен по валидному refresh. Возвращает (token, exp_in_sec)."""
    try:
        claims = decode_token(refresh_token_raw, expected_type="refresh")
    except JwtError as exc:
        raise AuthError(f"Невалидный refresh-токен: {exc}") from exc

    # Проверяем, что refresh не отозван.
    result = await session.execute(
        select(RefreshToken).where(RefreshToken.jti == claims.jti),
    )
    stored = result.scalar_one_or_none()
    if stored is None or stored.revoked_at is not None:
        raise AuthError("Refresh-токен отозван или не зарегистрирован")

    from anomaly_ai.common.config import get_settings

    settings = get_settings()
    new_access = create_access_token(int(claims.sub), claims.role)
    return new_access, settings.jwt_access_ttl_minutes * 60


async def revoke_refresh_token(session: AsyncSession, *, jti: str) -> None:
    """Пометить refresh-токен отозванным (для logout)."""
    result = await session.execute(select(RefreshToken).where(RefreshToken.jti == jti))
    stored = result.scalar_one_or_none()
    if stored is None or stored.revoked_at is not None:
        return
    stored.revoked_at = datetime.now(timezone.utc)


__all__ = [
    "AuthError",
    "authenticate",
    "issue_token_pair",
    "refresh_access_token",
    "register_user",
    "revoke_refresh_token",
]
