import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.data.session import  get_session  # whatever you're importing
from src.data.models import MoodSwing
from sqlalchemy import select

async def deduplicate_swings():
    async with get_session() as session:
        result = await session.execute(select(MoodSwing))
        swings = result.scalars().all()

        grouped = {}
        for swing in swings:
            key = tuple(sorted(map(int, swing.log_ids.split(','))))
            grouped.setdefault(key, []).append(swing)

        for swings in grouped.values():
            if len(swings) <= 1:
                continue
            swings.sort(key=lambda s: (s.duration_minutes, s.created_at), reverse=True)
            best = swings[0]
            for dup in swings[1:]:
                await session.delete(dup)
            print(f"Kept {best.swing_id}, removed {len(swings)-1} duplicates")

        await session.commit()

if __name__ == "__main__":
    asyncio.run(deduplicate_swings())
