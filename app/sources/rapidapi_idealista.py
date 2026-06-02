"""
RapidAPI Source Adapter for Idealista.
Updated for kiwimaker endpoint: https://rapidapi.com/kiwimaker/api/idealista-real-estate
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

class RapidAPISource(BaseSource):
    """
    Implementation of BaseSource using RapidAPI's Idealista Scraper (kiwimaker).
    Endpoint: /properties/list
    """

    def __init__(self, api_key: str | None = None, host: str | None = None) -> None:
        self.api_key = api_key or settings.rapidapi_key
        self.host = host or settings.rapidapi_host
        self.base_url = f"https://{self.host}"

    async def fetch_listings(self, city: str = "barcelona", rental_type: str = "apartments", **kwargs) -> Sequence[NormalizedListing]:
        """
        Calls the RapidAPI endpoint and normalizes the results.
        """
        if not self.api_key:
            logger.error("RapidAPI Key missing. Cannot fetch live listings.")
            return []

        # The kiwimaker API uses /properties/list
        url = f"{self.base_url}/properties/list"
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        }
        
        # Payload based on kiwimaker's playground
        params = {
            "locationName": city,
            "operation": "rent",
            "propertyType": rental_type,
            "locale": "en",
            "country": "es",
            "maxItems": "20"
        }

        try:
            async with httpx.AsyncClient(timeout=45.0) as client:
                response = await client.get(url, headers=headers, params=params)
                
                if response.status_code == 404:
                    # Fallback if endpoint name is slightly different in subscription
                    logger.warning("Main endpoint failed (404), trying fallback /search")
                    url = f"{self.base_url}/search"
                    response = await client.get(url, headers=headers, params=params)

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
        Parses complex JSON from RapidAPI into flat NormalizedListing objects.
        """
        normalized = []
        # kiwimaker structure: elementList
        items = data.get("elementList") or data.get("data", [])
        
        # If API returns a message instead of list
        if isinstance(items, dict):
            items = items.get("elementList", [])

        for item in items:
            try:
                # Basic mapping logic (Adjust based on actual API payload)
                property_id = str(item.get("propertyCode", item.get("id", "")))
                if not property_id:
                    continue

                nl = NormalizedListing(
                    external_id=property_id,
                    source="idealista",
                    url=item.get("url", f"https://www.idealista.com/en/inmueble/{property_id}/"),
                    title=item.get("suggestedSelfPromotion", item.get("address", "Rental Listing")),
                    description=item.get("description", "No description provided."),
                    price=float(item.get("price", 0)),
                    rental_type=item.get("propertyType", "apartment"),
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
