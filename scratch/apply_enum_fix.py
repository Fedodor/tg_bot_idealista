import asyncio
from app.db.session import AsyncSessionFactory
from sqlalchemy import text

async def fix_enum():
    async with AsyncSessionFactory() as session:
        try:
            # We must use separate transactions or ensure no other transaction is open for ALTER TYPE ADD VALUE
            # actually postgres allows it but not inside a block if it's the only command.
            # However, for simplicity using distinct calls.
            await session.execute(text("ALTER TYPE listing_rental_type_enum ADD VALUE IF NOT EXISTS 'PENTHOUSE'"))
            await session.execute(text("ALTER TYPE listing_rental_type_enum ADD VALUE IF NOT EXISTS 'HOUSE'"))
            await session.execute(text("ALTER TYPE listing_rental_type_enum ADD VALUE IF NOT EXISTS 'CHALET'"))
            await session.commit()
            print("ENUMS_FIXED")
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(fix_enum())
