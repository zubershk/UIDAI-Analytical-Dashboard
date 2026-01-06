import pandas as pd


def load_monthly_features(path: str) -> pd.DataFrame:
    """
    Load state-level monthly feature data.
    Enforces datetime parsing and drops invalid rows.
    """
    df = pd.read_csv(path)
    df["year_month"] = pd.to_datetime(df["year_month"])
    df = df[df["year_month"].notna()]
    return df


def load_priority_table(path: str) -> pd.DataFrame:
    """
    Load final state priority classification table.
    """
    return pd.read_csv(path)
