from comm.comm_link.email_sender_html import send_email_html
from comm.reports.format_helper_html import (
    summary_date,
    format_section_1_journal_html,
    format_section_2_wins_gratitude_html,
    format_section_3_reflection_html,
    format_section_4_moods_html,
    build_html_body  # NEW: import the final wrapper
)
from src.data.models import LogEntry
from src.data.session import get_session
from sqlalchemy import select, and_
from datetime import datetime, time, timezone
from zoneinfo import ZoneInfo
from sqlalchemy.ext.asyncio import AsyncSession

async def send_manual_daily_summary_html(user_id: int, date_str: str):
    """
    date_str is assumed to be in YYYY-MM-DD format and in local time (Asia/Kolkata).
    This function converts that to UTC, then fetches logs in that range.
    """
    local_tz = ZoneInfo("Asia/Kolkata")

    # Convert date string to datetime range in local time
    local_date = datetime.fromisoformat(date_str).date()
    local_start = datetime.combine(local_date, time.min).replace(tzinfo=local_tz)
    local_end = datetime.combine(local_date, time.max).replace(tzinfo=local_tz)

    # Convert to UTC
    utc_start = local_start.astimezone(timezone.utc)
    utc_end = local_end.astimezone(timezone.utc)

    # Fetch logs
    async with get_session() as session:  # type: AsyncSession
        result = await session.execute(
            select(LogEntry).where(
                and_(
                    LogEntry.user_id == user_id,
                    LogEntry.log_time >= utc_start,
                    LogEntry.log_time <= utc_end
                )
            )
        )
        logs = result.scalars().all()

        if not logs:
            print(f"[INFO] No logs found for user {user_id} on {date_str}")
            return

        # Format sections
        section0 = summary_date
        section2 = format_section_2_wins_gratitude_html(logs)
        section1 = format_section_1_journal_html(logs)
        section3 = format_section_3_reflection_html(logs)
        section4 = format_section_4_moods_html(logs)

        full_html = build_html_body(section0, section2, section1, section3, section4)
        subject = f"Daily Summary – {date_str}"

        # Send email
        send_email_html(to_email="abhinavrai123@gmail.com", subject=subject, body=full_html)
        print(f"[SUCCESS] Sent daily summary to user {user_id} for {date_str}")
