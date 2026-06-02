"""
User-submitted listing URL source adapter.

Placeholder — implemented in Epic 3.
"""
from __future__ import annotations

from app.sources.base import BaseSource
from app.sources.normalized_listing import NormalizedListing
from app.logging import get_logger

logger = get_logger(__name__)


class UserSubmittedSource(BaseSource):
    """Accepts listing URLs submitted by users via the bot."""

    source_name = "user_submitted"

    async def fetch(self) -> list[NormalizedListing]:
        # TODO: implement in Epic 3
        logger.info("UserSubmittedSource.fetch() — not yet implemented")
        return []

    async def health_check(self) -> bool:
        return True
