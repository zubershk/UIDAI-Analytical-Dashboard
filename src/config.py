"""
Configuration module for UIDAI Analytics Dashboard.
Centralizes all configurable values and environment-specific settings.
"""
import os

# ==============================
# Environment Detection
# ==============================
ENV = os.getenv("UIDAI_ENV", "development")
IS_PRODUCTION = ENV == "production"

# ==============================
# Data Paths
# ==============================
DATA_DIR = os.getenv("UIDAI_DATA_DIR", "data")

DATA_FILES = {
    "monthly_features": os.path.join(DATA_DIR, "feature_engineered_monthly.csv"),
    "priority_table": os.path.join(DATA_DIR, "state_priority_classification_final.csv"),
    "stat_summary": os.path.join(DATA_DIR, "statistical_summary.csv"),
    "regional": os.path.join(DATA_DIR, "regional_summary.csv"),
    "forecasts": os.path.join(DATA_DIR, "state_forecasts_3month.csv"),
    "benchmarking": os.path.join(DATA_DIR, "state_benchmarking.csv"),
    "effect_size": os.path.join(DATA_DIR, "effect_size_analysis.csv"),
    "india_map": os.path.join(DATA_DIR, "india_interactive_map.html"),
}

# ==============================
# Classification Thresholds
# ==============================
STAGNANT_THRESHOLD = 1e-6  # Below this is considered stagnant
DECAY_THRESHOLD = -0.01    # Decay signal threshold (1% decline)

# ==============================
# Display Settings
# ==============================
TABLE_ROW_LIMITS = {
    "priority_matrix": 15,
    "benchmarking": 20,
    "effect_size": 10,
    "low_activity": 10,
}

# ==============================
# Color Palette (UIDAI Theme)
# ==============================
COLORS = {
    "primary": "#0B3C5D",      # Dark blue
    "secondary": "#D97706",     # Orange accent
    "background": "#98B5DCFF",  # Light blue
    "healthy": "#10B981",       # Green
    "decaying": "#EF4444",      # Red
    "stagnant": "#6B7280",      # Gray
    "header_bg": "#DBEAFE",     # Light blue for headers
    "text_dark": "#1E293B",     # Dark text
    "text_light": "#E2E8F0",    # Light text
}

# ==============================
# Indian States/UTs Count
# ==============================
EXPECTED_STATES_COUNT = 36  # 28 States + 8 Union Territories
