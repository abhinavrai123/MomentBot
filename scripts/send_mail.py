import asyncio
from comm.backup.daily_summary_service import send_manual_daily_summary

if __name__ == "__main__":
    user_id = 7017034983  # Replace with your test user's ID
    date_str = "2025-07-25"  # Replace with the date you want to test

    asyncio.run(send_manual_daily_summary(user_id, date_str))
