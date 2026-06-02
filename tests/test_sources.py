"""
Unit tests for source adapters.
"""
from __future__ import annotations

import os
import json
import pytest
from app.sources.manual_import import ManualImportSource
from app.sources.normalized_listing import NormalizedListing

@pytest.mark.asyncio
async def test_manual_import_json(tmp_path):
    """Verifies that ManualImportSource correctly parses a JSON file."""
    data = [
        {"title": "Apartment A", "price": 1000, "city": "Barcelona", "rooms": 2},
        {"title": "Room B", "price": 500, "city": "Madrid", "rental_type": "room"}
    ]
    file_path = tmp_path / "test.json"
    file_path.write_text(json.dumps(data))
    
    source = ManualImportSource(str(file_path))
    listings = await source.fetch()
    
    assert len(listings) == 2
    assert listings[0].title == "Apartment A"
    assert listings[0].price == 1000
    assert listings[1].city == "Madrid"
    assert listings[1].rental_type == "room"
    assert isinstance(listings[0], NormalizedListing)


@pytest.mark.asyncio
async def test_manual_import_csv(tmp_path):
    """Verifies that ManualImportSource correctly parses a CSV file."""
    csv_content = (
        "title,price,city,rooms\n"
        "Flat X,1500,Barcelona,3\n"
        "Studio Y,900,Barcelona,1"
    )
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content)
    
    source = ManualImportSource(str(file_path))
    listings = await source.fetch()
    
    assert len(listings) == 2
    assert listings[0].title == "Flat X"
    assert listings[0].price == 1500.0
    assert listings[1].rooms == 1
    assert isinstance(listings[0], NormalizedListing)
