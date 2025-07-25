# src/bot/prompts.py
from telegram.constants import ParseMode

def make_send_prompt_fn(application):
    from src.logic.utils.prompt_utils import build_prompt
    bot = application.bot  # ✅ Extract actual Bot instance

    async def send_prompt(user_id: int, intent: str, **kwargs):
        message = build_prompt(intent, **kwargs)
        try:
            await bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            print(f"❌ Failed to send prompt to {user_id}: {e}")

    return send_prompt
