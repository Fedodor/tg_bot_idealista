"""
Telegram bot application factory.

Registers routers, middlewares, and error handlers.
"""
from __future__ import annotations

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.config import settings
from app.logging import get_logger
from app.bot.handlers_start import router as start_router
from app.bot.handlers_feedback import router as feedback_router

logger = get_logger(__name__)
async def setup_bot_commands(bot: Bot):
    """Register bot commands in the Telegram menu for different languages."""
    en_commands = [
        types.BotCommand(command="start", description="Start or restart onboarding"),
        types.BotCommand(command="help", description="Show help message"),
        types.BotCommand(command="my_search", description="View your active search filters"),
        types.BotCommand(command="delete_me", description="Permanently delete your data"),
    ]
    
    ru_commands = [
        types.BotCommand(command="start", description="Начать заново"),
        types.BotCommand(command="help", description="Показать помощь"),
        types.BotCommand(command="my_search", description="Ваш активный поиск"),
        types.BotCommand(command="delete_me", description="Удалить все мои данные"),
    ]
    
    await bot.set_my_commands(en_commands)  # Default
    await bot.set_my_commands(en_commands, language_code="en")
    await bot.set_my_commands(ru_commands, language_code="ru")
    logger.info("Bot commands registered in Telegram menu (EN/RU)")


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
        await setup_bot_commands(bot)
    
    @dp.shutdown()
    async def on_shutdown():
        logger.info("Bot is shutting down...")
        await bot.session.close()

    logger.info("Telegram bot application built and routers registered")
    return dp


async def start_bot():
    """Entry point for the bot runner."""
    try:
        dp = await build_application()
        bot = Bot(
            token=settings.telegram_bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        
        logger.info("Starting polling...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error("Bot crashed during startup/polling", error=str(e), exc_info=True)
    finally:
        logger.info("Bot execution finished.")
