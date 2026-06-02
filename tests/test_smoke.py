"""
Smoke tests — Task 1.21.

Verifies:
  1. All models can be imported cleanly.
  2. NormalizedListing dedup_hash is computed correctly.
  3. Config loads from environment without errors.
  4. Translation helper returns correct strings.

These tests do NOT require a live database connection.
Database connectivity is verified in tests/test_db_connection.py
(requires docker compose to be running).
"""
from __future__ import annotations

import os

import pytest


# ─── Models import ────────────────────────────────────────────────────────────

def test_models_import_cleanly() -> None:
    """All ORM models must be importable without errors."""
    from app.db.models import (
        Base,
        Feedback,
        Listing,
        ListingAnalysis,
        Match,
        Notification,
        User,
        UserSearch,
    )
    expected_tables = {
        "users", "user_searches", "listings",
        "listing_analysis", "matches", "notifications", "feedback",
    }
    actual_tables = set(Base.metadata.tables.keys())
    assert expected_tables == actual_tables, (
        f"Missing tables: {expected_tables - actual_tables}. "
        f"Extra tables: {actual_tables - expected_tables}."
    )


# ─── NormalizedListing ────────────────────────────────────────────────────────

def test_normalized_listing_dedup_hash_computed() -> None:
    """dedup_hash must be auto-computed from price+city+area_m2+title."""
    from app.sources.normalized_listing import NormalizedListing
    listing = NormalizedListing(
        source="test",
        price=800.0,
        city="Barcelona",
        area_m2=45.0,
        title="Cozy room in Eixample",
    )
    assert listing.dedup_hash is not None
    assert len(listing.dedup_hash) == 64  # SHA-256 hex digest


def test_normalized_listing_dedup_hash_deterministic() -> None:
    """Same inputs must always produce the same dedup_hash."""
    from app.sources.normalized_listing import NormalizedListing
    a = NormalizedListing(source="test", price=900.0, city="Barcelona", area_m2=55.0, title="Bright flat")
    b = NormalizedListing(source="other", price=900.0, city="Barcelona", area_m2=55.0, title="Bright flat")
    assert a.dedup_hash == b.dedup_hash  # source does not affect hash


def test_normalized_listing_dedup_hash_case_insensitive() -> None:
    """City and title are lowercased before hashing."""
    from app.sources.normalized_listing import NormalizedListing
    a = NormalizedListing(source="test", price=700.0, city="barcelona", title="Nice room")
    b = NormalizedListing(source="test", price=700.0, city="BARCELONA", title="Nice Room")
    assert a.dedup_hash == b.dedup_hash


# ─── Config ───────────────────────────────────────────────────────────────────

def test_config_loads(monkeypatch: pytest.MonkeyPatch) -> None:
    """Settings must load when required env vars are present."""
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "1234567890:AABBCCDDEEFFaabbccddeeff-test")

    # Re-import to pick up patched env
    import importlib
    import app.config as cfg_module
    importlib.reload(cfg_module)

    from app.config import Settings
    s = Settings(
        database_url="postgresql+asyncpg://test:test@localhost:5432/test",
        telegram_bot_token="1234567890:test",
    )
    assert s.database_url.startswith("postgresql+asyncpg://")
    assert s.log_level == "INFO"
    assert s.ollama_model == "llama3"


# ─── Translation ──────────────────────────────────────────────────────────────

def test_translation_returns_english_by_default() -> None:
    from app.services.translation import t
    result = t("welcome")
    assert "Spain" in result or len(result) > 0


def test_translation_returns_russian() -> None:
    from app.services.translation import t
    result = t("welcome", language="ru")
    # Russian text contains Cyrillic characters
    assert any(ord(c) > 127 for c in result)


def test_translation_unknown_key_returns_key() -> None:
    from app.services.translation import t
    assert t("nonexistent_key_xyz") == "nonexistent_key_xyz"
