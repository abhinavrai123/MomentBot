# moment_flow.py

MOMENT_FLOW = [
    {
        "step": "select_log_type",
        "prompt": "What would you like to log?",
        "options": ["mood", "win", "need_learning", "gratitude"],
        "input_type": "choice",
        "next": "ask_energy_score"
    },
    {
        "step": "ask_energy_score",
        "prompt": "How would you rate your current energy level?",
        "options": ["++", "+", "0", "-", "--"],
        "input_type": "choice",
        "next": "select_cognitive_state"
    },
    {
        "step": "select_cognitive_state",
        "prompt": "Which cognitive state best describes this moment?",
        "options": ["act", "obs", "crt", "mtn"],
        "input_type": "choice",
        "next": "ask_comment"
    },
    {
        "step": "ask_comment",
        "prompt": "Optional: Describe your moment.\nYou can share emotional state, thoughts, or physical sensations.",
        "input_type": "text_optional",
        "next": "ask_trigger"
    },
    {
        "step": "ask_trigger",
        "prompt": "What triggered this moment? (Write freely)",
        "input_type": "text",
        "next": "store_entry"
    },
    {
        "step": "store_entry",
        "action": "store_to_db",
        "fields": [
            "log_type", "energy_score", "cognitive_state",
            "comment", "trigger", "timestamp"
        ],
        "next": "check_for_mood"
    },
    {
        "step": "check_for_mood",
        "condition": "log_type == 'mood'",
        "true_next": "process_mood_swing",
        "false_next": "end_flow"
    },
    {
        "step": "process_mood_swing",
        "action": "track_mood_swing",
        "next": "end_flow"
    },
    {
        "step": "end_flow",
        "prompt": "Your moment has been recorded. ✅",
        "input_type": "none"
    }
]
