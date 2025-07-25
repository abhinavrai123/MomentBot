# scripts/init_db.py


import sys
from pathlib import Path

# Add project root (MomentBot/) to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import asyncio
from src.data.database import async_engine, Base
from src.data.models import LogEntry, MoodSwing

async def init():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # optional: clear old tables
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Fresh database initialized!")

if __name__ == "__main__":
    asyncio.run(init())
