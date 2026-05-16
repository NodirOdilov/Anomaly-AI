"""Тесты генерации и проверки API-ключей."""

from __future__ import annotations

from anomaly_ai.auth.api_keys import extract_prefix, generate_api_key, hash_api_key, verify_api_key


def test_generated_key_structure() -> None:
    gen = generate_api_key()
    assert gen.plain.startswith("aa_live_")
    assert len(gen.plain) > 40
    assert gen.prefix.startswith("aa_live_")
    assert gen.hashed == hash_api_key(gen.plain)


def test_verify_correctness() -> None:
    gen = generate_api_key()
    assert verify_api_key(gen.plain, gen.hashed) is True
    assert verify_api_key("aa_live_garbage", gen.hashed) is False


def test_extract_prefix_safe_for_logging() -> None:
    gen = generate_api_key()
    prefix = extract_prefix(gen.plain)
    assert prefix == gen.prefix
    assert gen.plain not in prefix
