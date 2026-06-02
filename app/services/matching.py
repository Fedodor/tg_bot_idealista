"""
Hard filtering logic for listings and user searches.
"""
from __future__ import annotations

from app.db.models import Listing, UserSearch, RentalType

def check_hard_filters(listing: Listing, search: UserSearch) -> bool:
    """
    Returns True if the listing passes all mandatory user filters.
    
    Filters:
    - City match
    - Rental type match (Apartment/Room/Both)
    - Price within [min_price, max_price]
    - Status is not 'removed'
    """
    # 1. Status check
    if listing.status == "removed":
        return False

    # 2. City match (Case insensitive)
    if listing.city.lower() != search.city.lower():
        return False

    # 3. Rental type match
    if search.rental_type == RentalType.APARTMENT:
        if listing.rental_type != "apartment":
            return False
    elif search.rental_type == RentalType.ROOM:
        if listing.rental_type != "room":
            return False
    # If search.rental_type is BOTH, we allow any listing rental_type
    
    # 4. Price check
    if search.min_price and listing.price < search.min_price:
        return False
    if search.max_price and listing.price > search.max_price:
        return False

    return True
