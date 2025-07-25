# Task utilities
from datetime import datetime
from zoneinfo import ZoneInfo
from src.config.constants import (
    ENERGY_LEVELS,
    ENERGY_LEVEL_SYMBOLS,
    DEFAULT_TIMEZONE,
    LogType,
    EnergyLevel,
    CognitiveState,
    EMOJI_MAP
)
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup


# --- ENERGY UTILS ---

def get_energy_numeric(symbol: str) -> int:
    return ENERGY_LEVELS.get(symbol, 0)

def get_energy_symbol(score: int) -> str:
    return ENERGY_LEVEL_SYMBOLS.get(score, "0")

def is_energy_level_valid(symbol: str) -> bool:
    return symbol in ENERGY_LEVELS

def format_energy_label(symbol: str) -> str:
    emoji = EMOJI_MAP.get(symbol, "")
    return f"{emoji} {symbol}"


# --- TIME UTILS ---

def get_current_timestamp(tz_name: str = DEFAULT_TIMEZONE) -> str:
    return datetime.now(ZoneInfo(tz_name)).isoformat()


# --- LOGIC UTILS ---

def is_valid_log_type(log_type: str) -> bool:
    return log_type in [lt.value for lt in LogType]

def is_mood_log(log_type: str) -> bool:
    return log_type == LogType.MOOD.value


# --- TEXT SANITIZERS ---

def clean_text_input(text: str) -> str:
    return text.strip() if text else ""

def normalize_trigger(text: str) -> str:
    return text.lower().strip()


# --- LOGGING HELPERS ---

logger = logging.getLogger("momentbot")

def log_info(message: str):
    logger.info(f"[MomentBot] {message}")

def log_error(message: str):
    logger.error(f"[MomentBot] {message}")

def log_debug(message: str):
    logger.debug(f"[MomentBot] {message}")


# --- BUTTON HELPERS ---

def build_choice_buttons(options: list[str], row_width: int = 2) -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(text=o, callback_data=o) for o in options]
    rows = [buttons[i:i+row_width] for i in range(0, len(buttons), row_width)]
    return InlineKeyboardMarkup(rows)

def build_energy_buttons() -> InlineKeyboardMarkup:
    return build_choice_buttons(list(ENERGY_LEVELS.keys()))

def build_cognitive_state_buttons() -> InlineKeyboardMarkup:
    return build_choice_buttons([cs.value for cs in CognitiveState])

#REPLY KEYBOARD
def build_reply_keyboard(options: list[str], one_time: bool = True) -> ReplyKeyboardMarkup:
    """Returns a simple ReplyKeyboardMarkup with each option on its own row."""
    keyboard = [[opt] for opt in options]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=one_time
    )


