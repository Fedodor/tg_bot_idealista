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
    from app.workers.orchestrator import Orchestrator

    orchestrator = Orchestrator(interval_seconds=settings.refresh_interval_seconds)
    
    # Run both the bot and the background work forever
    await asyncio.gather(
        start_bot(),
        orchestrator.start()
    )


if __name__ == "__main__":
    asyncio.run(main())
