# run_mood_swing_job.py

import asyncio
from src.logic.utils.swing_utils import process_mood_swings
from src.data.session import get_session
from src.data.models import MoodSwing

async def display_new_swing_summaries():
    async with get_session() as session:
        result = await session.execute(
            # Sort latest swings by creation time
            MoodSwing.__table__.select().order_by(MoodSwing.created_at.desc())
        )
        swings = result.fetchall()

        if not swings:
            print("❗ No mood swings found in the database.")
            return

        print(f"✅ Found {len(swings)} mood swing(s):\n")
        for row in swings:
            swing = row._mapping
            print(f"""
🌀 Swing ID: {swing['swing_id']}
User ID: {swing['user_id']}
Start: {swing['start_time']} → End: {swing['end_time']} ({swing['duration_minutes']} min)
Energy Path: {swing['energy_path']}
Volatility: {swing['swing_volatility']} | Adjusted: {swing['adjusted_volatility']}
Direction: {swing['direction']} | Avg Energy: {swing['avg_energy_level']}
Log IDs: {swing['log_ids']}
Created At: {swing['created_at']}
{'-' * 60}
""")

async def run_swing_job():
    try:
        print("🚀 Running mood swing processing job...\n")
        await process_mood_swings()
        print("\n✅ Mood swing detection completed.\n")
        await display_new_swing_summaries()
    except Exception as e:
        print(f"❌ Error during swing job: {e}")

if __name__ == "__main__":
    asyncio.run(run_swing_job())
