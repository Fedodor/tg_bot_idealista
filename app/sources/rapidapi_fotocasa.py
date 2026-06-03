"""
RapidAPI Source Adapter for Fotocasa.
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

class FotocasaSource(BaseSource):
    """
    Implementation of BaseSource for Fotocasa via RapidAPI.
    Host: fotocasa1.p.rapidapi.com
    Endpoint: /listproperties
    """

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or settings.rapidapi_key
        self.host = "fotocasa1.p.rapidapi.com" 

    async def fetch_listings(self, city: str = "barcelona", **kwargs) -> Sequence[NormalizedListing]:
        """Fetches listings from Fotocasa RapidAPI."""
        if not self.api_key:
            logger.error("RapidAPI key missing for Fotocasa")
            return []

        url = f"https://{self.host}/listproperties"
        
        # Fotocasa requires locationId and Coordinates
        # For Barcelona: 724,9,8,31,0,8019,0,0,0 (approx)
        # Coordinates for BCN center
        params = {
            "locationId": "724,9,8,31,0,8019,0,0,0", 
            "propertyType": "Homes",
            "operation": "rent",
            "pageNumber": "1",
            "latitude": "41.3851",
            "longitude": "2.1734"
        }

        # Handle price range if provided
        if kwargs.get("min_price"): params["minPrice"] = str(kwargs.get("min_price"))
        if kwargs.get("max_price"): params["maxPrice"] = str(kwargs.get("max_price"))

        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.host
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.get(url, headers=headers, params=params)
                if response.status_code != 200:
                    logger.warning("Fotocasa API error", status=response.status_code, body=response.text)
                    return []
                
                data = response.json()
                return self._normalize_response(data)
        except Exception as e:
            logger.error("Fotocasa fetch failed", error=str(e))
            return []

    async def health_check(self) -> bool:
        return self.api_key is not None

    def _normalize_response(self, data: dict) -> list[NormalizedListing]:
        normalized = []
        # Fotocasa structure: data['realEstates']
        items = data.get("data", {}).get("realEstates", [])

        for item in items:
            try:
                property_id = str(item.get("id", ""))
                if not property_id: continue

                # Get details safely
                features = item.get("features", [])
                surface = next((f.get("value") for f in features if f.get("id") == "surface"), None)
                rooms = next((f.get("value") for f in features if f.get("id") == "rooms"), None)
                bathrooms = next((f.get("value") for f in features if f.get("id") == "bathrooms"), None)

                nl = NormalizedListing(
                    external_id=property_id,
                    source="fotocasa",
                    url=item.get("url", f"https://www.fotocasa.es/en/vivienda/barcelona/{property_id}"),
                    title=item.get("address", "Fotocasa Rental"),
                    description=item.get("description", ""),
                    price=float(item.get("price", {}).get("value", 0)),
                    rental_type="APARTMENT",
                    city="Barcelona",
                    district=item.get("location", {}).get("district"),
                    area_m2=float(surface) if surface else None,
                    rooms=int(rooms) if rooms else None,
                    bathrooms=int(bathrooms) if bathrooms else None,
                    images=[img.get("url") for img in item.get("multimedia", [])],
                    raw_data=item
                )
                normalized.append(nl)
            except Exception as e:
                logger.warning(f"Failed to normalize Fotocasa item {item.get('id')}: {e}")
                continue
        return normalized
