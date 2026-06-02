"""
Matching worker — identifies listings for users.

Runs after ingestion to compare new listings against active user searches.
"""
from __future__ import annotations

from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.db.models import Listing, UserSearch, Match
from app.db.session import AsyncSessionFactory
from app.services.matching import check_hard_filters
from app.services.scoring import calculate_score
from app.logging import get_logger

logger = get_logger(__name__)


class MatchingWorker:
    """Worker responsible for finding matches for users."""

    async def run_once(self) -> None:
        """Process all active searches against recently updated listings."""
        async with AsyncSessionFactory() as session:
            # 1. Fetch active searches
            search_stmt = select(UserSearch).where(UserSearch.is_active == True).options(selectinload(UserSearch.user))
            search_result = await session.execute(search_stmt)
            active_searches = search_result.scalars().all()
            
            if not active_searches:
                logger.info("No active searches to process")
                return

            # 2. Fetch listings
            listing_stmt = select(Listing).where(Listing.status != "removed")
            listing_result = await session.execute(listing_stmt)
            listings = listing_result.scalars().all()
            
            logger.info("Matching cycle started", search_count=len(active_searches), listing_count=len(listings))
            
            match_count = 0
            # Track processed pairs in this session to avoid duplicates if user has multiple searches
            processed_pairs = set() 

            for search in active_searches:
                for listing in listings:
                    pair = (search.user_id, listing.id)
                    if pair in processed_pairs:
                        continue

                    # Check if match already exists in DB
                    dup_stmt = select(Match).where(
                        and_(Match.user_id == search.user_id, Match.listing_id == listing.id)
                    )
                    dup_result = await session.execute(dup_stmt)
                    if dup_result.scalar_one_or_none():
                        processed_pairs.add(pair)
                        continue

                    # Apply filters and scoring
                    if not check_hard_filters(listing, search):
                        continue

                    score, reasons = calculate_score(listing, search)
                    
                    # Create match
                    new_match = Match(
                        user_id=search.user_id,
                        search_id=search.id,
                        listing_id=listing.id,
                        match_score=score,
                        reason_en=", ".join(reasons) if reasons else "Matched your core filters",
                        reason_ru="Подходит под ваши фильтры",
                        should_notify=(score >= 50)
                    )
                    session.add(new_match)
                    # Flush immediately to ensure DB constraint is respected for subsequent searches in loop
                    await session.flush() 
                    
                    processed_pairs.add(pair)
                    match_count += 1
            
            await session.commit()
            logger.info("Matching cycle complete", new_matches=match_count)
