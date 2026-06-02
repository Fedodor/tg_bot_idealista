"""
Simple Admin CLI for Relocation Rental Radar.

Enables manual data import, system monitoring, and pipeline orchestration.
"""
from __future__ import annotations

import asyncio
import argparse

from sqlalchemy import select, func

from app.db.models import Listing, User, UserSearch, Match, Notification
from app.db.session import AsyncSessionFactory
from app.sources.manual_import import ManualImportSource
from app.workers.ingest_worker import IngestWorker
from app.workers.matching_worker import MatchingWorker
from app.workers.analyze_worker import AnalyzeWorker
from app.workers.notify_worker import NotifyWorker
from app.logging import setup_logging, get_logger

logger = get_logger(__name__)


async def cmd_import(file_path: str):
    """Manually triggers ingestion from a file."""
    source = ManualImportSource(file_path)
    worker = IngestWorker(sources=[source])
    await worker.run_once()


async def cmd_stats():
    """Prints system-wide statistics."""
    async with AsyncSessionFactory() as session:
        # Total counts
        listing_count = await session.scalar(select(func.count(Listing.id)))
        user_count = await session.scalar(select(func.count(User.id)))
        match_count = await session.scalar(select(func.count(Match.id)))
        notify_count = await session.scalar(select(func.count(Notification.id)))
        
        print("\n--- Rental Radar Stats ---")
        print(f"Total Listings:  {listing_count}")
        print(f"Total Users:     {user_count}")
        print(f"Total Matches:   {match_count}")
        print(f"Total Alerts:    {notify_count}")
        print("--------------------------\n")


async def cmd_run_pipeline():
    """Runs the full automation pipeline once."""
    print(">>> Starting full pipeline...")
    
    # 1. Ingest
    print("Step 0: Internet Search (Ingestion)...")
    await IngestWorker().run_once()
    
    # 2. Match
    print("Step 1: Matching Engine...")
    await MatchingWorker().run_once()
    
    # 3. Analyze (AI)
    print("Step 2: AI Analysis...")
    await AnalyzeWorker().run_once()
    
    # 4. Notify
    print("Step 3: Notifications...")
    worker = NotifyWorker()
    await worker.run_once()
    await worker.stop()
    
    print("--- Pipeline run complete.")


def main():
    setup_logging("INFO")
    parser = argparse.ArgumentParser(description="Rental Radar Admin Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Import
    import_parser = subparsers.add_parser("import", help="Import listings from file")
    import_parser.add_argument("file", help="Path to CSV or JSON file")

    # Stats
    subparsers.add_parser("stats", help="Show system statistics")

    # Full Run
    subparsers.add_parser("run", help="Run full pipeline (Match -> Analyze -> Notify)")

    args = parser.parse_args()

    if args.command == "import":
        asyncio.run(cmd_import(args.file))
    elif args.command == "stats":
        asyncio.run(cmd_stats())
    elif args.command == "run":
        asyncio.run(cmd_run_pipeline())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
