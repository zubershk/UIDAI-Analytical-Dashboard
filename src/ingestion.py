import pandas as pd
from .preprocessing import standardize_state_names


def load_monthly_features(path: str) -> pd.DataFrame:
    """
    Load state-level monthly feature data.
    Enforces datetime parsing, drops invalid rows, and standardizes state names.
    """
    df = pd.read_csv(path)
    df["year_month"] = pd.to_datetime(df["year_month"])
    df = df[df["year_month"].notna()]
    df = standardize_state_names(df)
    return df


def load_priority_table(path: str) -> pd.DataFrame:
    """
    Load final state priority classification table.
    Applies state name standardization.
    """
    df = pd.read_csv(path)
    df = standardize_state_names(df)
    return df

