"""
Inline keyboards for the Telegram bot.

Defined centraly to keep handlers clean.
"""
from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for initial language selection."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang_en"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru"),
    )
    return builder.as_markup()


def get_rental_type_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting rental type (Apartment/Room/Both)."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Apartment", callback_data="type_apartment"),
        InlineKeyboardButton(text="Room", callback_data="type_room"),
    )
    builder.row(
        InlineKeyboardButton(text="Both", callback_data="type_both")
    )
    return builder.as_markup()
