"""
Notification worker — delivery layer for matches.

Polls the matches table and triggers Telegram alerts for new matches.
"""
from __future__ import annotations

import asyncio
from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import Match, Notification, User, Listing
from app.db.session import AsyncSessionFactory
from app.services.notifications import send_listing_alert
from app.config import settings
from app.logging import get_logger

logger = get_logger(__name__)


class NotifyWorker:
    """Worker responsible for delivering matches to users."""

    def __init__(self, bot_token: str | None = None) -> None:
        self.bot = Bot(token=bot_token or settings.telegram_bot_token)

    async def run_once(self) -> None:
        """Fetch unsent matches and deliver them."""
        logger.info("Notify cycle started")
        
        async with AsyncSessionFactory() as session:
            # Select matches that should be notified but don't have a notification record yet
            # Task 7.23: Poll matches where should_notify = True and no notification sent
            subquery = select(Notification.match_id)
            stmt = (
                select(Match)
                .where(Match.should_notify == True)
                .where(~Match.id.in_(subquery))
                .options(
                    selectinload(Match.user),
                    selectinload(Match.listing).selectinload(Listing.analysis)
                )
            )
            
            result = await session.execute(stmt)
            pending_matches = result.scalars().all()
            
            if not pending_matches:
                logger.debug("No pending notifications")
                return
            
            logger.info("Found pending matches", count=len(pending_matches))
            
            sent_count = 0
            for match in pending_matches:
                # Task 7.24: Send alerts
                success = await send_listing_alert(
                    bot=self.bot,
                    match=match,
                    listing=match.listing,
                    user=match.user
                )
                if success:
                    sent_count += 1
                
                # Small delay to respect rate limits if many are sent at once
                await asyncio.sleep(0.1)
                
            logger.info("Notify cycle complete", sent=sent_count)

    async def stop(self):
         await self.bot.session.close()
