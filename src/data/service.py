from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from src.data.models import LogEntry
from src.data.session import get_session  # async session provider
from datetime import datetime

async def store_log_entry(user_id: int, log_type: str, energy_score: int, comment: str, evnttrigger: str, timestamp: datetime ,cognitive_state: str):
    """Persist log entry to database using AsyncSession."""
    async with get_session() as session:
        try:
            entry = LogEntry(
                user_id=user_id,
                log_type=log_type,
                energy_score=energy_score,
                comment=comment,
                evnttrigger=evnttrigger,
                log_time=timestamp,
                cog_state=cognitive_state
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
    async with get_session() as session:
        try:
            entry = LogEntry(
                user_id=user_id,
                log_type=log_type,
                energy_score=energy_score,
                comment=comment,
                evnttrigger=None,
                log_time=timestamp
            )
            session.add(entry)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()