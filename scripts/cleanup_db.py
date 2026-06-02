"""
Quick cleanup script to clear matches and dummy users
to force the system to notify the REAL user.
"""
import asyncio
from sqlalchemy import delete
from app.db.session import AsyncSessionFactory
from app.db.models import User, Match, Notification, ListingAnalysis

async def cleanup():
    async with AsyncSessionFactory() as session:
        # 1. Delete notifications and matches first (due to FKs)
        await session.execute(delete(Notification))
        await session.execute(delete(Match))
        await session.execute(delete(ListingAnalysis))
        
        # 2. Delete the dummy user
        await session.execute(delete(User).where(User.telegram_id == 12345678))
        
        await session.commit()
        print("Cleanup complete. Redundant data purged.")

if __name__ == "__main__":
    asyncio.run(cleanup())
