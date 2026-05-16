"""ORM-модели Anomaly AI v2.

Таблицы:

- :class:`User` — учётные записи аналитиков и админов.
- :class:`RefreshToken` — серверные refresh-токены (для отзыва).
- :class:`ApiKey` — машинные API-ключи (хранится только хэш).
- :class:`Prediction` — журнал предсказаний (для аудита и метрик).
- :class:`AuditLog` — журнал всех API-вызовов.
- :class:`Alert` — алерты, генерируемые при детектах.
- :class:`ModelRun` — записи об обучении моделей (для drift-tracking).
- :class:`SiemEndpoint` — настроенные SIEM-вебхуки.
"""

from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from anomaly_ai.db.base import Base, TimestampMixin, utc_now


class UserRole(enum.StrEnum):
    """Роли RBAC."""

    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


class AlertStatus(enum.StrEnum):
    """Жизненный цикл алерта."""

    NEW = "new"
    ACKNOWLEDGED = "acknowledged"
    CLOSED = "closed"
    FALSE_POSITIVE = "false_positive"


class DriftStatus(enum.StrEnum):
    """Статус дрейфа модели."""

    STABLE = "stable"
    WARNING = "warning"
    CRITICAL = "critical"


# === Пользователи и аутентификация ===


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"), nullable=False, default=UserRole.VIEWER,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    api_keys: Mapped[list[ApiKey]] = relationship(back_populates="user", cascade="all, delete-orphan")
    refresh_tokens: Mapped[list[RefreshToken]] = relationship(
        back_populates="user", cascade="all, delete-orphan",
    )


class RefreshToken(Base, TimestampMixin):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    jti: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(512), nullable=True)
    ip: Mapped[str | None] = mapped_column(String(45), nullable=True)

    user: Mapped[User] = relationship(back_populates="refresh_tokens")


class ApiKey(Base, TimestampMixin):
    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    prefix: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    hashed_key: Mapped[str] = mapped_column(String(255), nullable=False)
    scopes: Mapped[str] = mapped_column(String(512), nullable=False, default="predict")
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped[User] = relationship(back_populates="api_keys")

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_api_keys_user_name"),
        Index("ix_api_keys_active", "revoked_at", "expires_at"),
    )


# === Журнал предсказаний и аудит ===


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True,
    )
    module: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    input_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    payload_preview: Mapped[str | None] = mapped_column(String(512), nullable=True)
    prediction: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    severity: Mapped[str | None] = mapped_column(String(32), nullable=True)
    is_attack: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    model_version: Mapped[str | None] = mapped_column(String(32), nullable=True)
    extra_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False, index=True,
    )

    __table_args__ = (
        Index("ix_predictions_module_created", "module", "created_at"),
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True,
    )
    action: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    resource: Mapped[str | None] = mapped_column(String(255), nullable=True)
    method: Mapped[str | None] = mapped_column(String(10), nullable=True)
    path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    status_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ip: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(512), nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    extra_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False, index=True,
    )


# === Алерты ===


class Alert(Base, TimestampMixin):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    severity: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    module: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    summary: Mapped[str] = mapped_column(String(512), nullable=False)
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    prediction_id: Mapped[int | None] = mapped_column(
        ForeignKey("predictions.id", ondelete="SET NULL"), nullable=True,
    )
    status: Mapped[AlertStatus] = mapped_column(
        Enum(AlertStatus, name="alert_status"), nullable=False, default=AlertStatus.NEW, index=True,
    )
    acknowledged_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True,
    )
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)


# === Прогоны моделей и дрейф ===


class ModelRun(Base):
    __tablename__ = "model_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    artifact_path: Mapped[str] = mapped_column(String(512), nullable=False)
    metrics: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    training_samples: Mapped[int | None] = mapped_column(Integer, nullable=True)
    drift_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    drift_status: Mapped[DriftStatus | None] = mapped_column(
        Enum(DriftStatus, name="drift_status"), nullable=True,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False, index=True,
    )

    __table_args__ = (
        UniqueConstraint("model_type", "version", name="uq_model_runs_type_version"),
    )


# === SIEM эндпоинты ===


class SiemEndpoint(Base, TimestampMixin):
    __tablename__ = "siem_endpoints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    url: Mapped[str] = mapped_column(String(1024), nullable=False)
    format: Mapped[str] = mapped_column(String(16), nullable=False, default="json")
    token: Mapped[str | None] = mapped_column(String(512), nullable=True)
    min_confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.85)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    last_success_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)


# === Threat Intelligence ===


class ThreatIntelEntry(Base, TimestampMixin):
    __tablename__ = "threat_intel_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    indicator_type: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    indicator: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(32), nullable=False, default="medium")
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("indicator_type", "indicator", name="uq_threat_intel_type_indicator"),
    )


__all__ = [
    "Alert",
    "AlertStatus",
    "ApiKey",
    "AuditLog",
    "DriftStatus",
    "ModelRun",
    "Prediction",
    "RefreshToken",
    "SiemEndpoint",
    "ThreatIntelEntry",
    "User",
    "UserRole",
]
