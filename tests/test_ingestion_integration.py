"""
Integration tests for the ingestion pipeline.
"""
from __future__ import annotations

import pytest
from sqlalchemy import select
from app.db.models import Listing
from app.db.session import AsyncSessionFactory
from app.sources.manual_import import ManualImportSource
from app.workers.ingest_worker import IngestWorker

@pytest.mark.asyncio
async def test_ingest_worker_db_integration(tmp_path):
    """
    End-to-end test: 
    1. Create sample JSON.
    2. Run IngestWorker.
    3. Verify data in DB.
    """
    # 1. Setup sample file
    import json
    data = [{
        "external_id": "test_123",
        "title": "Integration Flat",
        "price": 1200,
        "city": "Barcelona",
        "area_m2": 50
    }]
    file_path = tmp_path / "import.json"
    file_path.write_text(json.dumps(data))
    
    # 2. Run worker
    source = ManualImportSource(str(file_path))
    worker = IngestWorker(sources=[source])
    await worker.run_once()
    
    # 3. Verify DB
    async with AsyncSessionFactory() as session:
        stmt = select(Listing).where(Listing.external_id == "test_123")
        result = await session.execute(stmt)
        listing = result.scalar_one_or_none()
        
        assert listing is not None
        assert listing.title == "Integration Flat"
        assert listing.price == 1200.0
        assert listing.dedup_hash is not None


@pytest.mark.asyncio
async def test_ingest_worker_deduplication():
    """Verifies that duplicate listings update existing records instead of creating new ones."""
    from app.sources.base import BaseSource
    from app.sources.normalized_listing import NormalizedListing
    
    class MockSource(BaseSource):
        source_name = "mock"
        async def fetch(self):
            return [NormalizedListing(
                source="mock", title="Dup Flat", price=1000, city="BCN", area_m2=40
            )]
        async def health_check(self): return True

    worker = IngestWorker(sources=[MockSource()])
    
    # Run twice
    await worker.run_once() # New
    await worker.run_once() # Duplicate (Update)
    
    async with AsyncSessionFactory() as session:
        stmt = select(Listing).where(Listing.title == "Dup Flat")
        result = await session.execute(stmt)
        listings = result.scalars().all()
        
        assert len(listings) == 1
        assert listings[0].first_seen_at <= listings[0].last_seen_at
