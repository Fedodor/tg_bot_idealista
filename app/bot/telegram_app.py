"""
Telegram bot application factory.

Placeholder — implemented in Epic 2.
"""
from __future__ import annotations

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import settings
from app.logging import get_logger

logger = get_logger(__name__)


async def build_application() -> Bot:
    """Build and return the configured aiogram Bot instance."""
    bot = Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    logger.info("Telegram bot application built", bot_token_prefix=settings.telegram_bot_token[:10])
    return bot
