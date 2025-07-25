from enum import Enum
import pytz

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

# --- Daily Routine ---
class DailyRoutine(Enum):
    FOUNDATION = ("05:00", "08:00", "Foundation")
    LAUNCH = ("08:00", "10:00", "Launch")
    FOCUSED_AND_RESTED = ("10:00", "14:00", "Focused and Rested")
    AFTERNOON_FLOW = ("14:00", "17:30", "Afternoon Flow")
    COMMUNITY_EXPRESSION = ("17:30", "19:30", "Community / Expression")
    WINDDOWN_REFLECTION = ("19:30", "22:00", "Winddown / Reflection")

    def start_time(self):
        return self.value[0]

    def end_time(self):
        return self.value[1]

    def label(self):
        return self.value[2]

LOCAL_TIMEZONE = pytz.timezone("Asia/Kolkata")
WIN_GRATITUDE_CHECK_TIMES = ["12:00", "16:00"]