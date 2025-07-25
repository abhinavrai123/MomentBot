from enum import Enum

# --- Energy Levels ---
class EnergyLevel(Enum):
    HIGH = "++"
    MEDIUM = "+"
    NEUTRAL = "0"
    LOW = "-"
    DRAINED = "--"

ENERGY_LEVELS = {
    EnergyLevel.HIGH.value: 2,
    EnergyLevel.MEDIUM.value: 1,
    EnergyLevel.NEUTRAL.value: 0,
    EnergyLevel.LOW.value: -1,
    EnergyLevel.DRAINED.value: -2,
}

ENERGY_LEVEL_SYMBOLS = {v: k for k, v in ENERGY_LEVELS.items()}

# --- Log Types ---
class LogType(Enum):
    MOOD = "mood"
    COGNITIVE = "cognitive_state"
    WIN = "win"
    LEARNING = "need_learning"
    GRATITUDE = "gratitude"

    @classmethod
    def has_value(cls, value):
        return value in (item.value for item in cls)

# --- Cognitive States ---
class CognitiveState(Enum):
    ACT = "act"
    OBSERVE = "obs"
    CREATE = "crt"
    MOTION = "mtn"

# --- Constants ---
RESET_HOUR = 20  # 8 PM
DEFAULT_TIMEZONE = "UTC"

DEFAULT_ENERGY = 0
MOOD_LOG_TYPE = LogType.MOOD.value  # used in mood swing tracking

# --- Emoji UI (optional) ---
EMOJI_MAP = {
    "++": "🌞",
    "+": "🙂",
    "0": "😐",
    "-": "😟",
    "--": "🌧️",
    "win": "🏆",
    "need_learning": "📘",
    "gratitude": "🙏",
    "mood": "🌀",
    "cognitive_state": "🧠",
}

# --- Swing Summary Format ---
SWING_SUMMARY_TEMPLATE = "{index}. {path} (lasted {duration})"
