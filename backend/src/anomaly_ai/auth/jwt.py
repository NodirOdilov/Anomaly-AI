"""Выпуск и валидация JWT-токенов."""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Literal

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError

from anomaly_ai.common.config import get_settings

TokenType = Literal["access", "refresh"]


class JwtError(Exception):
    """Базовая ошибка работы с JWT (невалидный или просроченный)."""


@dataclass(frozen=True)
class JwtClaims:
    """Декодированное содержимое токена."""

    sub: str               # user_id как строка
    role: str
    type: TokenType
    jti: str               # JWT ID (для отзыва refresh-токенов)
    issued_at: datetime
    expires_at: datetime
    extra: dict[str, Any]


def _now() -> datetime:
    return datetime.now(UTC)


def _encode(payload: dict[str, Any]) -> str:
    settings = get_settings()
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_access_token(user_id: int | str, role: str, extra: dict[str, Any] | None = None) -> str:
    """Выпустить access-токен (короткоживущий, для API-вызовов)."""
    settings = get_settings()
    now = _now()
    payload = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.jwt_access_ttl_minutes)).timestamp()),
        "jti": secrets.token_urlsafe(16),
        **(extra or {}),
    }
    return _encode(payload)


def create_refresh_token(user_id: int | str, role: str) -> tuple[str, str, datetime]:
    """Выпустить refresh-токен. Возвращает ``(token, jti, expires_at)``.

    ``jti`` нужно сохранить в БД (таблица ``refresh_tokens``) для возможности отзыва.
    """
    settings = get_settings()
    now = _now()
    jti = secrets.token_urlsafe(32)
    expires_at = now + timedelta(days=settings.jwt_refresh_ttl_days)
    payload = {
        "sub": str(user_id),
        "role": role,
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
        "jti": jti,
    }
    return _encode(payload), jti, expires_at


def decode_token(token: str, expected_type: TokenType | None = None) -> JwtClaims:
    """Декодировать и провалидировать токен.

    :raises JwtError: если токен невалидный, просрочен или не того типа.
    """
    settings = get_settings()
    try:
        raw = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except ExpiredSignatureError as exc:
        raise JwtError("Срок действия токена истёк") from exc
    except (InvalidTokenError, PyJWTError) as exc:
        raise JwtError(f"Невалидный токен: {exc}") from exc

    token_type = raw.get("type")
    if expected_type and token_type != expected_type:
        raise JwtError(f"Ожидался токен типа '{expected_type}', получен '{token_type}'")

    known = {"sub", "role", "type", "jti", "iat", "exp"}
    extra = {k: v for k, v in raw.items() if k not in known}

    return JwtClaims(
        sub=str(raw["sub"]),
        role=str(raw.get("role", "viewer")),
        type=token_type,  # type: ignore[arg-type]
        jti=str(raw.get("jti", "")),
        issued_at=datetime.fromtimestamp(int(raw["iat"]), tz=UTC),
        expires_at=datetime.fromtimestamp(int(raw["exp"]), tz=UTC),
        extra=extra,
    )


__all__ = [
    "JwtClaims",
    "JwtError",
    "TokenType",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
]
