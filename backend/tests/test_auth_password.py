"""Тесты хэширования паролей Argon2."""

from __future__ import annotations

import pytest

from anomaly_ai.auth.password import hash_password, needs_rehash, verify_password


def test_hash_and_verify_round_trip() -> None:
    plain = "Sup3rSecret!2026"
    hashed = hash_password(plain)
    assert hashed != plain
    assert hashed.startswith("$argon2")
    assert verify_password(plain, hashed) is True
    assert verify_password("wrong", hashed) is False


def test_empty_password_rejected() -> None:
    with pytest.raises(ValueError):
        hash_password("")


def test_needs_rehash_returns_bool() -> None:
    hashed = hash_password("test1234")
    assert isinstance(needs_rehash(hashed), bool)
