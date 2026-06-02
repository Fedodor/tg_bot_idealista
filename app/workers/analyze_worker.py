"""
AI Analysis worker — deep analysis layer.

Polls for matched listings that need AI enrichment and runs the LLM analysis.
"""
from __future__ import annotations

from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.db.models import Match, Listing, ListingAnalysis, ListingStatus
from app.db.session import AsyncSessionFactory
from app.services.ai_analysis import AIAnalysisService
from app.config import settings
from app.logging import get_logger

logger = get_logger(__name__)


class AnalyzeWorker:
    """Worker responsible for enrichment of listings using AI."""

    def __init__(self, ai_service: AIAnalysisService | None = None) -> None:
        self.ai = ai_service or AIAnalysisService()

    async def run_once(self) -> None:
        """Process pending matched listings through the AI pipeline."""
        logger.info("AI Analysis cycle started")
        
        async with AsyncSessionFactory() as session:
            # 1. Find matches that need notify but haven't been analyzed (Task 6.26)
            # and listings that don't have analysis yet (Task 6.24)
            stmt = (
                select(Listing)
                .where(Listing.status != ListingStatus.REMOVED)
                .where(~Listing.id.in_(select(ListingAnalysis.listing_id)))
                # Only analyze if it actually matched someone (Task 8.1 in plan)
                .where(Listing.id.in_(select(Match.listing_id).where(Match.should_notify == True)))
                .limit(10) # Process in small batches
            )
            
            result = await session.execute(stmt)
            listings_to_analyze = result.scalars().all()
            
            if not listings_to_analyze:
                logger.debug("No listings pending AI analysis")
                return
                
            logger.info("Starting AI analysis for batch", count=len(listings_to_analyze))
            
            for listing in listings_to_analyze:
                # We analyze in English primarily for the DB, 
                # Russian translation can be done in notify service or by LLM
                analysis = await self.ai.analyze_listing(listing.description or listing.title)
                
                if analysis:
                    new_analysis = ListingAnalysis(
                        listing_id=listing.id,
                        model_name=self.ai.model,
                        analysis_version="1.0",
                        summary_en=analysis.summary,
                        summary_ru=analysis.summary, # Simplified: can be improved with a second LLM pass later
                        risk_level=analysis.risk_level,
                        red_flags=analysis.red_flags,
                        positive_signals=analysis.positive_signals,
                        questions_to_ask=analysis.questions_to_ask
                    )
                    session.add(new_analysis)
                    logger.info("Listing analyzed successfully", listing_id=listing.id, risk=analysis.risk_level)
                else:
                    logger.warning("AI analysis failed for listing", listing_id=listing.id)
                
            await session.commit()
            logger.info("AI Analysis cycle complete")
