from datetime import datetime, time
import pytz
from src.config.constants import DailyRoutine

LOCAL_TIMEZONE = pytz.timezone("Asia/Kolkata")

def get_daily_routine_index(timestamp: datetime) -> int:
    # Ensure datetime is localized
    if timestamp.tzinfo is None:
        timestamp = pytz.utc.localize(timestamp)

    local_time = timestamp.astimezone(LOCAL_TIMEZONE).time()

    for index, routine in enumerate(DailyRoutine):
        start_hour, start_minute = map(int, routine.start_time().split(":"))
        end_hour, end_minute = map(int, routine.end_time().split(":"))

        start = time(start_hour, start_minute)
        end = time(end_hour, end_minute)

        if start <= local_time < end:
            return index  # Return routine index

    return -1
