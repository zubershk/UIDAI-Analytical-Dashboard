import pandas as pd

# Standard state name mapping for data consistency
STATE_NAME_MAPPING = {
    # Andaman and Nicobar
    'ANDAMAN & NICOBAR ISLANDS': 'ANDAMAN AND NICOBAR ISLANDS',
    'ANDAMAN & NICOBAR': 'ANDAMAN AND NICOBAR ISLANDS',
    
    # Dadra and Nagar Haveli and Daman and Diu (merged UT)
    'DADRA & NAGAR HAVELI AND DAMAN AND DIU': 'DADRA AND NAGAR HAVELI AND DAMAN AND DIU',
    'THE DADRA AND NAGAR HAVELI AND DAMAN AND DIU': 'DADRA AND NAGAR HAVELI AND DAMAN AND DIU',
    'DADRA & NAGAR HAVELI': 'DADRA AND NAGAR HAVELI AND DAMAN AND DIU',
    'DADRA AND NAGAR HAVELI': 'DADRA AND NAGAR HAVELI AND DAMAN AND DIU',
    'DAMAN & DIU': 'DADRA AND NAGAR HAVELI AND DAMAN AND DIU',
    'DAMAN AND DIU': 'DADRA AND NAGAR HAVELI AND DAMAN AND DIU',
    'D & N HAVELI': 'DADRA AND NAGAR HAVELI AND DAMAN AND DIU',
    
    # Puducherry (old name: Pondicherry)
    'PONDICHERRY': 'PUDUCHERRY',
    
    # West Bengal variations
    'WEST  BENGAL': 'WEST BENGAL',
    'WEST BANGAL': 'WEST BENGAL',
    'WESTBENGAL': 'WEST BENGAL',
    'WEST BENGLI': 'WEST BENGAL',
    
    # Jammu and Kashmir
    'JAMMU & KASHMIR': 'JAMMU AND KASHMIR',
    'J & K': 'JAMMU AND KASHMIR',
    
    # Telangana
    'TELENGANA': 'TELANGANA',
    
    # Odisha (old name: Orissa)
    'ORISSA': 'ODISHA',
    
    # Chhattisgarh
    'CHHATISGARH': 'CHHATTISGARH',
    'CHATTISGARH': 'CHHATTISGARH',
    
    # Tamil Nadu
    'TAMILNADU': 'TAMIL NADU',
    
    # Uttarakhand (old name: Uttaranchal)
    'UTTARANCHAL': 'UTTARAKHAND',
}

# Invalid entries that are cities, not states/UTs
INVALID_STATE_ENTRIES = [
    'BALANAGAR', 'DARBHANGA', 'JAIPUR', 'MADANAPALLE',
    'NAGPUR', 'PUTTENAHALLI', 'RAJA ANNAMALAI PURAM'
]


def standardize_state_names(df: pd.DataFrame, state_column: str = 'state') -> pd.DataFrame:
    """
    Standardize state names to remove duplicates and typos.
    Applies the STATE_NAME_MAPPING and removes invalid entries.
    
    Args:
        df: DataFrame with a state column
        state_column: Name of the column containing state names
        
    Returns:
        DataFrame with standardized state names
    """
    df = df.copy()
    df[state_column] = df[state_column].str.upper().str.strip()
    df[state_column] = df[state_column].replace(STATE_NAME_MAPPING)
    df = df[~df[state_column].isin(INVALID_STATE_ENTRIES)]
    return df


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

