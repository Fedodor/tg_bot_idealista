"""
Unit tests for the matching and scoring services.
"""
from __future__ import annotations

import pytest
from app.db.models import Listing, UserSearch, RentalType
from app.services.matching import check_hard_filters
from app.services.scoring import calculate_score

def test_hard_filters_price():
    """Verify city and price filtering logic."""
    search = UserSearch(city="Barcelona", min_price=500, max_price=1000, rental_type=RentalType.BOTH)
    
    # Passing
    l1 = Listing(city="Barcelona", price=800, rental_type="apartment", status="active")
    assert check_hard_filters(l1, search) is True
    
    # Failing - Wrong city
    l2 = Listing(city="Madrid", price=800, rental_type="apartment", status="active")
    assert check_hard_filters(l2, search) is False
    
    # Failing - Too expensive
    l3 = Listing(city="Barcelona", price=1200, rental_type="apartment", status="active")
    assert check_hard_filters(l3, search) is False

def test_hard_filters_type():
    """Verify rental type filtering logic."""
    search = UserSearch(city="Barcelona", rental_type=RentalType.ROOM)
    
    # Passing - Match room
    l1 = Listing(city="Barcelona", price=500, rental_type="room", status="active")
    assert check_hard_filters(l1, search) is True
    
    # Failing - Search wants room, listing is apartment
    l2 = Listing(city="Barcelona", price=500, rental_type="apartment", status="active")
    assert check_hard_filters(l2, search) is False

def test_scoring_logic():
    """Verify scoring rules and reasons."""
    search = UserSearch(city="Barcelona", max_price=1000, preferred_areas=["Gracia"])
    listing = Listing(
        city="Barcelona", 
        price=700, # Within 80% of 1000 (+30)
        district="Gracia", # Matches preferred (+15)
        is_furnished=True, # (+5)
        description="This is a very long description that definitely has more than one hundred characters to avoid the negative scoring red flag penalty for short descriptions."
    )
    
    score, reasons = calculate_score(listing, search)
    # 40 (Base) + 30 + 15 + 5 = 90
    assert score == 90
    assert "Great price for your budget" in reasons
    assert "In your preferred area" in reasons
