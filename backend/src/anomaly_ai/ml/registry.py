"""Реестр моделей с версионированием и hot-swap.

Структура каталога::

    models/
    ├── waf_payload/
    │   ├── 1.0.0/
    │   │   ├── artifact.joblib
    │   │   └── metadata.json
    │   ├── 1.1.0/
    │   │   ├── artifact.joblib
    │   │   └── metadata.json
    │   └── ACTIVE -> 1.1.0      # текстовый файл с активной версией
    └── network_anomaly/
        └── ...

При промоушене новой версии файл ``ACTIVE`` обновляется, кэш сбрасывается,
следующее обращение к сервису загружает новую модель.
"""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from anomaly_ai.common.config import get_settings
from anomaly_ai.common.paths import backend_root, resolve_under_root

ACTIVE_FILE = "ACTIVE"
ARTIFACT_NAME = "artifact.joblib"
METADATA_NAME = "metadata.json"


@dataclass(frozen=True)
class RegistryEntry:
    """Описание одной версии модели."""

    module: str
    version: str
    artifact_path: Path
    metadata: dict[str, Any]
    is_active: bool = False

    @property
    def created_at(self) -> str | None:
        return self.metadata.get("created_at")

    @property
    def metrics(self) -> dict[str, Any]:
        return self.metadata.get("metrics") or {}


class ModelRegistry:
    """Файловый реестр моделей. Потокобезопасен на уровне переключения активной версии."""

    def __init__(self, root: Path | str | None = None) -> None:
        if root is None:
            settings = get_settings()
            root = resolve_under_root(settings.model_dir, backend_root())
        self._root = Path(root)
        self._lock = threading.RLock()

    @property
    def root(self) -> Path:
        return self._root

    # === Чтение ===

    def list_modules(self) -> list[str]:
        if not self._root.exists():
            return []
        return sorted([p.name for p in self._root.iterdir() if p.is_dir()])

    def list_versions(self, module: str) -> list[RegistryEntry]:
        module_dir = self._root / module
        if not module_dir.exists():
            return []
        active = self._read_active(module)
        entries: list[RegistryEntry] = []
        for version_dir in sorted(p for p in module_dir.iterdir() if p.is_dir()):
            metadata = self._read_metadata(version_dir)
            entries.append(
                RegistryEntry(
                    module=module,
                    version=version_dir.name,
                    artifact_path=version_dir / ARTIFACT_NAME,
                    metadata=metadata,
                    is_active=(version_dir.name == active),
                ),
            )
        return entries

    def get_active(self, module: str) -> RegistryEntry | None:
        active = self._read_active(module)
        if active is None:
            # Fallback: попробовать legacy-путь backend/models/<module>_model.joblib
            legacy = self._root / f"{module}_model.joblib"
            if legacy.exists():
                return RegistryEntry(
                    module=module,
                    version="legacy",
                    artifact_path=legacy,
                    metadata={"legacy": True},
                    is_active=True,
                )
            return None
        version_dir = self._root / module / active
        return RegistryEntry(
            module=module,
            version=active,
            artifact_path=version_dir / ARTIFACT_NAME,
            metadata=self._read_metadata(version_dir),
            is_active=True,
        )

    # === Запись ===

    def register(
        self,
        module: str,
        version: str,
        *,
        artifact_bytes: bytes | None = None,
        metadata: dict[str, Any] | None = None,
        activate: bool = False,
    ) -> RegistryEntry:
        """Зарегистрировать новую версию. Если ``activate=True`` — сделать активной."""
        with self._lock:
            version_dir = self._root / module / version
            version_dir.mkdir(parents=True, exist_ok=True)
            if artifact_bytes is not None:
                (version_dir / ARTIFACT_NAME).write_bytes(artifact_bytes)
            meta = dict(metadata or {})
            meta.setdefault("registered_at", datetime.now(UTC).isoformat())
            (version_dir / METADATA_NAME).write_text(
                json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8",
            )
            if activate:
                self.activate(module, version)
            return RegistryEntry(
                module=module,
                version=version,
                artifact_path=version_dir / ARTIFACT_NAME,
                metadata=meta,
                is_active=activate,
            )

    def activate(self, module: str, version: str) -> None:
        """Сделать указанную версию активной (atomically)."""
        with self._lock:
            version_dir = self._root / module / version
            if not version_dir.exists():
                raise FileNotFoundError(f"Версия не найдена: {module}/{version}")
            active_file = self._root / module / ACTIVE_FILE
            active_file.write_text(version, encoding="utf-8")

    # === Внутреннее ===

    def _read_active(self, module: str) -> str | None:
        path = self._root / module / ACTIVE_FILE
        if not path.exists():
            return None
        try:
            return path.read_text(encoding="utf-8").strip() or None
        except OSError:
            return None

    @staticmethod
    def _read_metadata(version_dir: Path) -> dict[str, Any]:
        path = version_dir / METADATA_NAME
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}


# === Глобальный синглтон ===

_default_registry: ModelRegistry | None = None
_default_lock = threading.Lock()


def get_default_registry() -> ModelRegistry:
    """Получить общий реестр приложения."""
    global _default_registry
    if _default_registry is None:
        with _default_lock:
            if _default_registry is None:
                _default_registry = ModelRegistry()
    return _default_registry


def reset_default_registry() -> None:
    """Сбросить (для тестов)."""
    global _default_registry
    _default_registry = None


__all__ = [
    "ACTIVE_FILE",
    "ARTIFACT_NAME",
    "METADATA_NAME",
    "ModelRegistry",
    "RegistryEntry",
    "get_default_registry",
    "reset_default_registry",
]
