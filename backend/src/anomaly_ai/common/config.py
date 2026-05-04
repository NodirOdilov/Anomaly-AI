from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from anomaly_ai.common.paths import backend_root, resolve_under_root
from anomaly_ai.version import __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = Field(default="development", alias="APP_ENV")
    app_name: str = Field(default="Anomaly AI", alias="APP_NAME")
    app_version: str = Field(default=__version__, alias="APP_VERSION")
    model_dir: str = Field(default="models", alias="MODEL_DIR")
    data_dir: str = Field(default="data", alias="DATA_DIR")


@lru_cache
def get_settings() -> Settings:
    return Settings()


def load_yaml_config(rel_path: str) -> dict[str, Any]:
    path = resolve_under_root(rel_path)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def merged_app_config() -> dict[str, Any]:
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
    return data
