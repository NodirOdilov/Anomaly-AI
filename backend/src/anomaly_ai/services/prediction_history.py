from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from threading import Lock


@dataclass
class HistoryItem:
    module: str
    summary: str


class PredictionHistory:
    def __init__(self, maxlen: int = 50) -> None:
        self._items: deque[HistoryItem] = deque(maxlen=maxlen)
        self._lock = Lock()

    def add(self, module: str, summary: str) -> None:
        with self._lock:
            self._items.appendleft(HistoryItem(module=module, summary=summary))

    def recent(self, limit: int = 10) -> list[HistoryItem]:
        with self._lock:
            return list(self._items)[:limit]


prediction_history = PredictionHistory()
