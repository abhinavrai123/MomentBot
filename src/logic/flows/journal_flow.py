# journal_flow.py

JOURNAL_FLOW = [
    {
        "step": "ask_energy_score",
        "prompt": "How would you rate your energy level?",
        "options": ["++", "+", "0", "-", "--"],
        "input_type": "choice",
        "next": "store_journal_entry"
    },
    {
        "step": "store_journal_entry",
        "action": "store_journal_to_db",
        "fields": ["comment", "energy_score", "log_type", "timestamp"],
        "next": "end_flow"
    },
    {
        "step": "end_flow",
        "prompt": "📝 Journal entry recorded!",
        "input_type": "none"
    }
]
