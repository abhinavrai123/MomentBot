# src/utils/time_prompt_utils.py

from datetime import datetime, time, timedelta
from sqlalchemy import select, or_
from src.data.models import LogEntry
from src.config.constants import DailyRoutine, LOCAL_TIMEZONE
from src.data.session import get_session

def get_routine_time_range(routine: DailyRoutine):
    """Return localized datetime start and end for a DailyRoutine block for today."""
    now = datetime.now(LOCAL_TIMEZONE)
    start_hour, end_hour = routine.start_time(), routine.end_time()

    start = datetime.combine(now.date(), time.fromisoformat(start_hour)).astimezone(LOCAL_TIMEZONE)
    end = datetime.combine(now.date(), time.fromisoformat(end_hour)).astimezone(LOCAL_TIMEZONE)

    return start, end

def is_current_time_after(time_str: str) -> bool:
    """Check if current time is after a specific HH:MM string (e.g., '12:00')."""
    now = datetime.now(LOCAL_TIMEZONE).time()
    target = time.fromisoformat(time_str)
    return now >= target

async def has_logs_in_range(user_id: int, log_types: list[str], start: datetime, end: datetime) -> bool:
    """Check if any logs exist in the given time window for the user and given log types."""
    async with get_session() as session:
        stmt = select(LogEntry).where(
            LogEntry.user_id == user_id,
            LogEntry.log_type.in_(log_types),
            LogEntry.log_time >= start,
            LogEntry.log_time < end
        )
        result = await session.execute(stmt)
        return result.first() is not None
