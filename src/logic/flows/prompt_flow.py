# prompt_flow.py

PROMPT_FLOW = [
    {
        "step": "check_missing_journal_log",
        "trigger": "daily_routine_end",  # Triggered at end of each DailyRoutine block
        "action": "check_log_entries",
        "log_types": ["mood", "journal"],
        "if_missing": {
            "next": "send_journal_prompt"
        },
        "next": "end_check"
    },
    {
        "step": "send_journal_prompt",
        "prompt": "No log/journal recorded. Let's add a moment?",
        "input_type": "none",
        "action": "send_prompt"
    },
    {
        "step": "check_win_gratitude_12pm",
        "trigger": "12:00",
        "action": "check_log_entries",
        "log_types": ["win", "gratitude"],
        "if_missing": {
            "next": "send_win_gratitude_prompt"
        },
        "next": "end_check"
    },
    {
        "step": "check_win_gratitude_4pm",
        "trigger": "16:00",
        "action": "check_log_entries",
        "log_types": ["win", "gratitude"],
        "if_missing": {
            "next": "send_win_gratitude_prompt"
        },
        "next": "end_check"
    },
    {
        "step": "send_win_gratitude_prompt",
        "prompt": "Let’s target a win and gratitude today?",
        "input_type": "none",
        "action": "send_prompt"
    },
    {
        "step": "end_check",
        "input_type": "none"
    }
]
