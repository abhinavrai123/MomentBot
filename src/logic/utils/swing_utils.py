from datetime import datetime
from src.config.constants import LOCAL_TIMEZONE
from src.data.models import MoodSwing
from uuid import uuid4

ENERGY_WEIGHTS = {
    -2: 2,
    -1: 1,
     0: 0,
     1: 1,
     2: 2
}


def detect_swings(logs):
    """
    Given a list of logs (sorted by time), detect energy swings from 0 → ... → 0.
    Only valid if it starts and ends on 0.
    Ignores 0 → 0 sequences.
    """
    swings = []
    current_swing = []
    in_swing = False

    for log in logs:
        score = log.energy_score
        if score is None:
            continue

        if score == 0:
            if in_swing:
                current_swing.append(log)
                swings.append(current_swing)
                current_swing = []
                in_swing = False
            else:
                continue  # Ignore 0 → 0
        else:
            if not in_swing:
                in_swing = True
                current_swing = []
            current_swing.append(log)

    return swings


def compute_adjusted_volatility(swing_logs):
    total_weighted_energy = 0
    total_transitions = len(swing_logs) - 1
    if total_transitions == 0:
        return 0.0

    for i in range(len(swing_logs) - 1):
        a, b = swing_logs[i], swing_logs[i + 1]

        # Convert both to same tz-aware datetime
        a_time = a.log_time
        b_time = b.log_time

        # If naive, localize them to LOCAL_TIMEZONE
        if a_time.tzinfo is None:
            a_time = a_time.replace(tzinfo=LOCAL_TIMEZONE)
        if b_time.tzinfo is None:
            b_time = b_time.replace(tzinfo=LOCAL_TIMEZONE)

        minutes = (b_time - a_time).total_seconds() / 60
        energy = abs(ENERGY_WEIGHTS.get(a.energy_score, 0))
        total_weighted_energy += energy * minutes

            return round((total_weighted_energy / 60) * 100, 2)

def determine_direction(energy_path):
    ups = sum(1 for e in energy_path if "+" in e)
    downs = sum(1 for e in energy_path if "-" in e)

    if ups > downs:
        return "upward"
    elif downs > ups:
        return "downward"
    else:
        return "mixed"


def parse_energy_label(score):
    match score:
        case 2: return "++"
        case 1: return "+"
        case -1: return "-"
        case -2: return "--"
        case 0: return "0"
        case _: return "?"

def create_mood_swing_entry(user_id: int, swing_logs: list) -> MoodSwing:
    """
    Constructs a MoodSwing ORM object from a list of log entries (forming a swing).
    All time-based calculations are done in LOCAL_TIMEZONE.
    """
    start = swing_logs[0].log_time.astimezone(LOCAL_TIMEZONE)
    end = swing_logs[-1].log_time.astimezone(LOCAL_TIMEZONE)
    duration = int((end - start).total_seconds() / 60)

    energy_path = " , ".join(parse_energy_label(log.energy_score) for log in swing_logs)
    energy_scores = [log.energy_score for log in swing_logs if log.energy_score is not None]

    max_intensity = max(abs(s) for s in energy_scores)
    swing_volatility = len([s for s in energy_scores if s != 0])
    avg_energy = round(sum(energy_scores) / len(energy_scores), 2)
    adjusted_vol = compute_adjusted_volatility(swing_logs)
    direction = determine_direction(energy_path.split(" , "))
    transitions = len(swing_logs) - 1

    return MoodSwing(
        swing_id=str(uuid4()),
        user_id=user_id,
        start_time=start,
        end_time=end,
        duration_minutes=duration,
        energy_path=energy_path,
        swing_intensity=max_intensity,
        swing_volatility=swing_volatility,
        adjusted_volatility=adjusted_vol,
        avg_energy_level=avg_energy,
        direction=direction,
        num_transitions=transitions,
        recovered_to_zero=True,
        log_ids=",".join(str(log.log_id) for log in swing_logs),
        created_at=datetime.now(LOCAL_TIMEZONE)
    )