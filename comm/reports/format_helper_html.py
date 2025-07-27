from collections import defaultdict
from comm.utils.timezone_utils import to_local_time
from src.config.constants import DailyRoutine

ENERGY_EMOJI_MAP = {
    2: "🌞", 1: "🙂", 0: "😌", -1: "☁️", -2: "🌧️",
}

SECTION_STYLE_MAP = {
    "journal": "#ffffff",
    "wins": "#ffffff",
    "reflection": "#ffffff",
    "moods": "#ffffff",
}

from datetime import datetime
summary_date = datetime.now().strftime("%B %d, %Y")


def wrap_text(text, max_words=12):
    words = text.split()
    lines = [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
    return "<br>".join(lines)


def format_section_1_journal_html(logs):
    routine_blocks = defaultdict(list)

    for log in logs:
        if log.log_type != "journal":
            continue
        routine_index = log.daily_routine
        routine = DailyRoutine.from_index(routine_index)
        label = routine.label() if routine else "Other"
        time_str = to_local_time(log.log_time).strftime("%-I:%M %p")
        energy = ENERGY_EMOJI_MAP.get(log.energy_score, "–")
        comment = wrap_text(log.comment or "")
        entry = f"<div class='entry-block'> • [{time_str}]{energy} {comment}</div>"
        routine_blocks[label].append(entry)

    blocks = []
    for block in DailyRoutine:
        label = block.label()
        if routine_blocks[label]:
            blocks.append(f"<u>{label}</u>")
            blocks.extend(routine_blocks[label])
    if routine_blocks["Other"]:
        blocks.append("<u>Other</u>")
        blocks.extend(routine_blocks["Other"])

    return f"""
    <div>{''.join(blocks)}</div>
    """


def format_section_2_wins_gratitude_html(logs):
    lines = []
    for log in logs:
        if log.log_type not in ("win", "gratitude"):
            continue
        emoji = "✅" if log.log_type == "win" else "🙏"
        time_str = to_local_time(log.log_time).strftime("%-I:%M %p")
        energy = ENERGY_EMOJI_MAP.get(log.energy_score, "–")
        cog = log.cog_state or "–"
        tag = log.raw_text or "–"
        trg = log.evnttrigger or "–"
        comment = wrap_text(log.comment or "")
        entry = f"<div class='entry-block'> • [{time_str}]{emoji} {energy} {comment} <br><i>(Cog: {cog}, Tag: {tag}, Trg: {trg})</i></div>"
        lines.append(entry)

    return f"""
    <div>{''.join(lines)}</div>
    """


def format_section_3_reflection_html(logs):
    routine_blocks = defaultdict(list)

    for log in logs:
        if log.log_type in ("win", "gratitude", "mood", "journal"):
            continue
        routine_index = getattr(log, "daily_routine", None)
        routine = DailyRoutine.from_index(routine_index)
        label = routine.label() if routine else "Other"
        time_str = to_local_time(log.log_time).strftime("%-I:%M %p")
        energy = ENERGY_EMOJI_MAP.get(log.energy_score, "–")
        comment = wrap_text(log.comment or "")
        cog = getattr(log, "cog_state", "–")
        tag = log.raw_text or "–"
        trg = getattr(log, "evnttrigger", "–")
        entry = f"<div class='entry-block'> • [{time_str}] {energy} {comment} <br><i>(Cog: {cog}, Tag: {tag}, Trg: {trg})</i></div>"
        routine_blocks[label].append(entry)

    blocks = []
    for block in DailyRoutine:
        label = block.label()
        if routine_blocks[label]:
            blocks.append(f"<u>{label}</u>")
            blocks.extend(routine_blocks[label])
    if routine_blocks["Other"]:
        blocks.append("<u>Other</u>")
        blocks.extend(routine_blocks["Other"])

    return f"""
    <div>{''.join(blocks)}</div>
    """


def format_section_4_moods_html(logs):
    lines = []
    for log in logs:
        if log.log_type != "mood":
            continue
        time_str = to_local_time(log.log_time).strftime("%-I:%M %p")
        energy = ENERGY_EMOJI_MAP.get(log.energy_score, "–")
        comment = wrap_text(log.comment or "")
        cog = log.cog_state or "–"
        tag = log.raw_text or "–"
        trg = log.evnttrigger or "–"
        entry = f"<div class='entry-block'> • [{time_str}] {energy} {comment} <br> <i>(Cog: {cog}, Tag: {tag}, Trg: {trg})</i></div>"
        lines.append(entry)

    return f"""
    <div>{''.join(lines)}</div>
    """


def build_html_body(summary_date: str, section_1: str, section_2: str, section_3: str, section_4: str) -> str:
    return f"""
<html>
  <head>
    <style>
      body {{
        background-color: #f4f4f4;
        font-family: Arial, sans-serif;
        padding: 40px 0;
      }}

      .email-container {{
        width: 100%;
        max-width: 550px;
        margin: 0 auto;
        background-color: #fcfcfc;
        border: 1px solid #ccc;
        padding: 24px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
      }}

      .section-wrapper {{
        margin-bottom: 32px;
      }}

      h2 {{
        font-size: 14px;  
        font-weight: italic;
        margin-bottom: 1px;
        margin-top: 1px;
        border-bottom: 1px solid #ddd;
        padding-bottom: 1px;
        text-align: left;
        color: #222;

      }}
    
    .sub-header {{
        font-size: 15px;
        font-weight: bold;
        color: #333;
        margin: 12px 0 6px 8px;
      }}
      .entry-block {{
        padding-left: 8px;
        margin-bottom: 0px;
      }}

      .time {{
        font-weight: bold;
        font-style: normal;
        margin-right: 6px;
      }}

      .emoji {{
        font-size: 16px;
        margin-right: 4px;
      }}

      .text {{
        display: inline-block;
        line-height: 1.4;
        word-break: normal;
        max-width: 100%;
        white-space: normal;
        text-align: justify;
      }}

      i {{
        font-style: italic;
        color: #444;
      }}

      u {{
        text-decoration: underline;
        font-weight: 600;
      }}

      @media only screen and (max-width: 600px) {{
        body {{
          padding: 20px 0;
        }}

        .email-container {{
          padding: 16px;
        }}

        h2 {{
          font-size: 18px;
        }}

        .entry-block {{
          font-size: 17px;
        }}
      }}
    </style>
  </head>
  <body>
    <div class="email-container">
      <div style="font-size: 20px; color: #666; text-align: center; margin-bottom: 24px;">
        📅 Summary for <b>{summary_date}</b>
      </div>

      <div class="section-wrapper">
        <h2>📝 Section 1: Daily Journal</h2>
        {section_1}
      </div>

      <div class="section-wrapper">
        <h2>🏆 Section 2: Wins & Gratitude</h2>
        {section_2}
      </div>

      <div class="section-wrapper">
        <h2>💭 Section 3: Daily Reflection</h2>
        {section_3}
      </div>

      <div class="section-wrapper">
        <h2>️ 💫Section 4: Moods</h2>
        {section_4}
      </div>
    </div>
  </body>
</html>
"""

