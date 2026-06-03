"""
RapidAPI Source Adapter for Idealista.
RE-MAPPED BASED ON BROWSER RESEARCH: 
Endpoint: /v1/search
Location Code for Barcelona: [0-EU-ES-08]
"""
from __future__ import annotations

import httpx
from typing import Sequence
import json

from app.sources.base import BaseSource
from app.sources.normalized_listing import NormalizedListing
from app.config import settings
from app.logging import get_logger

logger = get_logger(__name__)

# Mapping our internal city names to RapidAPI location IDs
# 0-EU-ES-08 is Barcelona city
LOCATION_MAPPING = {
    "barcelona": "0-EU-ES-08"
}

class RapidAPISource(BaseSource):
    """
    Implementation of BaseSource using RapidAPI's Idealista Scraper (kiwimaker/v1 style).
    """

    def __init__(self, api_key: str | None = None, host: str | None = None) -> None:
        self.api_key = api_key or settings.rapidapi_key
        self.host = host or settings.rapidapi_host
        self.base_url = f"https://{self.host}"

    async def fetch_listings(self, city: str = "barcelona", **kwargs) -> Sequence[NormalizedListing]:
        """
        Fetches listings from RapidAPI.
        Supported kwargs:
        - since: 'W' (week), 'D' (day), 'M' (month)
        - max_items: int (default 40)
        """
        if not settings.rapidapi_key:
            logger.error("RapidAPI key missing")
            return []

        url = f"https://{settings.rapidapi_host}/v1/search"
        
        # Mapping our internal city names to RapidAPI location IDs
        location_id = LOCATION_MAPPING.get(city.lower(), "0-EU-ES-08")
        
        params = {
            "locationIds": f"[{location_id}]",
            "operation": "rent",
            "propertyType": "homes",
            "locale": "es",
            "country": "es",
            "maxItems": str(kwargs.get("max_items", 40)),
            "numPage": "1"
        }

        # Handle historical data
        since = kwargs.get("since")
        if since:
            params["minPublicationDate"] = since

        headers = {
            "x-rapidapi-key": settings.rapidapi_key,
            "x-rapidapi-host": settings.rapidapi_host
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.get(url, headers=headers, params=params)
                
                if response.status_code != 200:
                    logger.error("RapidAPI returned error", status=response.status_code, body=response.text)
                    response.raise_for_status()

                data = response.json()
                return self._normalize_response(data)

        except Exception as e:
            logger.error("RapidAPI fetch failed", error=str(e))
            return []

    async def health_check(self) -> bool:
        return self.api_key is not None

    def _normalize_response(self, data: dict) -> list[NormalizedListing]:
        """
        Parses JSON from /v1/search.
        Expected structure: data['elementList'] or data['data']['elementList']
        """
        normalized = []
        
        # The /v1 structure usually nests elements in 'data'
        payload = data.get("data", data)
        items = payload.get("elementList", [])

        for item in items:
            try:
                property_id = str(item.get("propertyCode", item.get("id", "")))
                if not property_id:
                    continue

                # Safe mapping of property type to our enumeration
                raw_type = item.get("propertyType", "apartment").lower()
                if "penthouse" in raw_type or "atico" in raw_type:
                    rental_type = "PENTHOUSE"
                elif "house" in raw_type or "chalet" in raw_type:
                    rental_type = "HOUSE"
                elif "room" in raw_type:
                    rental_type = "ROOM"
                else:
                    rental_type = "APARTMENT"

                nl = NormalizedListing(
                    external_id=property_id,
                    source="idealista",
                    url=item.get("url", f"https://www.idealista.com/en/inmueble/{property_id}/"),
                    title=item.get("suggestedSelfPromotion", item.get("address", "Rental Listing")),
                    description=item.get("description", "No description provided."),
                    price=float(item.get("price", 0)),
                    rental_type=rental_type,
                    city=item.get("municipality", "Barcelona"),
                    district=item.get("district"),
                    area_m2=float(item.get("size", 0)) if item.get("size") else None,
                    rooms=item.get("rooms"),
                    bathrooms=item.get("bathrooms"),
                    images=[img.get("url") for img in item.get("multimedia", {}).get("images", [])] if item.get("multimedia") else [],
                    raw_data=item
                )
                normalized.append(nl)
            except Exception as e:
                logger.warning("Failed to normalize individual listing", error=str(e), item_id=item.get("propertyCode"))
                continue
                
        return normalized
