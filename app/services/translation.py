"""
EN/RU string translation helpers.

Placeholder — implemented in Epic 2.
"""
from __future__ import annotations

_STRINGS: dict[str, dict[str, str]] = {
    "welcome": {
        "en": "Welcome! I help people relocating to Spain find apartments and rooms faster.",
        "ru": "Добро пожаловать! Я помогаю людям, переезжающим в Испанию, быстрее находить квартиры и комнаты.",
    },
}


def t(key: str, language: str = "en") -> str:
    """Return the translated string for the given key and language."""
    entry = _STRINGS.get(key, {})
    return entry.get(language, entry.get("en", key))
