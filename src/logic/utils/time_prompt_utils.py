# src/utils/time_prompt_utils.py

from datetime import datetime, time, timedelta
from sqlalchemy import select, or_
from src.data.models import LogEntry
from src.config.constants import DailyRoutine, LOCAL_TIMEZONE
from src.data.session import get_session

from datetime import datetime, time
from zoneinfo import ZoneInfo
from src.config.constants import LOCAL_TIMEZONE

def get_routine_time_range(routine: DailyRoutine):
    """Return UTC datetime start and end for a DailyRoutine block for today."""
    local_now = datetime.now(LOCAL_TIMEZONE)
    date_today = local_now.date()

    start_local = datetime.combine(date_today, time.fromisoformat(routine.start_time())).replace(tzinfo=LOCAL_TIMEZONE)
    end_local = datetime.combine(date_today, time.fromisoformat(routine.end_time())).replace(tzinfo=LOCAL_TIMEZONE)

    start_utc = start_local.astimezone(ZoneInfo("UTC"))
    end_utc = end_local.astimezone(ZoneInfo("UTC"))

    return start_utc, end_utc

def is_current_time_after(time_str: str) -> bool:
    """Check if current time is after a specific HH:MM string (e.g., '12:00')."""
    now = datetime.now(LOCAL_TIMEZONE).time()
    target = time.fromisoformat(time_str)
    return now >= target

async def has_logs_in_range(user_id: int, log_types: list[str], start: datetime, end: datetime) -> bool:
    """Check if any logs exist in the given time window for the user and given log types."""
    async with get_session() as session:
        print("Checking logs for user:", user_id)
        print("Log types:", log_types)
        print("Start:", start)
        print("End:", end)
        print("Timezone info:", start.tzinfo, end.tzinfo)
        stmt = select(LogEntry).where(
            LogEntry.user_id == user_id,
            LogEntry.log_type.in_(log_types),
            LogEntry.log_time >= start,
            LogEntry.log_time < end
        )
        result = await session.execute(stmt)
        return result.first() is not None
