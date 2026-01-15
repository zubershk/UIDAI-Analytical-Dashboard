def filter_states_with_history(df, min_months: int = 4):
    """
    Keep only states with sufficient temporal coverage.
    """
    return (
        df.groupby("state")
        .filter(lambda x: x["year_month"].nunique() >= min_months)
    )


def get_state_timeseries(df, state: str):
    """
    Return sorted time series for a given state.
    """
    return (
        df[df["state"] == state]
        .sort_values("year_month")
    )
