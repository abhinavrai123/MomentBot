from datetime import datetime
from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from src.config.constants import LOCAL_TIMEZONE
from src.data.models import LogEntry, MoodSwing
from src.data.session import get_session
from src.logic.utils.data_utils import group_logs_by_user, create_synthetic_zero
from datetime import time

ENERGY_WEIGHTS = {
    -2: 2,
    -1: 1,
     0: 0,
     1: 1,
     2: 2
}

async def process_mood_swings():
    """
    Detect mood swings from unprocessed logs and store them.
    Automatically adds a synthetic 0 at 10pm if needed to close swings.
    """
    async with get_session() as session:
        try:
            result = await session.execute(
                select(LogEntry)
                .where(LogEntry.energy_score.isnot(None))
                .order_by(LogEntry.user_id, LogEntry.log_time)
            )
            all_logs = result.scalars().all()
            unassigned_logs = [log for log in all_logs if log.swing_id is None]
            grouped_logs = group_logs_by_user(unassigned_logs)

            swings = []

            for user_id, logs in grouped_logs.items():
                logs = sorted(logs, key=lambda log: log.log_time)
                if not logs:
                    continue

                last_log = logs[-1]
                last_log_time_local = last_log.log_time.astimezone(LOCAL_TIMEZONE)
                ten_pm = datetime.combine(last_log_time_local.date(), time(22, 0)).astimezone(LOCAL_TIMEZONE)

                if last_log.energy_score != 0 and last_log_time_local < ten_pm:
                    synthetic_log = create_synthetic_zero(user_id, last_log_time_local)
                    logs.append(synthetic_log)

                swings_for_user = detect_swings(logs)
                swings.extend(swings_for_user)

            for swing_logs in swings:
                swing_id = f"{datetime.now(LOCAL_TIMEZONE).strftime('%Y%m%d%H%M')}-{uuid4().hex[:6]}"
                swing_entry = create_mood_swing_entry(
                    user_id=swing_logs[0].user_id,
                    swing_logs=swing_logs,
                    swing_id=swing_id
                )

                for log in swing_logs:
                    log.swing_id = swing_id
                    session.add(log)

                session.add(swing_entry)

            if swings:
                await session.commit()

        except SQLAlchemyError as e:
            await session.rollback()
            raise e

def detect_swings(logs: list[LogEntry]) -> list[list[LogEntry]]:
    swings = []
    current_swing = []
    last_was_zero = False

    for log in logs:
        if log.energy_score is None:
            continue

        if log.energy_score == 0:
            if current_swing:
                current_swing.append(log)
                if len(current_swing) > 2:
                    swings.append(current_swing[:])
                current_swing = []
            last_was_zero = True
        else:
            if last_was_zero:
                # Start of a new swing
                current_swing = [logs[logs.index(log) - 1]]  # Include the preceding 0
                last_was_zero = False
            if current_swing is not None:
                current_swing.append(log)

    return swings

def compute_adjusted_volatility(swing_logs):
    total_weighted_energy = 0
    total_transitions = len(swing_logs) - 1
    if total_transitions == 0:
        return 0.0

    for i in range(total_transitions):
        a, b = swing_logs[i], swing_logs[i + 1]

        a_time = a.log_time
        b_time = b.log_time

        if a_time.tzinfo is None:
            a_time = a_time.replace(tzinfo=LOCAL_TIMEZONE)
        if b_time.tzinfo is None:
            b_time = b_time.replace(tzinfo=LOCAL_TIMEZONE)

        minutes = (b_time - a_time).total_seconds() / 60
        energy = abs(ENERGY_WEIGHTS.get(a.energy_score, 0))
        total_weighted_energy += energy * minutes

    return round(total_weighted_energy, 2)

def determine_direction(energy_path: list[str]) -> str:
    ups = sum(1 for e in energy_path if "+" in e)
    downs = sum(1 for e in energy_path if "-" in e)

    if ups > downs:
        return "upward"
    elif downs > ups:
        return "downward"
    else:
        return "mixed"

def parse_energy_label(score: int) -> str:
    return {
        2: "++",
        1: "+",
        0: "0",
        -1: "-",
        -2: "--"
    }.get(score, "?")

def create_mood_swing_entry(user_id: int, swing_logs: list[LogEntry], swing_id: str) -> MoodSwing:
    """
    Constructs a MoodSwing ORM object from a list of log entries (forming a swing).
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
        swing_id=swing_id,
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
