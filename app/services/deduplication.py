"""
Deduplication service for listings.

Ensures we don't notify users about the same listing twice.
Uses a hash based on key property features.
"""
from __future__ import annotations

import hashlib
from app.sources.normalized_listing import NormalizedListing
from app.logging import get_logger

logger = get_logger(__name__)

def generate_dedup_hash(listing: NormalizedListing) -> str:
    """
    Generates a unique SHA-256 hash for a listing (Task 7.3).
    Formula: price + city + area_m2 + title (lowercased/stripped).
    """
    # We round price and area to avoid floating point jitter
    price_val = int(listing.price)
    area_val = int(listing.area_m2 or 0)
    city_val = listing.city.lower().strip()
    title_val = listing.title.lower().strip()
    
    components = f"{price_val}|{city_val}|{area_val}|{title_val}"
    return hashlib.sha256(components.encode("utf-8")).hexdigest()
