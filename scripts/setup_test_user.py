"""
Quick utility to register a test user and search in the DB
so we can test matching and notifications immediately.
"""
import asyncio
from datetime import datetime
from sqlalchemy import select, func
from app.db.session import AsyncSessionFactory
from app.db.models import User, UserSearch, Language

async def setup_test_data():
    async with AsyncSessionFactory() as session:
        # 1. Check if user exists
        res = await session.execute(select(User).filter_by(telegram_id=12345678))
        user = res.scalar_one_or_none()
        
        if not user:
            user = User(
                telegram_id=12345678, # Dummy ID
                language=Language.RU, 
                consent_at=datetime.utcnow(), 
                status="active"
            )
            session.add(user)
            await session.flush()
            print("Registered test user.")

        # 2. Add a search for Barcelona
        res = await session.execute(select(UserSearch).filter_by(user_id=user.id))
        search = res.scalar_one_or_none()
        
        if not search:
            search = UserSearch(
                user_id=user.id,
                city="Barcelona",
                max_price=2000.0,
                rental_type="apartment",
                preferred_areas=["Gracia", "Eixample"],
                is_active=True
            )
            session.add(search)
            print("Registered test search for Barcelona.")
            
        await session.commit()

if __name__ == "__main__":
    asyncio.run(setup_test_data())
