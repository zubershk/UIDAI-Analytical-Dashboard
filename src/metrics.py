def compute_rolling_average(series, window: int = 3):
    """
    Compute rolling mean with safe minimum periods.
    """
    return series.rolling(window, min_periods=1).mean()


def compute_decay_signal(series):
    """
    Simple decay signal based on average month-to-month change.
    Negative values indicate decline.
    """
    return series.diff().mean()


def classify_state(
    avg_update_intensity: float,
    recent_update_intensity: float,
    decay_signal: float
):
    """
    Rule-based state classification.
    """
    if avg_update_intensity == 0:
        return "STAGNANT"

    if decay_signal < 0 and recent_update_intensity < avg_update_intensity:
        return "DECAYING"

    return "HEALTHY"
