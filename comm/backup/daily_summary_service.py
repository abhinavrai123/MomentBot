from comm.backup.email_sender import send_email
from comm.backup.format_helper import (
    format_section_1_journal,
    format_section_2_wins_gratitude,
    format_section_3_reflection,
    format_section_4_moods_html
)
from sqlalchemy.ext.asyncio import AsyncSession

from zoneinfo import ZoneInfo
from datetime import datetime, time, timezone
from sqlalchemy import select, and_
from src.data.models import LogEntry
from src.data.session import get_session

async def send_manual_daily_summary(user_id: int, date_str: str):
    """
    date_str is assumed to be in YYYY-MM-DD format and in local time (Asia/Kolkata).
    This function converts that to UTC, then fetches logs in that range.
    """
    local_tz = ZoneInfo("Asia/Kolkata")

    # Parse the local date string into a datetime.date object
    local_date = datetime.fromisoformat(date_str).date()

    # Define start and end of the day in local time
    local_start = datetime.combine(local_date, time.min).replace(tzinfo=local_tz)
    local_end = datetime.combine(local_date, time.max).replace(tzinfo=local_tz)

    # Convert local time bounds to UTC
    utc_start = local_start.astimezone(timezone.utc)
    utc_end = local_end.astimezone(timezone.utc)

    # Query logs within that UTC range
    async with get_session() as session:  # type: AsyncSession
        log_result = await session.execute(
            select(LogEntry).where(
                and_(
                    LogEntry.user_id == user_id,
                    LogEntry.log_time >= utc_start,
                    LogEntry.log_time <= utc_end
                )
            )
        )
        logs = log_result.scalars().all()

        if not logs:
            print(f"[INFO] No logs found for user {user_id} on {date_str}")
            return

        # Process logs (e.g. call formatter or sender here)
        # await send_summary_email(logs)
        # Format sections
        section1 = format_section_1_journal(logs)
        section2 = format_section_2_wins_gratitude(logs)
        section3 = format_section_3_reflection(logs)
        section4 = format_section_4_moods_html(logs)

        email_body = "\n\n".join([section1, section2, section3, section4])
        subject = f" Daily Summary – {date_str}"

        # Send the email
        send_email(to_email="abhinavrai123@gmail.com", subject=subject, body=email_body)
        print(f"[SUCCESS] Sent daily summary to user {user_id} for {date_str}")
