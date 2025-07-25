{
    "step": "check_mood_swing",
    "trigger": "20:00",
    "action": "analyze_mood_swing",
    "log_types": ["mood", "cog", "win", "gratitude", "need_learning"],
    "next": "send_mood_swing_summary"
},
{
    "step": "send_mood_swing_summary",
    "prompt": "mood_swing_summary",  # special type, resolved dynamically by system
    "input_type": "none",
    "action": "send_prompt"
}
