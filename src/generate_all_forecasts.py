"""
Generate ARIMA Forecasts for ALL States
This script generates 3-month ARIMA forecasts for all states/UTs in the dataset,
not just the top 10 decaying states.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from dateutil.relativedelta import relativedelta
import warnings
import os

warnings.filterwarnings('ignore')

# Get the project root directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")


def load_data():
    """Load the feature engineered monthly data and priority classification."""
    df = pd.read_csv(os.path.join(DATA_DIR, "feature_engineered_monthly.csv"))
    df['year_month'] = pd.to_datetime(df['year_month'])
    df = df.sort_values(['state', 'year_month'])
    
    df_priority = pd.read_csv(os.path.join(DATA_DIR, "state_priority_classification_final.csv"))
    
    print(f"Data loaded: {df.shape[0]} rows")
    print(f"Date range: {df['year_month'].min()} to {df['year_month'].max()}")
    print(f"Total states: {df['state'].nunique()}")
    
    return df, df_priority


def forecast_state_arima(state_name, data, periods=3):
    """
    Forecast update intensity using ARIMA model with improved robustness.
    
    Args:
        state_name: Name of the state
        data: Full dataframe
        periods: Number of months to forecast
    
    Returns:
        Dictionary with historical data, forecast, and confidence intervals
    """
    # Filter state data
    state_df = data[data['state'] == state_name].sort_values('year_month').copy()
    
    # Remove any NaT values
    state_df = state_df[state_df['year_month'].notna()]
    
    if len(state_df) < 6:
        print(f"⚠ Skipping {state_name}: Not enough data points ({len(state_df)})")
        return None
    
    # Prepare time series with proper datetime index
    ts = state_df[['year_month', 'update_intensity']].copy()
    ts = ts.set_index('year_month')['update_intensity']
    
    # Ensure index is datetime
    if not isinstance(ts.index, pd.DatetimeIndex):
        ts.index = pd.to_datetime(ts.index)
    
    # Remove any remaining NaT from index
    ts = ts[ts.index.notna()]
    
    # Remove any NaN values from the series
    ts = ts.dropna()
    
    if len(ts) < 6:
        print(f"⚠ Skipping {state_name}: Not enough valid data points after cleaning ({len(ts)})")
        return None
    
    # Check for constant or near-constant time series
    if ts.std() < 0.001:
        print(f"⚠ Warning: {state_name} has near-constant values, using simple forecast")
        # For constant series, just use the mean as forecast
        mean_val = ts.mean()
        last_date = ts.index[-1]
        future_dates = [last_date + relativedelta(months=i) for i in range(1, periods + 1)]
        future_dates = pd.DatetimeIndex(future_dates)
        
        # Create simple forecast with small CI based on historical range
        std_val = max(ts.std(), ts.mean() * 0.1)  # At least 10% of mean
        
        return {
            'state': state_name,
            'historical_dates': ts.index,
            'historical_values': ts.values,
            'forecast_dates': future_dates,
            'forecast_values': np.array([mean_val] * periods),
            'lower_ci': np.array([mean_val - 1.96 * std_val] * periods),
            'upper_ci': np.array([mean_val + 1.96 * std_val] * periods),
            'model_aic': 0
        }
    
    # Try different ARIMA orders if the default fails
    arima_orders = [
        (1, 0, 1),  # Default
        (1, 1, 1),  # With differencing
        (0, 1, 1),  # Simple MA with differencing
        (1, 0, 0),  # Simple AR
        (0, 0, 1),  # Simple MA
    ]
    
    for order in arima_orders:
        try:
            # Fit ARIMA model
            model = ARIMA(ts, order=order)
            fitted_model = model.fit()
            
            # Forecast
            forecast_result = fitted_model.forecast(steps=periods)
            
            # Get confidence intervals
            forecast_detail = fitted_model.get_forecast(steps=periods)
            forecast_ci = forecast_detail.conf_int()
            
            # Create future dates
            last_date = ts.index[-1]
            future_dates = [last_date + relativedelta(months=i) for i in range(1, periods + 1)]
            future_dates = pd.DatetimeIndex(future_dates)
            
            print(f"✓ Forecast generated for {state_name} (Order: {order}, AIC: {fitted_model.aic:.2f})")
            
            return {
                'state': state_name,
                'historical_dates': ts.index,
                'historical_values': ts.values,
                'forecast_dates': future_dates,
                'forecast_values': forecast_result.values,
                'lower_ci': forecast_ci.iloc[:, 0].values,
                'upper_ci': forecast_ci.iloc[:, 1].values,
                'model_aic': fitted_model.aic
            }
        except Exception as e:
            continue
    
    # If all ARIMA orders fail, use a simple fallback
    print(f"⚠ ARIMA failed for {state_name}, using fallback method")
    try:
        # Use simple moving average as fallback
        mean_val = ts.tail(3).mean()
        std_val = ts.std()
        
        last_date = ts.index[-1]
        future_dates = [last_date + relativedelta(months=i) for i in range(1, periods + 1)]
        future_dates = pd.DatetimeIndex(future_dates)
        
        return {
            'state': state_name,
            'historical_dates': ts.index,
            'historical_values': ts.values,
            'forecast_dates': future_dates,
            'forecast_values': np.array([mean_val] * periods),
            'lower_ci': np.array([mean_val - 1.96 * std_val] * periods),
            'upper_ci': np.array([mean_val + 1.96 * std_val] * periods),
            'model_aic': float('inf')
        }
    except Exception as e:
        print(f"✗ Error forecasting {state_name}: {str(e)}")
        return None


def generate_all_forecasts(df, df_priority):
    """Generate forecasts for ALL states."""
    # Get all unique states
    all_states = df['state'].unique().tolist()
    
    print(f"\nGenerating forecasts for {len(all_states)} states:")
    print("-" * 50)
    
    forecasts = {}
    for state in all_states:
        result = forecast_state_arima(state, df, periods=3)
        if result:
            forecasts[state] = result
    
    print("-" * 50)
    print(f"\nSuccessfully forecasted {len(forecasts)} out of {len(all_states)} states")
    
    return forecasts


def save_forecasts_to_csv(forecasts, output_path):
    """Save forecasts to CSV file."""
    rows = []
    for state, forecast in forecasts.items():
        for i, date in enumerate(forecast['forecast_dates']):
            rows.append({
                'state': state,
                'forecast_month': date.strftime('%Y-%m-%d'),
                'forecast_value': forecast['forecast_values'][i],
                'lower_bound': forecast['lower_ci'][i],
                'upper_bound': forecast['upper_ci'][i]
            })
    
    df_forecast = pd.DataFrame(rows)
    df_forecast.to_csv(output_path, index=False)
    print(f"\nForecasts saved to {output_path}")
    print(f"Total rows: {len(df_forecast)}")
    return df_forecast


def create_visualization(forecasts, output_path):
    """Create visualization for all state forecasts."""
    n_states = len(forecasts)
    
    # Calculate grid dimensions (aim for roughly 6 columns)
    n_cols = 6
    n_rows = (n_states + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(24, 4 * n_rows))
    axes = axes.flatten() if n_states > 1 else [axes]
    
    states_sorted = sorted(forecasts.keys())
    
    for idx, state in enumerate(states_sorted):
        ax = axes[idx]
        forecast = forecasts[state]
        
        # Plot historical data
        ax.plot(forecast['historical_dates'], forecast['historical_values'], 
                'b-', linewidth=1.5, label='Historical', alpha=0.7)
        
        # Plot forecast
        ax.plot(forecast['forecast_dates'], forecast['forecast_values'], 
                'r-', linewidth=2, label='Forecast', marker='o')
        
        # Plot confidence interval
        ax.fill_between(forecast['forecast_dates'], 
                       forecast['lower_ci'], 
                       forecast['upper_ci'], 
                       alpha=0.3, color='red', label='95% CI')
        
        ax.set_title(state, fontsize=8, fontweight='bold')
        ax.tick_params(axis='both', labelsize=6)
        ax.tick_params(axis='x', rotation=45)
        
        # Add grid
        ax.grid(True, alpha=0.3)
    
    # Hide empty subplots
    for idx in range(len(forecasts), len(axes)):
        axes[idx].set_visible(False)
    
    plt.suptitle('3-Month ARIMA Forecasts for All States', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"Visualization saved to {output_path}")


def main():
    """Main function to generate all forecasts."""
    print("=" * 60)
    print("ARIMA Forecasting for All States")
    print("=" * 60)
    
    # Load data
    df, df_priority = load_data()
    
    # Generate forecasts for all states
    forecasts = generate_all_forecasts(df, df_priority)
    
    # Save to CSV
    output_csv = os.path.join(DATA_DIR, "state_forecasts_3month.csv")
    save_forecasts_to_csv(forecasts, output_csv)
    
    # Create visualization
    output_png = os.path.join(DATA_DIR, "forecasts_visualization.png")
    create_visualization(forecasts, output_png)
    
    print("\n" + "=" * 60)
    print("Forecasting complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
