from datetime import datetime
from src.config.constants import LOCAL_TIMEZONE
from src.data.models import LogEntry

# Simulated base date: July 28, 2025
base_date = datetime(2025, 7, 28, tzinfo=LOCAL_TIMEZONE)

sample_logs = [
    LogEntry(
        log_id=1,
        user_id=1,
        log_type="mood",
        cog_state=None,
        comment="Feeling okay this morning",
        energy_score=0,
        log_time=base_date.replace(hour=8, minute=0),
        log_day=base_date.date(),
        evnttrigger="woke up",
        daily_routine=1,
        raw_text="Feeling okay this morning",
    ),
    LogEntry(
        log_id=2,
        user_id=1,
        log_type="mood",
        cog_state=None,
        comment="Motivated after planning the day",
        energy_score=1,
        log_time=base_date.replace(hour=9, minute=30),
        log_day=base_date.date(),
        evnttrigger="planning",
        daily_routine=2,
        raw_text="Motivated after planning the day",
    ),
    LogEntry(
        log_id=3,
        user_id=1,
        log_type="mood",
        cog_state=None,
        comment="A little overwhelmed by tasks",
        energy_score=-1,
        log_time=base_date.replace(hour=15, minute=0),
        log_day=base_date.date(),
        evnttrigger="workload",
        daily_routine=4,
        raw_text="A little overwhelmed by tasks",
    ),
    LogEntry(
        log_id=4,
        user_id=1,
        log_type="mood",
        cog_state=None,
        comment="Still not back to balance",
        energy_score=-2,
        log_time=base_date.replace(hour=18, minute=30),
        log_day=base_date.date(),
        evnttrigger="missed break",
        daily_routine=5,
        raw_text="Still not back to balance",
    )
]
