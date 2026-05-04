"""Defensive helpers — sanitization and safety checks (no exploitation)."""

from __future__ import annotations

import re

MAX_PAYLOAD_LEN = 50_000


def truncate_payload(text: str, max_len: int = MAX_PAYLOAD_LEN) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len]


def strip_control_chars(text: str) -> str:
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
