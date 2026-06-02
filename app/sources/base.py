"""
Abstract BaseSource interface.

Every source adapter must:
  - extend BaseSource
  - implement fetch() returning list[NormalizedListing]
  - implement health_check() returning bool
  - handle its own errors internally (log + return empty list on failure)
  - never leak source-specific logic outside sources/
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from app.sources.normalized_listing import NormalizedListing


class BaseSource(ABC):
    """Abstract base class for all listing source adapters."""

    source_name: str = "base"

    @abstractmethod
    async def fetch(self) -> list[NormalizedListing]:
        """
        Fetch new listings from this source.

        Must handle all internal errors and return an empty list on failure.
        Never raise exceptions to the caller.
        """
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        """Return True if the source is reachable and healthy."""
        raise NotImplementedError
