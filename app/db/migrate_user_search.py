import asyncio
from app.db.session import engine
from sqlalchemy import text

async def add_col():
    async with engine.begin() as conn:
        await conn.execute(text('ALTER TABLE user_searches ADD COLUMN IF NOT EXISTS last_full_scan_at TIMESTAMPTZ'))
    print("Column added successfully")

if __name__ == "__main__":
    asyncio.run(add_col())
