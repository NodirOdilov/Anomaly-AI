from __future__ import annotations

import os
from pathlib import Path


def backend_root() -> Path:
    """Directory containing `configs/`, `data/`, `models/`.

    Uses ``BACKEND_ROOT`` when set (e.g. Vercel monorepo root + ``backend/``).
    Otherwise ``cwd`` (Docker/local when started from ``backend/``).
    """
    env = os.getenv("BACKEND_ROOT", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return Path.cwd().resolve()


def resolve_under_root(rel: str, root: Path | None = None) -> Path:
    base = root or backend_root()
    return (base / rel).resolve()
