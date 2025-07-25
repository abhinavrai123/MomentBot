from datetime import datetime
from uuid import uuid4
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from src.data.models import LogEntry, MoodSwing
from src.data.session import get_session
from src.logic.utils.time_utils import get_daily_routine_index
from src.logic.utils.swing_utils import detect_swings, create_mood_swing_entry


async def store_log_entry(
    user_id: int,
    log_type: str,
    energy_score: int,
    comment: str,
    evnttrigger: str,
    timestamp: datetime,
    cognitive_state: str,
    raw_text: str
):
    """
    Store a general log entry and immediately run mood swing detection.
    Journal-style entries should use `store_journal_entry()` instead.
    """
    routine_index = get_daily_routine_index(timestamp)

    async with get_session() as session:
        try:
            # 1. Create and persist the new log entry
            new_entry = LogEntry(
                user_id=user_id,
                log_type=log_type,
                energy_score=energy_score,
                comment=comment,
                evnttrigger=evnttrigger,
                log_time=timestamp,
                cog_state=cognitive_state,
                daily_routine=routine_index,
                raw_text=raw_text
            )
            session.add(new_entry)
            await session.commit()

            # 2. Fetch all energy logs
            result = await session.execute(
                select(LogEntry)
                .where(LogEntry.user_id == user_id)
                .order_by(LogEntry.log_time)
            )
            all_logs = result.scalars().all()
            energy_logs = [log for log in all_logs if log.energy_score is not None]

            # 3. Detect and store new swings
            swings = detect_swings(energy_logs)
            for swing_logs in swings:
                swing_entry = create_mood_swing_entry(user_id, swing_logs)
                session.add(swing_entry)

            if swings:
                await session.commit()

        except SQLAlchemyError as e:
            await session.rollback()
            raise e


async def store_journal_entry(
    user_id: int,
    log_type: str,
    energy_score: int,
    comment: str,
    timestamp: datetime
):
    """
    Store a journal-style entry (e.g. gratitude, reflection).
    Does NOT trigger swing logic.
    """
    routine_index = get_daily_routine_index(timestamp)

    async with get_session() as session:
        try:
            entry = LogEntry(
                user_id=user_id,
                log_type=log_type,
                energy_score=energy_score,
                comment=comment,
                evnttrigger=None,
                log_time=timestamp,
                daily_routine=routine_index,
            )
            session.add(entry)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
