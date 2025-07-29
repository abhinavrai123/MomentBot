import asyncio
from comm.reports.daily_summary_service_html import send_manual_daily_summary_html

if __name__ == "__main__":
    user_id = 7017034983  # Replace with your test user's ID
    date_str = "2025-07-28"  # Replace with the date you want to test

    asyncio.run(send_manual_daily_summary_html(user_id, date_str))
