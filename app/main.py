"""
Relocation Rental Radar — entry point.

Starts the Telegram bot and background workers.
"""
from __future__ import annotations

import asyncio

from app.logging import setup_logging
from app.config import settings


async def main() -> None:
    setup_logging(settings.log_level)

    # Import here to ensure logging is configured first
    from app.bot.telegram_app import start_bot

    await start_bot()


if __name__ == "__main__":
    asyncio.run(main())
