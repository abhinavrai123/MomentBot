from src.config.constants import DailyRoutine

def build_prompt(intent: str, **kwargs) -> str:
    if intent == "missing_log":
        routine: DailyRoutine = kwargs.get("routine")
        return f"🕓 No log/journal recorded during *{routine.label()}*. Let's add a moment?"

    elif intent == "missing_win_gratitude":
        return "✨ Let’s target for a win and a gratitude entry?"

    else:
        return "⏰ Just checking in. How’s your day going?"
