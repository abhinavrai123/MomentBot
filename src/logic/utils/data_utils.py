from sqlalchemy import select
from src.data.models import LogEntry
from src.data.session import get_session
from collections import defaultdict
from typing import List


async def get_all_user_ids():
    async with get_session() as session:
        stmt = select(LogEntry.user_id).distinct()
        result = await session.execute(stmt)
        return [row[0] for row in result.fetchall()]


def group_logs_by_user(logs: List[LogEntry]) -> dict[int, List[LogEntry]]:
    grouped = defaultdict(list)
    for log in logs:
        grouped[log.user_id].append(log)
    return grouped

from zoneinfo import ZoneInfo
from datetime import datetime

IST = ZoneInfo("Asia/Kolkata")

def create_synthetic_zero(user_id, last_log_time):
    # Step 1: Convert from UTC to IST
    last_log_ist = last_log_time.astimezone(IST)

    # Step 2: Set time to 10:00 PM IST
    synthetic_ist = last_log_ist.replace(hour=22, minute=0, second=0, microsecond=0)

    # Step 3: Convert back to UTC for storage
    synthetic_utc = synthetic_ist.astimezone(ZoneInfo("UTC"))

    return LogEntry(
        user_id=user_id,
        energy_score=0,
        log_type="mood",
        log_time=synthetic_utc,  # stored in UTC
        comment="(auto-appended 10pm reset)",
        evnttrigger="reset",
        swing_id=None,
    )
