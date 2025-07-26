from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from src.data.models import LogEntry
from src.data.session import get_session
from src.logic.utils.time_utils import get_daily_routine_index


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
    Store a general log entry. Mood swings are processed separately by scheduler.
    """
    routine_index = get_daily_routine_index(timestamp)

    async with get_session() as session:
        try:
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
