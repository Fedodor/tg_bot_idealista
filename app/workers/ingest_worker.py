"""
Ingestion worker — entrance for new data.

Orchestrates fetching from sources and saving to the DB with deduplication.
"""
from __future__ import annotations

from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from app.db.models import Listing, ListingStatus
from app.db.session import AsyncSessionFactory
from app.sources.rapidapi_idealista import RapidAPISource
from app.services.deduplication import generate_dedup_hash
from app.logging import get_logger

logger = get_logger(__name__)

class IngestWorker:
    """Worker responsible for live internet data collection."""

    def __init__(self, source: RapidAPISource | None = None) -> None:
        self.source = source or RapidAPISource()

    async def run_once(self) -> None:
        """Fetch listings and upsert them into the database."""
        logger.info("Ingestion cycle started (Internet Search)")
        
        # 1. Fetch live data
        new_listings = await self.source.fetch_listings(city="barcelona")
        
        if not new_listings:
            logger.warning("No listings fetched from live search.")
            return

        logger.info("Fetched live listings", count=len(new_listings))
        
        # 2. Upsert logic
        async with AsyncSessionFactory() as session:
            new_count = 0
            for nl in new_listings:
                dedup_hash = generate_dedup_hash(nl)
                
                # SQLAlchemy Upsert (PostgreSQL specific)
                stmt = insert(Listing).values(
                    external_id=nl.external_id,
                    source=nl.source,
                    url=nl.url,
                    title=nl.title,
                    description=nl.description,
                    price=nl.price,
                    currency=nl.currency,
                    rental_type=nl.rental_type,
                    city=nl.city,
                    district=nl.district,
                    area_m2=nl.area_m2,
                    rooms=nl.rooms,
                    bathrooms=nl.bathrooms,
                    floor=nl.floor,
                    has_lift=nl.has_lift,
                    images=nl.images,
                    dedup_hash=dedup_hash,
                    status=ListingStatus.ACTIVE,
                    last_seen_at=datetime.utcnow()
                )
                
                # On conflict: update last_seen_at and price
                stmt = stmt.on_conflict_do_update(
                    index_elements=['external_id', 'source'],
                    set_={
                        "price": stmt.excluded.price,
                        "last_seen_at": stmt.excluded.last_seen_at,
                        "status": ListingStatus.ACTIVE # Re-activate if it reappeared
                    }
                )
                
                res = await session.execute(stmt)
                # Note: Rowcount estimation in async sessions can be tricky
                new_count += 1
                
            await session.commit()
            logger.info("Ingestion cycle complete", processed=new_count)
