from sqlalchemy import select
from src.data.models import LogEntry
from src.data.session import get_session

async def get_all_user_ids():
    async with get_session() as session:
        stmt = select(LogEntry.user_id).distinct()
        result = await session.execute(stmt)
        return [row[0] for row in result.fetchall()]