import math


def compute_rolling_average(series, window: int = 3):
    """
    Compute rolling mean with safe minimum periods.
    """
    return series.rolling(window, min_periods=1).mean()


def compute_decay_signal(series):
    """
    Simple decay signal based on average month-to-month change.
    Negative values indicate decline.
    Returns 0.0 if series is empty or has no valid differences.
    """
    if series is None or len(series) < 2:
        return 0.0
    diff = series.diff().mean()
    if math.isnan(diff):
        return 0.0
    return diff


def classify_state(
    avg_update_intensity: float,
    recent_update_intensity: float,
    decay_signal: float
) -> str:
    """
    Rule-based state classification with safe handling of edge cases.
    
    Args:
        avg_update_intensity: Average update intensity over time
        recent_update_intensity: Most recent update intensity
        decay_signal: Decay signal (negative = declining)
    
    Returns:
        Classification: "STAGNANT", "DECAYING", or "HEALTHY"
    """
    # Handle None and NaN values
    if avg_update_intensity is None or math.isnan(avg_update_intensity):
        return "STAGNANT"
    if recent_update_intensity is None or math.isnan(recent_update_intensity):
        return "STAGNANT"
    if decay_signal is None or math.isnan(decay_signal):
        decay_signal = 0.0
    
    # Use threshold instead of exact zero comparison (floating point safety)
    STAGNANT_THRESHOLD = 1e-6
    if abs(avg_update_intensity) < STAGNANT_THRESHOLD:
        return "STAGNANT"

    # Check for decay with significance threshold
    DECAY_THRESHOLD = -0.01  # 1% decline threshold
    if decay_signal < DECAY_THRESHOLD and recent_update_intensity < avg_update_intensity:
        return "DECAYING"

    return "HEALTHY"
