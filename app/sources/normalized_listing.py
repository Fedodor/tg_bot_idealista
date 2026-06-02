"""
NormalizedListing — the canonical data transfer object for all listings.

Every source adapter must convert its raw data into a NormalizedListing
before returning it. This ensures the rest of the pipeline is source-agnostic.

Rules (from AGENTS.md):
  - Use Pydantic v2 for all data models.
  - dedup_hash is computed here from: price + city + area_m2 + title.
  - Never store phone numbers or emails in these fields.
"""
from __future__ import annotations

import hashlib
from typing import Any, Optional

from pydantic import BaseModel, Field, model_validator


class NormalizedListing(BaseModel):
    """Canonical listing object output by every source adapter."""

    # --- Source metadata ---
    source: str = Field(..., description="Source adapter name, e.g. 'manual_import'")
    external_id: Optional[str] = Field(None, description="ID from the source system")
    url: Optional[str] = Field(None, description="Direct URL to the listing")

    # --- Core listing fields ---
    title: Optional[str] = None
    description: Optional[str] = Field(None, description="Never include phone/email")
    price: Optional[float] = None
    currency: str = "EUR"
    city: Optional[str] = None
    district: Optional[str] = None
    neighborhood: Optional[str] = None
    address_text: Optional[str] = None
    rental_type: str = "unknown"   # apartment | room | both | unknown
    area_m2: Optional[float] = None
    rooms: Optional[int] = None
    bathrooms: Optional[int] = None
    floor: Optional[int] = None
    has_elevator: Optional[bool] = None
    is_furnished: Optional[bool] = None
    agency_or_private: Optional[str] = None
    available_from: Optional[str] = None

    # --- Raw payload for debugging ---
    raw_data: Optional[dict[str, Any]] = None

    # --- Deduplication hash (computed automatically) ---
    dedup_hash: Optional[str] = Field(None, description="SHA-256 of price+city+area_m2+title")

    @model_validator(mode="after")
    def compute_dedup_hash(self) -> "NormalizedListing":
        """Compute dedup_hash from the four canonical fields if not already set."""
        if self.dedup_hash is None:
            raw = "|".join([
                str(self.price or ""),
                str(self.city or "").lower().strip(),
                str(self.area_m2 or ""),
                str(self.title or "").lower().strip(),
            ])
            self.dedup_hash = hashlib.sha256(raw.encode()).hexdigest()
        return self
