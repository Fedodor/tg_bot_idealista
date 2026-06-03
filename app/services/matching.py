"""
Hard filtering logic for listings and user searches.
"""
from __future__ import annotations

from app.db.models import Listing, UserSearch, RentalType, ListingStatus

def check_hard_filters(listing: Listing, search: UserSearch) -> bool:
    """
    Returns True if the listing passes all mandatory user filters.
    
    Filters:
    - City match
    - Rental type match (Apartment/Room/Both)
    - Price within [min_price, max_price]
    - Status is not 'removed'
    """
    # 1. Status check (use enum comparison)
    if listing.status == ListingStatus.REMOVED:
        return False

    # 2. City match (Case insensitive)
    if listing.city and listing.city.lower() != search.city.lower():
        return False

    # 3. Rental type match (DB stores UPPERCASE enum values)
    if search.rental_type == RentalType.APARTMENT:
        if listing.rental_type != RentalType.APARTMENT:
            return False
    elif search.rental_type == RentalType.ROOM:
        if listing.rental_type != RentalType.ROOM:
            return False
    # If search.rental_type is BOTH, allow any listing rental_type

    # 4. Price check
    if search.min_price and listing.price and listing.price < search.min_price:
        return False
    if search.max_price and listing.price and listing.price > search.max_price:
        return False

    return True
