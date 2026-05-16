"""Эндпоинты аутентификации."""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from anomaly_ai.auth.api_keys import generate_api_key
from anomaly_ai.auth.dependencies import AuthPrincipal, get_current_principal
from anomaly_ai.auth.rbac import require_admin
from anomaly_ai.auth.service import (
    AuthError,
    authenticate,
    issue_token_pair,
    refresh_access_token,
    register_user,
    revoke_refresh_token,
)
from anomaly_ai.db.models import ApiKey, User, UserRole
from anomaly_ai.db.session import get_session
from anomaly_ai.observability.metrics import auth_logins_total
from anomaly_ai.schemas.auth import (
    AccessTokenResponse,
    ApiKeyCreated,
    ApiKeyCreateRequest,
    ApiKeyPublic,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenPair,
    UserPublic,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def _client_info(request: Request) -> tuple[str | None, str | None]:
    ua = request.headers.get("user-agent")
    ip = request.client.host if request.client else None
    return ua, ip


@router.post("/login", response_model=TokenPair)
async def login(
    body: LoginRequest,
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> TokenPair:
    """Login по email+паролю. Возвращает пару access+refresh."""
    try:
        user = await authenticate(session, email=body.email, password=body.password)
    except AuthError as exc:
        auth_logins_total.labels(result="failure").inc()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "AuthError", "message": exc.message},
        ) from exc

    user_agent, ip = _client_info(request)
    access, refresh, access_ttl, refresh_ttl = await issue_token_pair(
        session, user=user, user_agent=user_agent, ip=ip,
    )
    auth_logins_total.labels(result="success").inc()
    return TokenPair(
        access_token=access,
        refresh_token=refresh,
        access_expires_in=access_ttl,
        refresh_expires_in=refresh_ttl,
    )


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
async def register(
    body: RegisterRequest,
    session: AsyncSession = Depends(get_session),
) -> UserPublic:
    """Регистрация нового пользователя. Только admin."""
    try:
        user = await register_user(
            session,
            email=body.email,
            password=body.password,
            full_name=body.full_name,
        )
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "AuthError", "message": exc.message},
        ) from exc

    return UserPublic.model_validate(user, from_attributes=True)


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(
    body: RefreshRequest,
    session: AsyncSession = Depends(get_session),
) -> AccessTokenResponse:
    """Обновить access-токен по валидному refresh."""
    try:
        access, ttl = await refresh_access_token(session, refresh_token_raw=body.refresh_token)
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "AuthError", "message": exc.message},
        ) from exc
    return AccessTokenResponse(access_token=access, expires_in=ttl)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    body: RefreshRequest,
    session: AsyncSession = Depends(get_session),
) -> None:
    """Отозвать refresh-токен."""
    from anomaly_ai.auth.jwt import JwtError, decode_token

    try:
        claims = decode_token(body.refresh_token, expected_type="refresh")
    except JwtError:
        return
    await revoke_refresh_token(session, jti=claims.jti)


@router.get("/me", response_model=UserPublic)
async def me(
    principal: AuthPrincipal = Depends(get_current_principal),
    session: AsyncSession = Depends(get_session),
) -> UserPublic:
    """Информация о текущем пользователе."""
    user = await session.get(User, principal.user_id)
    if user is None:
        # Анонимный режим (auth_required=false)
        return UserPublic(
            id=0,
            email=principal.email,
            full_name=None,
            role=principal.role.value if isinstance(principal.role, UserRole) else str(principal.role),
            is_active=True,
            created_at=datetime.now(UTC),
        )
    return UserPublic.model_validate(user, from_attributes=True)


# === API-ключи ===


@router.get("/api-keys", response_model=list[ApiKeyPublic])
async def list_api_keys(
    principal: AuthPrincipal = Depends(get_current_principal),
    session: AsyncSession = Depends(get_session),
) -> list[ApiKeyPublic]:
    """Список ключей текущего пользователя."""
    stmt = select(ApiKey).where(ApiKey.user_id == principal.user_id).order_by(ApiKey.created_at.desc())
    rows = (await session.execute(stmt)).scalars().all()
    return [ApiKeyPublic.model_validate(r, from_attributes=True) for r in rows]


@router.post("/api-keys", response_model=ApiKeyCreated, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    body: ApiKeyCreateRequest,
    principal: AuthPrincipal = Depends(get_current_principal),
    session: AsyncSession = Depends(get_session),
) -> ApiKeyCreated:
    """Создать новый API-ключ. ``plain`` значение возвращается ОДИН раз."""
    generated = generate_api_key()
    row = ApiKey(
        user_id=principal.user_id,
        name=body.name,
        prefix=generated.prefix,
        hashed_key=generated.hashed,
        scopes=body.scopes,
        expires_at=body.expires_at,
    )
    session.add(row)
    await session.flush()
    return ApiKeyCreated(
        id=row.id,
        name=row.name,
        prefix=row.prefix,
        scopes=row.scopes,
        created_at=row.created_at,
        expires_at=row.expires_at,
        revoked_at=row.revoked_at,
        last_used_at=row.last_used_at,
        plain=generated.plain,
    )


@router.delete("/api-keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_key(
    key_id: int,
    principal: AuthPrincipal = Depends(get_current_principal),
    session: AsyncSession = Depends(get_session),
) -> None:
    """Отозвать ключ (мягкое удаление)."""
    row = await session.get(ApiKey, key_id)
    if row is None or row.user_id != principal.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "NotFound", "message": "API-ключ не найден"},
        )
    row.revoked_at = datetime.now(UTC)
