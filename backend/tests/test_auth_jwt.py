"""Тесты выпуска и валидации JWT-токенов."""

from __future__ import annotations

import time

import pytest

from anomaly_ai.auth.jwt import (
    JwtError,
    create_access_token,
    create_refresh_token,
    decode_token,
)


def test_access_token_round_trip() -> None:
    token = create_access_token(user_id=42, role="analyst", extra={"feature": "x"})
    claims = decode_token(token, expected_type="access")
    assert claims.sub == "42"
    assert claims.role == "analyst"
    assert claims.type == "access"
    assert claims.extra.get("feature") == "x"


def test_refresh_token_round_trip() -> None:
    token, jti, _expires = create_refresh_token(user_id=7, role="viewer")
    claims = decode_token(token, expected_type="refresh")
    assert claims.sub == "7"
    assert claims.role == "viewer"
    assert claims.jti == jti


def test_wrong_token_type_rejected() -> None:
    token = create_access_token(user_id=1, role="viewer")
    with pytest.raises(JwtError):
        decode_token(token, expected_type="refresh")


def test_garbage_token_rejected() -> None:
    with pytest.raises(JwtError):
        decode_token("not.a.valid.jwt", expected_type="access")
