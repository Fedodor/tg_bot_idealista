import asyncio
from app.db.session import AsyncSessionFactory
from sqlalchemy import text

async def check_enum():
    async with AsyncSessionFactory() as session:
        try:
            res = await session.execute(text("SELECT enumlabel FROM pg_enum JOIN pg_type ON pg_type.oid = pg_enum.enumtypid WHERE typname = 'listing_rental_type_enum'"))
            labels = [row[0] for row in res.all()]
            print(f"ENUM_LABELS: {labels}")
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(check_enum())
