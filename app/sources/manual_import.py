"""
Manual CSV/JSON import source adapter.

Reads rental listings from local files and converts them 
into NormalizedListing objects. 
"""
from __future__ import annotations

import csv
import json
import os
from typing import Any

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
        """Reads file and returns a list of NormalizedListings."""
        if not os.path.exists(self.file_path):
            logger.error("Import file not found", path=self.file_path)
            return []

        ext = os.path.splitext(self.file_path)[1].lower()
        
        try:
            if ext == ".json":
                return self._parse_json()
            elif ext == ".csv":
                return self._parse_csv()
            else:
                logger.error("Unsupported file format", ext=ext)
                return []
        except Exception as e:
            logger.error("Failed to parse import file", error=str(e))
            return []

    def _parse_json(self) -> list[NormalizedListing]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            logger.error("JSON import must be a list of objects")
            return []
            
        listings = []
        for item in data:
            try:
                listings.append(NormalizedListing(source=self.source_name, **item))
            except Exception as e:
                logger.warning("Skipping invalid JSON item", item=item, error=str(e))
        return listings

    def _parse_csv(self) -> list[NormalizedListing]:
        listings = []
        with open(self.file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Clean up empty strings to None
                    clean_row = {k: (v if v != "" else None) for k, v in row.items()}
                    
                    # Convert types where necessary
                    if clean_row.get("price"):
                        clean_row["price"] = float(clean_row["price"])
                    if clean_row.get("area_m2"):
                        clean_row["area_m2"] = float(clean_row["area_m2"])
                    if clean_row.get("rooms"):
                        clean_row["rooms"] = int(clean_row["rooms"])
                    
                    listings.append(NormalizedListing(source=self.source_name, **clean_row))
                except Exception as e:
                    logger.warning("Skipping invalid CSV row", row=row, error=str(e))
        return listings

    async def health_check(self) -> bool:
        return os.path.exists(self.file_path)
