from collections import defaultdict
from comm.utils.timezone_utils import *
from src.config.constants import DailyRoutine
from collections import defaultdict
from collections import defaultdict

ENERGY_EMOJI_MAP = {
    2: "🌞",   # ++
    1: "🙂",   # +
    0: "😌",   # 0
   -1: "☁️",   # -
   -2: "🌧️",  # --
}

def format_section_1_journal(logs):
    section = ["**📝 Section 1: Daily Journal**"]
    routine_blocks = defaultdict(list)

    for log in logs:
        if log.log_type != "journal":
            continue  # Skip non-journal entries

        routine_index = log.daily_routine  # assumes column name is `routine_block`
        energy_e = ENERGY_EMOJI_MAP.get(log.energy_score, "–")
        routine = DailyRoutine.from_index(routine_index)
        label = routine.label() if routine else "Other"
        time_str = to_local_time(log.log_time).strftime("%-I:%M %p")
        entry = f"• [{time_str}] {energy_e} {log.comment}"
        routine_blocks[label].append(entry)

    for block in DailyRoutine:
        label = block.label()
        if routine_blocks[label]:
            section.append(f"\n{label}")
            section.extend(routine_blocks[label])

    # Add "Other" entries if any
    if routine_blocks["Other"]:
        section.append("\nOther")
        section.extend(routine_blocks["Other"])

    return "\n".join(section)

def format_section_2_wins_gratitude(logs):
    section = ["🏆 **Section 2: Wins & Gratitude**"]

    for log in logs:
        if log.log_type not in ("win", "gratitude"):
            continue

        emoji = "✅" if log.log_type == "win" else "🙏"
        dt = log.log_time
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            dt = to_local_time(dt)
        time_str = to_local_time(log.log_time).strftime("%-I:%M %p")
        energy_e = ENERGY_EMOJI_MAP.get(log.energy_score, "–")
        cog = log.cog_state or "–"
        tag = log.raw_text or "–"
        trigger = log.evnttrigger or "–"

        entry = f"• [{time_str}] {emoji} {energy_e} {log.comment} (Cog: {cog}, Tag: {tag}, Trg: {trigger})"
        section.append(entry)

    return "\n".join(section)

def format_section_3_reflection(logs):
    section = ["**💭 Section 3: Daily Reflection**"]
    routine_blocks = defaultdict(list)

    for log in logs:
        if log.log_type in ("win", "gratitude", "mood", "journal"):
            continue  # exclude these

        routine_index = getattr(log, "daily_routine", None)
        routine = DailyRoutine.from_index(routine_index)
        label = routine.label() if routine else "Other"
        time_str = to_local_time(log.log_time).strftime("%-I:%M %p")
        energy_e = ENERGY_EMOJI_MAP.get(log.energy_score, "–")
        tag = log.raw_text or "–"
        cog = getattr(log, "cog_state", "")
        trigger = getattr(log, "evnttrigger", "")
        comment = log.comment or ""

        entry = f"• [{time_str}] {energy_e} {comment} (Cog: {cog}, Tag: {tag} Trg: {trigger})"
        routine_blocks[label].append(entry)

    for block in DailyRoutine:
        label = block.label()
        if routine_blocks[label]:
            section.append(f"\n{label}")
            section.extend(routine_blocks[label])

    if routine_blocks["Other"]:
        section.append("\nOther")
        section.extend(routine_blocks["Other"])

    return "\n".join(section)

from comm.utils.timezone_utils import to_local_time

def format_section_4_moods_html(logs):
    section = ["🌡️ Section 4: Moods"]

    for log in logs:
        if log.log_type != "mood":
            continue

        time_str = to_local_time(log.log_time).strftime("%-I:%M %p")
        cog = log.cog_state or "–"
        energy_e = ENERGY_EMOJI_MAP.get(log.energy_score, "–")
        tag = log.raw_text or "–"
        trigger = log.evnttrigger or "–"
        comment = log.comment or "–"

        entry = (
            f"• [{time_str}] {energy_e} {comment} "
            f"(Cog: {cog}, Tag: {tag}, Trg: {trigger})"
        )
        section.append(entry)

    return "\n".join(section)

