"""Расширенная конфигурация приложения Anomaly AI v2.

Загружает настройки из переменных окружения и/или ``.env`` файла. Поддерживает
профили: ``development`` | ``staging`` | ``production`` | ``test``.

Все секреты должны задаваться через переменные окружения. Дефолты подходят
исключительно для локальной разработки и автоматических тестов.
"""

from __future__ import annotations

import secrets
from functools import lru_cache
from typing import Any, Literal

import yaml
from pydantic import Field, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from anomaly_ai.common.paths import backend_root, resolve_under_root
from anomaly_ai.version import __version__

AppEnv = Literal["development", "staging", "production", "test"]


class Settings(BaseSettings):
    """Главный объект настроек. Доступ через :func:`get_settings`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # === Профиль и метаданные ===
    app_env: AppEnv = Field(default="development", alias="APP_ENV")
    app_name: str = Field(default="Anomaly AI", alias="APP_NAME")
    app_version: str = Field(default=__version__, alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")

    # === Пути ===
    model_dir: str = Field(default="models", alias="MODEL_DIR")
    data_dir: str = Field(default="data", alias="DATA_DIR")
    reports_dir: str = Field(default="reports", alias="REPORTS_DIR")

    # === База данных ===
    # По умолчанию — SQLite в backend/data/anomaly_ai.db (для dev и тестов).
    database_url: str = Field(
        default="sqlite+aiosqlite:///./data/anomaly_ai.db",
        alias="DATABASE_URL",
    )
    database_echo: bool = Field(default=False, alias="DATABASE_ECHO")
    database_pool_size: int = Field(default=5, alias="DATABASE_POOL_SIZE")

    # === Redis (кэш + rate-limit storage) ===
    redis_url: str | None = Field(default=None, alias="REDIS_URL")
    cache_ttl_seconds: int = Field(default=300, alias="CACHE_TTL_SECONDS")

    # === Аутентификация ===
    # auth_required=false в dev сохраняет совместимость с демо-режимом фронта.
    auth_required: bool = Field(default=False, alias="AUTH_REQUIRED")
    jwt_secret: str = Field(
        default_factory=lambda: secrets.token_urlsafe(64),
        alias="JWT_SECRET",
    )
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_access_ttl_minutes: int = Field(default=15, alias="JWT_ACCESS_TTL_MINUTES")
    jwt_refresh_ttl_days: int = Field(default=7, alias="JWT_REFRESH_TTL_DAYS")
    api_key_prefix: str = Field(default="aa_live", alias="API_KEY_PREFIX")

    # Первый администратор создаётся автоматически при старте, если БД пуста.
    bootstrap_admin_email: str = Field(default="admin@anomaly.local", alias="BOOTSTRAP_ADMIN_EMAIL")
    bootstrap_admin_password: str = Field(
        default="ChangeMe!2026",
        alias="BOOTSTRAP_ADMIN_PASSWORD",
    )

    # === CORS ===
    cors_origins: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173,http://localhost:5174,http://127.0.0.1:5174",
        alias="CORS_ORIGINS",
    )

    # === Rate limiting ===
    rate_limit_default: str = Field(default="100/minute", alias="RATE_LIMIT_DEFAULT")
    rate_limit_auth: str = Field(default="10/minute", alias="RATE_LIMIT_AUTH")
    rate_limit_predict: str = Field(default="60/minute", alias="RATE_LIMIT_PREDICT")

    # === Наблюдаемость ===
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_json: bool = Field(default=False, alias="LOG_JSON")
    metrics_enabled: bool = Field(default=True, alias="METRICS_ENABLED")
    sentry_dsn: str | None = Field(default=None, alias="SENTRY_DSN")

    # === SIEM-вебхуки ===
    siem_webhook_url: str | None = Field(default=None, alias="SIEM_WEBHOOK_URL")
    siem_webhook_format: Literal["json", "cef"] = Field(default="json", alias="SIEM_WEBHOOK_FORMAT")
    siem_webhook_token: str | None = Field(default=None, alias="SIEM_WEBHOOK_TOKEN")
    siem_min_confidence: float = Field(default=0.85, alias="SIEM_MIN_CONFIDENCE")

    # === ML ===
    ml_drift_warning_threshold: float = Field(default=0.10, alias="ML_DRIFT_WARNING_THRESHOLD")
    ml_drift_critical_threshold: float = Field(default=0.25, alias="ML_DRIFT_CRITICAL_THRESHOLD")
    ml_explain_top_features: int = Field(default=10, alias="ML_EXPLAIN_TOP_FEATURES")

    # === Валидаторы ===

    @field_validator("jwt_algorithm")
    @classmethod
    def _validate_jwt_algo(cls, v: str) -> str:
        if v not in {"HS256", "HS384", "HS512", "RS256"}:
            raise ValueError(f"Неподдерживаемый JWT алгоритм: {v}")
        return v

    @field_validator("ml_drift_warning_threshold", "ml_drift_critical_threshold")
    @classmethod
    def _validate_threshold(cls, v: float) -> float:
        if not 0.0 <= v <= 1.0:
            raise ValueError("Порог дрейфа должен быть в диапазоне [0, 1]")
        return v

    # === Производные ===

    @computed_field  # type: ignore[prop-decorator]
    @property
    def cors_origins_list(self) -> list[str]:
        """CORS-разрешения как список (парсинг из строки)."""
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_test(self) -> bool:
        return self.app_env == "test"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_serverless(self) -> bool:
        """На Vercel/Lambda некоторые подсистемы отключаются."""
        import os
        on_vercel = os.getenv("VERCEL", "").lower() in {"1", "true"}
        on_lambda = os.getenv("AWS_LAMBDA_FUNCTION_NAME") is not None
        return on_vercel or on_lambda


@lru_cache
def get_settings() -> Settings:
    """Кэшированный аксессор. Сбрасывайте через ``get_settings.cache_clear()`` в тестах."""
    return Settings()


# === YAML-конфигурации (для треининга и app.yaml) ===


def load_yaml_config(rel_path: str) -> dict[str, Any]:
    """Загрузить YAML относительно ``backend_root()``."""
    path = resolve_under_root(rel_path)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def merged_app_config() -> dict[str, Any]:
    """Слить ``configs/app.yaml`` с настройками окружения."""
    root = backend_root()
    cfg_path = root / "configs" / "app.yaml"
    data: dict[str, Any] = {}
    if cfg_path.exists():
        with cfg_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    settings = get_settings()
    data.setdefault("app", {})
    data["app"]["name"] = settings.app_name
    data["app"]["env"] = settings.app_env
    data["app"]["version"] = settings.app_version
    data.setdefault("paths", {})
    data["paths"]["model_dir"] = str(resolve_under_root(settings.model_dir, root))
    data["paths"]["data_dir"] = str(resolve_under_root(settings.data_dir, root))
    data["paths"]["reports_dir"] = str(resolve_under_root(settings.reports_dir, root))
    return data


__all__ = ["AppEnv", "Settings", "get_settings", "load_yaml_config", "merged_app_config"]
