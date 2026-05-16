"""Схемы для админских эндпоинтов (users, audit, alerts)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int
    pages: int


class UserUpdateRequest(BaseModel):
    full_name: str | None = None
    role: str | None = None
    is_active: bool | None = None


class AuditLogPublic(BaseModel):
    id: int
    user_id: int | None
    action: str
    method: str | None
    path: str | None
    status_code: int | None
    ip: str | None
    request_id: str | None
    created_at: datetime


class AuditLogPage(BaseModel):
    items: list[AuditLogPublic]
    meta: PaginationMeta


class AlertPublic(BaseModel):
    id: int
    severity: str
    module: str
    summary: str
    status: str
    payload: dict[str, Any] | None
    created_at: datetime
    acknowledged_at: datetime | None


class AlertAckRequest(BaseModel):
    status: str = Field(pattern="^(acknowledged|closed|false_positive)$")
    notes: str | None = None
