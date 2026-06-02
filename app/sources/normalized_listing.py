"""
Normalized Listing model for the Relocation Rental Radar.
All source adapters must return data in this format.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field

class NormalizedListing(BaseModel):
    """
    Standardized listing format across all sources.
    Maps to app.db.models.Listing.
    """
    external_id: str = Field(..., description="ID from the source (e.g. Idealista listing ID)")
    source: str = Field(..., description="Source name (e.g. idealista, manual)")
    url: str = Field(..., description="Full URL to the listing")
    title: str = Field(..., description="Short title of the listing")
    description: str | None = Field(None, description="Full description text")
    
    price: float = Field(..., description="Monthly rent in EUR")
    currency: str = Field("EUR")
    
    rental_type: str = Field("apartment", description="apartment, room, or house")
    city: str = Field("Barcelona")
    district: str | None = None
    neighborhood: str | None = None
    
    area_m2: float | None = None
    rooms: int | None = None
    bathrooms: int | None = None
    floor: str | None = None
    has_lift: bool | None = None
    
    images: list[str] = Field(default_factory=list)
    
    # Metadata for ingestion logic
    raw_data: dict[str, Any] = Field(default_factory=dict, description="Original source data")
    extracted_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        frozen = True # Make it immutable to ensure data integrity through the pipe
