"""Хэширование паролей через Argon2 (passlib)."""

from __future__ import annotations

from passlib.context import CryptContext

# Argon2id — современный рекомендованный OWASP алгоритм.
_pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,   # 64 MiB
    argon2__time_cost=3,
    argon2__parallelism=4,
)


def hash_password(plain: str) -> str:
    """Захэшировать пароль. Никогда не логируйте plain."""
    if not plain:
        raise ValueError("Пароль не может быть пустым")
    return _pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Проверить пароль против хэша. Константно по времени."""
    try:
        return _pwd_context.verify(plain, hashed)
    except Exception:
        return False


def needs_rehash(hashed: str) -> bool:
    """Нужно ли перехэшировать (например, после обновления параметров)."""
    return _pwd_context.needs_update(hashed)


__all__ = ["hash_password", "needs_rehash", "verify_password"]
