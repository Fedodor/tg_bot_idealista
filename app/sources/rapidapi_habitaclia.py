"""
RapidAPI Source Adapter for Habitaclia.
Confirmed working via probe script:
- Host: habitaclia.p.rapidapi.com
- Endpoint: /listproperties
- locationId: "listados/alquiler-pisos-barcelona"

Response fields confirmed: Title, Location, Url, MainImage, Price, Rooms, Size, Floor
"""
from __future__ import annotations

import httpx
from typing import Sequence
import re

from app.sources.base import BaseSource
from app.sources.normalized_listing import NormalizedListing
from app.config import settings
from app.logging import get_logger

logger = get_logger(__name__)

# Confirmed working locationIds for /listproperties
LOCATION_IDS = {
    "barcelona": "listados/alquiler-pisos-barcelona",
}


class HabitacliaSource(BaseSource):
    """
    Habitaclia source adapter via RapidAPI.
    Host: habitaclia.p.rapidapi.com
    Endpoint: GET /listproperties
    """

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or settings.rapidapi_key
        self.host = "habitaclia.p.rapidapi.com"

    async def fetch_listings(self, city: str = "barcelona", **kwargs) -> Sequence[NormalizedListing]:
        """Fetches rental listings from Habitaclia RapidAPI."""
        if not self.api_key:
            logger.error("RapidAPI key missing for Habitaclia")
            return []

        location_id = LOCATION_IDS.get(city.lower(), LOCATION_IDS["barcelona"])

        url = f"https://{self.host}/listproperties"
        params = {
            "locationId": location_id,
            "numPage": "1",
            "order": "habitacliascore"
        }

        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.host
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=headers, params=params)
                if response.status_code != 200:
                    logger.warning("Habitaclia API error", status=response.status_code, body=response.text[:200])
                    return []

                data = response.json()
                return self._normalize_response(data, city)
        except Exception as e:
            logger.error("Habitaclia fetch failed", error=str(e))
            return []

    async def health_check(self) -> bool:
        return self.api_key is not None

    def _normalize_response(self, data: list | dict, city: str = "barcelona") -> list[NormalizedListing]:
        """
        Parse Habitaclia /listproperties response.
        The response is a list of objects with: Title, Location, Url, MainImage, Price, Rooms, Size, Floor
        """
        normalized = []

        # Response is a list directly
        items = data if isinstance(data, list) else data.get("data", [])

        for item in items:
            try:
                # Derive a stable external_id from the URL
                url = item.get("Url", "")
                # Extract property ID from URL like ...i2277003488164.htm
                id_match = re.search(r'-i(\d+)\.htm', url)
                property_id = id_match.group(1) if id_match else url[-20:] if url else ""

                if not property_id:
                    continue

                # Parse price — may be string like "1.200 €/mes" or just a number
                raw_price = str(item.get("Price", "0"))
                price_digits = re.sub(r'[^\d]', '', raw_price.split(",")[0].split(".")[0])
                try:
                    price = float(price_digits) if price_digits else 0.0
                    # Handle thousands separator: "1200" from "1.200"
                    if len(price_digits) <= 4 and "." in raw_price:
                        price = float(re.sub(r'[^\d,]', '', raw_price).replace(",", "."))
                except ValueError:
                    price = 0.0

                # Parse size from Size field (may be "85 m²" or just 85)
                raw_size = str(item.get("Size", ""))
                size_match = re.search(r'(\d+)', raw_size)
                area_m2 = float(size_match.group(1)) if size_match else None

                # Parse rooms
                raw_rooms = item.get("Rooms", None)
                try:
                    rooms = int(raw_rooms) if raw_rooms is not None else None
                except (ValueError, TypeError):
                    rooms_match = re.search(r'(\d+)', str(raw_rooms))
                    rooms = int(rooms_match.group(1)) if rooms_match else None

                # Extract district from Location field like "Eixample, Barcelona"
                location_str = item.get("Location", "")
                parts = [p.strip() for p in location_str.split(",")]
                district = parts[0] if len(parts) > 1 else None

                nl = NormalizedListing(
                    external_id=property_id,
                    source="habitaclia",
                    url=url,
                    title=item.get("Title", "Habitaclia Rental"),
                    description=item.get("Description", ""),
                    price=price,
                    rental_type="APARTMENT",
                    city=city.title(),
                    district=district,
                    area_m2=area_m2,
                    rooms=rooms,
                    bathrooms=None,
                    images=[item["MainImage"]] if item.get("MainImage") else [],
                    raw_data=item
                )
                normalized.append(nl)
            except Exception as e:
                logger.warning("Failed to normalize Habitaclia item", error=str(e), item=str(item)[:100])
                continue

        logger.debug("Habitaclia normalized", count=len(normalized))
        return normalized
