"""
Manual CSV/JSON import source adapter.

Placeholder — implemented in Epic 3.
"""
from __future__ import annotations

from app.sources.base import BaseSource
from app.sources.normalized_listing import NormalizedListing
from app.logging import get_logger

logger = get_logger(__name__)


class ManualImportSource(BaseSource):
    """Imports listings from a local CSV or JSON file."""

    source_name = "manual_import"

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    async def fetch(self) -> list[NormalizedListing]:
        # TODO: implement in Epic 3
        logger.info("ManualImportSource.fetch() — not yet implemented")
        return []

    async def health_check(self) -> bool:
        import os
        return os.path.exists(self.file_path)
