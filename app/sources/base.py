"""
Base interface for all rental data sources.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from app.sources.normalized_listing import NormalizedListing

class BaseSource(ABC):
    """
    Abstract base class for source adapters (Idealista, Manual, etc).
    """

    @abstractmethod
    async def fetch_listings(self, **kwargs) -> Sequence[NormalizedListing]:
        """
        Fetches and returns a list of standardized listings.
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Returns True if the source (API/Scraper) is available.
        """
        pass
