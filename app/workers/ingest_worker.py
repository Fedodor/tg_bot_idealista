"""
Ingestion worker — entrance for new data.

Orchestrates fetching from sources and saving to the DB with deduplication.
"""
from __future__ import annotations

import asyncio
from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from app.db.models import Listing, ListingStatus, UserSearch
from app.db.session import AsyncSessionFactory
from app.sources.base import BaseSource
from app.sources.rapidapi_idealista import RapidAPISource
from app.sources.rapidapi_habitaclia import HabitacliaSource
# FotocasaSource disabled: returns 403 (subscription required)
# from app.sources.rapidapi_fotocasa import FotocasaSource
from app.services.deduplication import generate_dedup_hash
from app.logging import get_logger

logger = get_logger(__name__)

class IngestWorker:
    """Worker responsible for live internet data collection from multiple sources."""

    def __init__(self, sources: list[BaseSource] | None = None) -> None:
        self.sources = sources or [
            RapidAPISource(),
            HabitacliaSource(),
            # FotocasaSource(),  # Re-enable once RapidAPI plan allows access
        ]

    async def run_once(self) -> None:
        """Fetch listings from all sources and upsert them into the database."""
        logger.info("Ingestion cycle started (Multi-Source Search)")
        
        # 1. Determine if we need a deep scan (check for new searches)
        async with AsyncSessionFactory() as session:
            stmt = select(UserSearch).where(UserSearch.last_full_scan_at == None, UserSearch.is_active == True)
            res = await session.execute(stmt)
            needs_deep_scan = res.scalars().first() is not None

        # 2. Iterate through each source and process its listings
        total_processed = 0
        for source in self.sources:
            source_name = source.__class__.__name__
            logger.info(f"Fetching from source: {source_name}")
            
            fetch_params = {"city": "barcelona"}
            if needs_deep_scan:
                logger.info(f"New search detected, performing deep scan on {source_name} (1 week back)")
                fetch_params["since"] = "W"
                fetch_params["max_items"] = 40

            new_listings = await source.fetch_listings(**fetch_params)
            
            if not new_listings:
                logger.warning(f"No listings fetched from {source_name}.")
                continue

            logger.info(f"Processing {len(new_listings)} listings from {source_name}")
            
            # 3. Upsert logic for this specific source's listings
            async with AsyncSessionFactory() as session:
                source_new_count = 0
                for nl in new_listings:
                    dedup_hash = generate_dedup_hash(nl)
                    
                    # Logical Deduplication: check if same content already exists
                    existing_stmt = select(Listing).where(Listing.dedup_hash == dedup_hash)
                    existing_res = await session.execute(existing_stmt)
                    existing_listing = existing_res.scalar_one_or_none()
                    
                    if existing_listing:
                        # Update existing semantic record
                        existing_listing.price = nl.price
                        existing_listing.last_seen_at = datetime.utcnow()
                        existing_listing.status = ListingStatus.ACTIVE
                        source_new_count += 1
                        continue

                    # Technical Upsert: check if external_id/source already exists
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
                    
                    stmt = stmt.on_conflict_do_update(
                        index_elements=['external_id', 'source'],
                        set_={
                            "price": stmt.excluded.price,
                            "last_seen_at": stmt.excluded.last_seen_at,
                            "status": ListingStatus.ACTIVE
                        }
                    )
                    
                    await session.execute(stmt)
                    source_new_count += 1
                    
                await session.commit()
                total_processed += source_new_count
                logger.info(f"Source {source_name} complete", processed=source_new_count)

        # 4. Mark all searches as 'fully scanned' for history
        if needs_deep_scan:
            async with AsyncSessionFactory() as session:
                await session.execute(
                    update(UserSearch)
                    .where(UserSearch.last_full_scan_at == None)
                    .values(last_full_scan_at=datetime.utcnow())
                )
                await session.commit()

        logger.info("Ingestion cycle complete", total_processed=total_processed)
