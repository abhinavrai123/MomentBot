import asyncio
from src.data.models import MoodSwing, LogEntry
from src.logic.utils.swing_utils import compute_adjusted_volatility
from src.data.session import get_session
from sqlalchemy import select

async def recalculate_all_adjusted_volatilities():
    async with get_session() as session:
        all_swings = await session.execute(
            select(MoodSwing)
        )
        swings = all_swings.scalars().all()

        for swing in swings:
            log_ids = [int(id.strip()) for id in swing.log_ids.split(",") if id.strip().isdigit()]
            log_result = await session.execute(
                select(LogEntry).where(LogEntry.log_id.in_(log_ids)).order_by(LogEntry.log_time)
            )
            logs = log_result.scalars().all()
            new_value = compute_adjusted_volatility(logs)
            print(f"Recalculating swing {swing.swing_id}: New volatility = {new_value}")
            swing.adjusted_volatility = new_value

        await session.commit()

if __name__ == "__main__":
    asyncio.run(recalculate_all_adjusted_volatilities())
