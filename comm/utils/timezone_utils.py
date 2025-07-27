# comm/utils/timezone_utils.py

from datetime import datetime, timedelta, time,timezone
from zoneinfo import ZoneInfo
import pytz

LOCAL_TZ = ZoneInfo("Asia/Kolkata")  # Use your preferred timezone here


def to_local_time(dt_utc, tz_str="Asia/Kolkata"):
    if dt_utc.tzinfo is None:
        dt_utc = dt_utc.replace(tzinfo=timezone.utc)  # Ensure UTC awareness
    return dt_utc.astimezone(ZoneInfo(tz_str))

def format_time(utc_dt: datetime) -> str:
    """Format datetime to 'H:MM AM/PM' in local time."""
    return to_local_time(utc_dt).strftime('%-I:%M %p')

def get_today_bounds_in_utc(timezone_str: str):
    now_local = datetime.now(ZoneInfo(timezone_str))
    print(now_local)
    start_of_day_local = now_local.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day_local = start_of_day_local + timedelta(days=1)
    return start_of_day_local.astimezone(ZoneInfo("UTC")), end_of_day_local.astimezone(ZoneInfo("UTC"))

def get_utc_day_bounds_from_local_date(local_date):
    """
    Convert local date to UTC start and end datetime range.
    """
    tz = pytz.timezone(LOCAL_TIMEZONE)

    local_start = tz.localize(datetime.combine(local_date, time.min))  # 00:00 local
    local_end = tz.localize(datetime.combine(local_date, time.max))    # 23:59:59.999999 local

    utc_start = local_start.astimezone(pytz.utc)
    utc_end = local_end.astimezone(pytz.utc)

    return utc_start, utc_end