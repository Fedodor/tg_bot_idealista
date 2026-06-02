"""
Telegram bot application factory.

Registers routers, middlewares, and error handlers.
"""
from __future__ import annotations

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import settings
from app.logging import get_logger
from app.bot.handlers_start import router as start_router
from app.bot.handlers_feedback import router as feedback_router

logger = get_logger(__name__)


async def build_application() -> Dispatcher:
    """Build and return the configured aiogram Dispatcher and Bot."""
    bot = Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    
    # Using memory storage for MVP; move to Redis later as planned
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register routers
    dp.include_router(start_router)
    dp.include_router(feedback_router)
    
    # Startup/Shutdown events
    @dp.startup()
    async def on_startup():
        logger.info("Bot is starting up...")
        # setup_db_checks() or similar could go here
    
    @dp.shutdown()
    async def on_shutdown():
        logger.info("Bot is shutting down...")
        await bot.session.close()

    logger.info("Telegram bot application built and routers registered")
    return dp


async def start_bot():
    """Entry point for the bot runner."""
    dp = await build_application()
    bot = Bot(token=settings.telegram_bot_token)
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
