"""Role-Based Access Control: проверка ролей через FastAPI Depends."""

from __future__ import annotations

from collections.abc import Callable, Iterable

from fastapi import Depends, HTTPException, status

from anomaly_ai.auth.dependencies import AuthPrincipal, get_current_principal
from anomaly_ai.db.models import UserRole

# Иерархия: admin > analyst > viewer.
_ROLE_LEVEL: dict[UserRole, int] = {
    UserRole.VIEWER: 1,
    UserRole.ANALYST: 2,
    UserRole.ADMIN: 3,
}


def _level(role: UserRole | str) -> int:
    if isinstance(role, str):
        role = UserRole(role)
    return _ROLE_LEVEL[role]


def require_role(*allowed: UserRole | str) -> Callable[..., AuthPrincipal]:
    """Создать зависимость, разрешающую только указанные роли (или выше)."""
    allowed_roles: list[UserRole] = [r if isinstance(r, UserRole) else UserRole(r) for r in allowed]
    min_level = min(_level(r) for r in allowed_roles)

    async def _check(principal: AuthPrincipal = Depends(get_current_principal)) -> AuthPrincipal:
        if _level(principal.role) < min_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "Forbidden",
                    "message": f"Требуется одна из ролей: {[r.value for r in allowed_roles]}",
                },
            )
        return principal

    return _check


def require_any(roles: Iterable[UserRole | str]) -> Callable[..., AuthPrincipal]:
    """Вариант с явным итерируемым списком ролей."""
    return require_role(*roles)


# Удобные шорткаты для частых случаев.
require_admin = require_role(UserRole.ADMIN)
require_analyst = require_role(UserRole.ANALYST)
require_viewer = require_role(UserRole.VIEWER)


__all__ = ["require_admin", "require_analyst", "require_any", "require_role", "require_viewer"]
