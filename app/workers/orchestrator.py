"""
Orchestrator — The continuous loop that runs the pipeline.
"""
from __future__ import annotations

import asyncio
from app.workers.ingest_worker import IngestWorker
from app.workers.matching_worker import MatchingWorker
from app.workers.analyze_worker import AnalyzeWorker
from app.workers.notify_worker import NotifyWorker
from app.logging import get_logger

logger = get_logger(__name__)

class Orchestrator:
    """
    Main background process that runs the end-to-end pipeline at intervals.
    """
    def __init__(self, interval_seconds: int = 900): # Default 15 minutes
        self.interval = interval_seconds
        self.ingest_worker = IngestWorker()
        self.matching_worker = MatchingWorker()
        self.analyze_worker = AnalyzeWorker()
        self.notify_worker = NotifyWorker()

    async def start(self):
        """Starts the infinite loop."""
        logger.info("Background Orchestrator started", interval=self.interval)
        
        while True:
            try:
                logger.info("--- Starting Pipeline Cycle ---")
                
                # 1. Ingest new listings
                await self.ingest_worker.run_once()
                
                # 2. Match with users
                await self.matching_worker.run_once()
                
                # 3. Analyze potential matches
                await self.analyze_worker.run_once()
                
                # 4. Notify users
                await self.notify_worker.run_once()
                
                logger.info("--- Cycle Complete. Sleeping... ---", seconds=self.interval)
                await asyncio.sleep(self.interval)
                
            except Exception as e:
                logger.error("Orchestrator encountered an error in cycle", error=str(e), exc_info=True)
                # Sleep a bit before retrying to prevent rapid-fire failures
                await asyncio.sleep(60)
