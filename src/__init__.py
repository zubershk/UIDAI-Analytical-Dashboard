# UIDAI Analytics - Source Module

from .ingestion import load_monthly_features, load_priority_table
from .preprocessing import (
    standardize_state_names,
    filter_states_with_history,
    get_state_timeseries,
    STATE_NAME_MAPPING,
    INVALID_STATE_ENTRIES
)
from .visualization import low_update_bar_chart, update_trend_chart
from .metrics import compute_rolling_average, compute_decay_signal, classify_state
from .config import (
    ENV, IS_PRODUCTION, DATA_DIR, DATA_FILES,
    STAGNANT_THRESHOLD, DECAY_THRESHOLD,
    TABLE_ROW_LIMITS, COLORS, EXPECTED_STATES_COUNT
)

__all__ = [
    # Ingestion
    'load_monthly_features',
    'load_priority_table',
    # Preprocessing
    'standardize_state_names',
    'filter_states_with_history',
    'get_state_timeseries',
    'STATE_NAME_MAPPING',
    'INVALID_STATE_ENTRIES',
    # Visualization
    'low_update_bar_chart',
    'update_trend_chart',
    # Metrics
    'compute_rolling_average',
    'compute_decay_signal',
    'classify_state',
    # Config
    'ENV', 'IS_PRODUCTION', 'DATA_DIR', 'DATA_FILES',
    'STAGNANT_THRESHOLD', 'DECAY_THRESHOLD',
    'TABLE_ROW_LIMITS', 'COLORS', 'EXPECTED_STATES_COUNT',
]


