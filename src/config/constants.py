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
DAY_FIXED_DAY_START = ("5:00")
DAY_FIXED_BREAKFAST = ("9:00")
DAY_FIXED_LUNCH = ("11:30")
DAY_FIXED_TEA = ("15:30")
DAY_FIXED_DINNER = ("19:30")
DAY_FIXED_ACCOUNTS = ("19:00")
DAY_FIXED_REFLECTION_HOUR = ("20:00")
DAY_FIXED_NEXT_DAY_PREP = ("20:30")
DAY_FIXED_DAY_END = ("10:00")
WEEK_START = "SUNDAY"
WEEK_END = "SATURDAY"
WEEK_MID = "WEDNESDAY"

class DailyRoutine(Enum):
    FOUNDATION = ("05:00", "08:00", "Foundation", 0)
    LAUNCH = ("08:00", "10:00", "Launch", 1)
    FOCUSED_AND_RESTED = ("10:00", "14:00", "Focused and Rested", 2)
    AFTERNOON_FLOW = ("14:00", "17:30", "Afternoon Flow", 3)
    COMMUNITY_EXPRESSION = ("17:30", "19:30", "Community / Expression", 4)
    WINDDOWN_REFLECTION = ("19:30", "22:00", "Winddown / Reflection", 5)

    def start_time(self):
        return self.value[0]

    def end_time(self):
        return self.value[1]

    def label(self):
        return self.value[2]

    def index(self):
        return self.value[3]

    @classmethod
    def from_index(cls, idx: int):
        for routine in cls:
            if routine.index() == idx:
                return routine
        return None
LOCAL_TIMEZONE = pytz.timezone("Asia/Kolkata")
WIN_GRATITUDE_CHECK_TIMES = ["12:00", "16:00"]
