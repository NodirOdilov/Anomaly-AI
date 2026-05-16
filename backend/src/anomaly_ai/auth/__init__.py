"""Аутентификация и авторизация Anomaly AI v2.

Подмодули:

- :mod:`anomaly_ai.auth.password` — argon2 хэширование паролей.
- :mod:`anomaly_ai.auth.jwt` — выпуск и валидация JWT.
- :mod:`anomaly_ai.auth.api_keys` — генерация и проверка API-ключей.
- :mod:`anomaly_ai.auth.dependencies` — FastAPI зависимости (Bearer + X-API-Key).
- :mod:`anomaly_ai.auth.rbac` — декоратор/зависимость для проверки ролей.
- :mod:`anomaly_ai.auth.service` — высокоуровневые операции (login, register, refresh).
"""

from anomaly_ai.auth.api_keys import generate_api_key, hash_api_key, verify_api_key
from anomaly_ai.auth.dependencies import (
    AuthPrincipal,
    get_current_principal,
    get_optional_principal,
)
from anomaly_ai.auth.jwt import (
    JwtClaims,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from anomaly_ai.auth.password import hash_password, verify_password
from anomaly_ai.auth.rbac import require_role

__all__ = [
    "AuthPrincipal",
    "JwtClaims",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "generate_api_key",
    "get_current_principal",
    "get_optional_principal",
    "hash_api_key",
    "hash_password",
    "require_role",
    "verify_api_key",
    "verify_password",
]
