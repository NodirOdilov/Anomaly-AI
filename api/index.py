"""Vercel Python entrypoint — must live under ``api/`` for ``vercel.json`` ``functions`` patterns."""

from __future__ import annotations

import os
import sys
from pathlib import Path

_root = Path(__file__).resolve().parents[1]
_backend = _root / "backend"
os.environ.setdefault("BACKEND_ROOT", str(_backend))
sys.path.insert(0, str(_backend / "src"))

from anomaly_ai.api.main import app  # noqa: E402

__all__ = ["app"]
