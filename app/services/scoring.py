"""
Deterministic scoring logic for listings.
"""
from __future__ import annotations

from typing import Any
from app.db.models import Listing, UserSearch

def calculate_score(listing: Listing, search: UserSearch) -> tuple[int, list[str]]:
    """
    Calculates a match score (0-100) and returns a list of human-readable reasons.
    """
    score = 40  # Starting base score for passing hard filters
    reasons = []

    # 1. Price fit (+30)
    # If price is towards the lower end of user max, give bonus
    if search.max_price and listing.price <= (search.max_price * 0.8):
        score += 30
        reasons.append("Great price for your budget")
    elif search.max_price and listing.price <= search.max_price:
        score += 15
        reasons.append("Fits your budget")

    # 2. Area match (+15)
    # Check if district or neighborhood matches preferred areas
    listing_areas = []
    if listing.district: listing_areas.append(listing.district.lower())
    if listing.neighborhood: listing_areas.append(listing.neighborhood.lower())
    
    if search.preferred_areas:
        preferred = [a.lower() for a in search.preferred_areas]
        if any(area in preferred for area in listing_areas):
            score += 15
            reasons.append("In your preferred area")

    # 3. Completeness & Quality
    if listing.is_furnished:
        score += 5
        reasons.append("Furnished")
    
    if listing.has_elevator:
        score += 5

    # 4. Red flags (Negative scoring)
    if not listing.description or len(listing.description) < 100:
        score -= 20
        reasons.append("Very short description")
        
    # Clamp final score
    final_score = max(0, min(100, score))
    
    return final_score, reasons


def get_score_band(score: int) -> str:
    """Maps numerical score to a human-readable band."""
    if score >= 85: return "Excellent"
    if score >= 70: return "Good"
    if score >= 50: return "Average"
    return "Poor"
