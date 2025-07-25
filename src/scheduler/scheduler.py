# src/scheduler/scheduler.py

import asyncio
from datetime import datetime
from src.logic.utils.data_utils import get_all_user_ids
from src.config.constants import LOCAL_TIMEZONE, DailyRoutine, WIN_GRATITUDE_CHECK_TIMES
from src.logic.utils.time_prompt_utils import get_routine_time_range, has_logs_in_range
from src.bot.prompts import make_send_prompt_fn

async def run_scheduler(send_prompt_fn):
    print("⏰ Scheduler started.")
    while True:
        now = datetime.now(LOCAL_TIMEZONE)
        current_time_str = now.strftime("%H:%M")
        user_ids = await get_all_user_ids()

        # Check routine end times
        for routine in DailyRoutine:
            if current_time_str == routine.end_time():
                start, end = get_routine_time_range(routine)
                print(f"🔍 [{current_time_str}] Checking logs for routine: {routine.label()}")

                for user_id in user_ids:
                    has_logs = await has_logs_in_range(user_id, [], start, end)
                    if not has_logs:
                        print(f"📩 [PROMPT] {user_id} missing log for {routine.label()}")
                        await send_prompt_fn(
                            user_id,
                            intent="missing_log",
                            routine=routine
                        )

        # Check win + gratitude
        if current_time_str in WIN_GRATITUDE_CHECK_TIMES:
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            for user_id in user_ids:
                has_win = await has_logs_in_range(user_id, ["win"], start_of_day, now)
                has_gratitude = await has_logs_in_range(user_id, ["gratitude"], start_of_day, now)

                if not has_win or not has_gratitude:
                    print(f"📩 [PROMPT] {user_id} missing win/gratitude")
                    await send_prompt_fn(
                        user_id,
                        intent="missing_win_gratitude"
                    )

        await asyncio.sleep(60 - datetime.now().second)

def prompt_scheduler(app):
    async def post_init(application):
        send_prompt_fn = make_send_prompt_fn(application)
        asyncio.create_task(run_scheduler(send_prompt_fn))
        print("🧠 Scheduler background task attached.")
    app.post_init = post_init
