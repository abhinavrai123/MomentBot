# constants.py

# --- Energy Levels ---
ENERGY_LEVELS = {
    "++": 2,
    "+": 1,
    "0": 0,
    "-": -1,
    "--": -2,
}

ENERGY_LEVEL_SYMBOLS = {
    2: "++",
    1: "+",
    0: "0",
    -1: "-",
    -2: "--"
}

# --- Cognitive States ---
COGNITIVE_STATES = ["Act", "Obs", "Crt", "Mtn"]

# --- Log Types ---
LOG_TYPES = ["log", "mood", "acmp", "thank"]  # <-- "acc" changed to "acmp"

# --- Accomplishment Types ---
ACMP_TYPES = ["win", "learn"]  # renamed for consistency

# --- Time Constants ---
RESET_HOUR = 20  # 8 PM
DEFAULT_TIMEZONE = "UTC"  # Adjustable if needed

# --- Swing Logic ---
MOOD_LOG_TYPE = "mood"  # Only mood entries are used for swings
DEFAULT_ENERGY = 0

# --- Emojis (Optional UI enhancement) ---
EMOJI_MAP = {
    "++": "🌞",
    "+": "🙂",
    "0": "😐",
    "-": "😟",
    "--": "🌧️",
    "win": "🏆",
    "learn": "📘"
}

# --- Swing Summary Format ---
SWING_SUMMARY_TEMPLATE = "{index}. {path} (lasted {duration})"
