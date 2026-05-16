"""FastAPI зависимости для извлечения текущего пользователя.

Поддерживает два способа аутентификации:

1. ``Authorization: Bearer <jwt>`` — для UI-сессий.
2. ``X-API-Key: aa_live_...`` — для машинных интеграций.

Если включена ``AUTH_REQUIRED=false`` (dev), :func:`get_optional_principal`
возвращает ``None`` для эндпоинтов, которые умеют работать в режиме
анонимного демо.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from anomaly_ai.auth.api_keys import hash_api_key
from anomaly_ai.auth.jwt import JwtError, decode_token
from anomaly_ai.common.config import get_settings
from anomaly_ai.db.models import ApiKey, User, UserRole
from anomaly_ai.db.session import get_session

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class AuthPrincipal:
    """Аутентифицированный субъект (пользователь или машинный клиент)."""

    user_id: int
    email: str
    role: UserRole
    method: str  # "jwt" | "api_key"
    api_key_id: int | None = None

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN


def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"error": "Unauthorized", "message": detail},
        headers={"WWW-Authenticate": "Bearer"},
    )


async def _resolve_jwt(token: str, session: AsyncSession) -> AuthPrincipal:
    try:
        claims = decode_token(token, expected_type="access")
    except JwtError as exc:
        raise _unauthorized(str(exc)) from exc

    user = await session.get(User, int(claims.sub))
    if user is None or not user.is_active:
        raise _unauthorized("Пользователь не найден или деактивирован")
    return AuthPrincipal(user_id=user.id, email=user.email, role=user.role, method="jwt")


async def _resolve_api_key(raw_key: str, session: AsyncSession) -> AuthPrincipal:
    hashed = hash_api_key(raw_key)
    stmt = select(ApiKey).where(ApiKey.hashed_key == hashed)
    result = await session.execute(stmt)
    api_key = result.scalar_one_or_none()
    if api_key is None:
        raise _unauthorized("Невалидный API-ключ")

    now = datetime.now(UTC)
    if api_key.revoked_at is not None:
        raise _unauthorized("API-ключ отозван")
    if api_key.expires_at is not None and api_key.expires_at < now:
        raise _unauthorized("Срок действия API-ключа истёк")

    user = await session.get(User, api_key.user_id)
    if user is None or not user.is_active:
        raise _unauthorized("Пользователь API-ключа неактивен")

    # Best-effort обновление last_used_at (не блокируем при ошибке).
    api_key.last_used_at = now
    try:
        await session.commit()
    except Exception:
        await session.rollback()

    return AuthPrincipal(
        user_id=user.id,
        email=user.email,
        role=user.role,
        method="api_key",
        api_key_id=api_key.id,
    )


async def get_optional_principal(
    bearer: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    session: AsyncSession = Depends(get_session),
) -> AuthPrincipal | None:
    """Вернуть субъекта если он есть; None — иначе. Не бросает 401."""
    if bearer and bearer.credentials:
        try:
            return await _resolve_jwt(bearer.credentials, session)
        except HTTPException:
            return None
    if x_api_key:
        try:
            return await _resolve_api_key(x_api_key, session)
        except HTTPException:
            return None
    return None


async def get_current_principal(
    bearer: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    session: AsyncSession = Depends(get_session),
) -> AuthPrincipal:
    """Жёстко требовать аутентификацию. 401 если не предоставлена.

    В режиме ``AUTH_REQUIRED=false`` возвращает синтетического анонимного
    "viewer" субъекта — удобно для dev и Vercel-демо.
    """
    settings = get_settings()
    if bearer and bearer.credentials:
        return await _resolve_jwt(bearer.credentials, session)
    if x_api_key:
        return await _resolve_api_key(x_api_key, session)

    if not settings.auth_required:
        return AuthPrincipal(
            user_id=0,
            email="anonymous@demo.local",
            role=UserRole.VIEWER,
            method="anonymous",
        )

    raise _unauthorized("Требуется Bearer-токен или X-API-Key заголовок")


__all__ = ["AuthPrincipal", "get_current_principal", "get_optional_principal"]
