# src/scheduler/scheduler_swing.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from src.logic.utils.swing_utils import process_mood_swings

scheduler = AsyncIOScheduler()

def scheduler_swing(app):
    async def post_init(application):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(
            process_mood_swings,
            CronTrigger(hour=20, minute=0),  # 🕗 Every day at 8:00 PM local
            name="Daily Mood Swing Processor"
        )
        scheduler.start()
        print("🧠 Swing scheduler started.")

    app.post_init = post_init