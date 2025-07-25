from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from src.data.models import LogEntry, MoodSwing
from src.data.session import get_session  # async session provider
from datetime import datetime
from src.logic.utils.time_utils import get_daily_routine_index
from src.logic.utils.swing_utils import detect_swings, create_mood_swing_entry

async def store_log_entry(user_id: int, log_type: str, energy_score: int, comment: str, evnttrigger: str, timestamp: datetime ,cognitive_state: str):
    """Persist log entry to database using AsyncSession."""
    routine_index = get_daily_routine_index(timestamp)
    async with get_session() as session:
        try:
            entry = LogEntry(
                user_id=user_id,
                log_type=log_type,
                energy_score=energy_score,
                comment=comment,
                evnttrigger=evnttrigger,
                log_time=timestamp,
                cog_state=cognitive_state,
                daily_routine = routine_index
            )
            session.add(entry)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

async def store_journal_entry(user_id: int, log_type: str, energy_score: int, comment: str, timestamp: datetime):
    """Persist journal entry to database using AsyncSession."""
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
                daily_routine = routine_index
            )
            session.add(entry)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

async def store_user_swings(user_id: int, logs: list, db_session: AsyncSession):
    """
    Detects and stores mood swings from user's mood logs.
    Assumes logs are already filtered to mood type and sorted by time.
    """
    swings = detect_swings(logs)

    for swing_logs in swings:
        swing_entry = create_mood_swing_entry(user_id, swing_logs)  # ✅ sync function
        db_session.add(swing_entry)

    await db_session.commit()