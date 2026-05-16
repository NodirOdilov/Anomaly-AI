"""Декларативная база ORM. Все модели наследуют :class:`Base`."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

# Единая convention для имён индексов/constraints (важно для Alembic autogenerate).
NAMING_CONVENTION: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


def utc_now() -> datetime:
    """Текущее UTC-время без микросекунд (для воспроизводимости тестов)."""
    return datetime.now(timezone.utc).replace(microsecond=0)


class Base(DeclarativeBase):
    """Корень иерархии ORM. Содержит общие колонки и удобства."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)

    # Автоматическое имя таблицы из имени класса в snake_case.
    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        return _camel_to_snake(cls.__name__) + "s"

    def to_dict(self) -> dict[str, Any]:
        """Сериализация всех колонок (без relationships) в обычный dict."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TimestampMixin:
    """Колонки ``created_at`` / ``updated_at`` для аудита изменений."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False, index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False,
    )


def _camel_to_snake(name: str) -> str:
    out: list[str] = []
    for i, ch in enumerate(name):
        if i > 0 and ch.isupper() and not name[i - 1].isupper():
            out.append("_")
        out.append(ch.lower())
    return "".join(out)
