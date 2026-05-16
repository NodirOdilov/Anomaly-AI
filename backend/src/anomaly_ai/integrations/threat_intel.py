"""Локальная база Threat Intelligence (репутация IP, доменов, хэшей).

В простом случае хранится в SQLite/Postgres (таблица ``threat_intel_entries``).
Импорт из CSV/JSON, lookup за O(1) через индекс ``(indicator_type, indicator)``.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from anomaly_ai.db.models import ThreatIntelEntry


@dataclass(frozen=True)
class ThreatVerdict:
    """Результат проверки индикатора."""

    indicator: str
    indicator_type: str
    matched: bool
    severity: str | None = None
    source: str | None = None
    description: str | None = None


class ThreatIntelService:
    """CRUD + lookup для индикаторов угроз."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def lookup(self, *, indicator: str, indicator_type: str) -> ThreatVerdict:
        """Проверить один индикатор."""
        now = datetime.now(timezone.utc)
        stmt = select(ThreatIntelEntry).where(
            ThreatIntelEntry.indicator == indicator,
            ThreatIntelEntry.indicator_type == indicator_type,
        )
        entry = (await self.session.execute(stmt)).scalar_one_or_none()
        if entry is None:
            return ThreatVerdict(indicator=indicator, indicator_type=indicator_type, matched=False)
        if entry.expires_at is not None and entry.expires_at < now:
            return ThreatVerdict(indicator=indicator, indicator_type=indicator_type, matched=False)
        return ThreatVerdict(
            indicator=indicator,
            indicator_type=indicator_type,
            matched=True,
            severity=entry.severity,
            source=entry.source,
            description=entry.description,
        )

    async def bulk_upsert(self, entries: Iterable[dict]) -> int:
        """Идемпотентная массовая загрузка. Возвращает число обработанных."""
        count = 0
        for raw in entries:
            indicator = raw.get("indicator")
            indicator_type = raw.get("indicator_type")
            if not indicator or not indicator_type:
                continue
            stmt = select(ThreatIntelEntry).where(
                ThreatIntelEntry.indicator == indicator,
                ThreatIntelEntry.indicator_type == indicator_type,
            )
            existing = (await self.session.execute(stmt)).scalar_one_or_none()
            if existing is None:
                self.session.add(
                    ThreatIntelEntry(
                        indicator=indicator,
                        indicator_type=indicator_type,
                        severity=raw.get("severity") or "medium",
                        source=raw.get("source"),
                        description=raw.get("description"),
                    ),
                )
            else:
                existing.severity = raw.get("severity") or existing.severity
                existing.source = raw.get("source") or existing.source
                existing.description = raw.get("description") or existing.description
            count += 1
        return count

    async def import_csv(self, csv_text: str) -> int:
        """Импорт CSV с колонками: ``indicator_type,indicator,severity,source,description``."""
        reader = csv.DictReader(io.StringIO(csv_text))
        return await self.bulk_upsert(list(reader))


__all__ = ["ThreatIntelService", "ThreatVerdict"]
