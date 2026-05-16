"""API-ключи для машинной аутентификации.

Формат: ``aa_live_<32_url_safe_random>``. Префикс показывается в UI и хранится
открыто; полное значение — только в момент создания. В БД лежит SHA-256 хэш.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from dataclasses import dataclass

from anomaly_ai.common.config import get_settings

DEFAULT_KEY_BYTES = 32  # → 43 url-safe символа


@dataclass(frozen=True)
class GeneratedApiKey:
    """Результат создания API-ключа."""

    plain: str       # Полный ключ, показать ОДИН раз пользователю
    prefix: str      # Для отображения в UI (aa_live_xxxx…)
    hashed: str      # Сохранить в БД


def generate_api_key(prefix: str | None = None) -> GeneratedApiKey:
    """Сгенерировать новый ключ. Префикс по умолчанию из настроек."""
    settings = get_settings()
    actual_prefix = prefix or settings.api_key_prefix
    body = secrets.token_urlsafe(DEFAULT_KEY_BYTES)
    plain = f"{actual_prefix}_{body}"
    visible_prefix = f"{actual_prefix}_{body[:6]}"
    return GeneratedApiKey(plain=plain, prefix=visible_prefix, hashed=hash_api_key(plain))


def hash_api_key(plain: str) -> str:
    """SHA-256 от полного ключа (hex). Достаточно для проверки равенства."""
    return hashlib.sha256(plain.encode("utf-8")).hexdigest()


def verify_api_key(plain: str, hashed: str) -> bool:
    """Константная по времени проверка."""
    return hmac.compare_digest(hash_api_key(plain), hashed)


def extract_prefix(plain: str) -> str:
    """Вернуть видимую часть для логирования (без раскрытия секрета)."""
    parts = plain.split("_")
    if len(parts) < 3:
        return "invalid"
    return f"{parts[0]}_{parts[1]}_{parts[2][:6]}"


__all__ = [
    "DEFAULT_KEY_BYTES",
    "GeneratedApiKey",
    "extract_prefix",
    "generate_api_key",
    "hash_api_key",
    "verify_api_key",
]
