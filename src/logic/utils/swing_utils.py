# --- SWING TRACKING UTILS ---

def is_swing_boundary(prev_energy: int, curr_energy: int) -> bool:
    return prev_energy == 0 or curr_energy == 0

def is_energy_transition(prev: int, curr: int) -> bool:
    return prev != curr

def is_valid_swing_sequence(seq: list[int]) -> bool:
    return seq and seq[0] == 0 and seq[-1] == 0 and len(seq) > 2

def calculate_swing_duration(start_ts: str, end_ts: str) -> str:
    try:
        start = datetime.fromisoformat(start_ts)
        end = datetime.fromisoformat(end_ts)
        duration = end - start
        return str(duration)
    except Exception:
        return "unknown"

def format_swing_path(seq: list[int]) -> str:
    symbols = [get_energy_symbol(s) for s in seq]
    return " → ".join(symbols)
