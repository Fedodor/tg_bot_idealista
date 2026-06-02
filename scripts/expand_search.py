"""
Update the real user's search to match everything.
"""
import asyncio
from sqlalchemy import update
from app.db.session import AsyncSessionFactory
from app.db.models import UserSearch

async def update_search():
    async with AsyncSessionFactory() as session:
        await session.execute(
            update(UserSearch)
            .values(min_price=0.0, max_price=5000.0)
        )
        await session.commit()
        print("User search updated to match all price ranges.")

if __name__ == "__main__":
    asyncio.run(update_search())
