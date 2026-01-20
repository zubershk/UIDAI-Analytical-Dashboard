import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.ingestion import load_monthly_features, load_priority_table
import streamlit.components.v1 as components
import os

# ==============================
# Page Configuration
# ==============================
st.set_page_config(
    page_title="UIDAI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# Load Data
# ==============================
@st.cache_data
def load_data():
    monthly = load_monthly_features("data/feature_engineered_monthly.csv")
    priority = load_priority_table("data/state_priority_classification_final.csv")
    
    # Check if forecast file exists, if not generate it
    forecast_path = "data/state_forecasts_3month.csv"
    if not os.path.exists(forecast_path):
        with st.spinner('Generating forecasts for the first time... (this may take a minute)'):
            try:
                from src.generate_all_forecasts import main as generate_forecasts
                generate_forecasts()
            except Exception as e:
                st.error(f"Failed to generate forecasts: {str(e)}")

    # Load analytical CSVs with proper error handling
    analytics = {}
    files_to_load = [
        ('stat_summary', 'data/statistical_summary.csv'),
        ('regional', 'data/regional_summary.csv'),
        ('forecasts', 'data/state_forecasts_3month.csv'),
        ('benchmarking', 'data/state_benchmarking.csv'),
        ('effect_size', 'data/effect_size_analysis.csv')
    ]
    
    for name, path in files_to_load:
        try:
            if os.path.exists(path):
                analytics[name] = pd.read_csv(path)
            else:
                analytics[name] = pd.DataFrame()
        except PermissionError:
            st.error(f"Error: Permission denied accessing {path}")
            analytics[name] = pd.DataFrame()
    
    return monthly, priority, analytics

df_monthly, df_priority, analytics = load_data()

# ==============================
# CSS Styling - Clean & Simple
# ==============================
st.markdown("""
<style>
    /* Main app background - UIDAI Light Blue */
    .stApp {
        background-color: #98B5DCFF;
    }
    
    /* Metric/KPI Cards - Blue gradient with hover */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #0B3C5D 0%, #1e3a8a 100%);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-left: 5px solid #D97706;
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    }
    
    [data-testid="stMetric"] label {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #D97706 !important;
    }
    
    /* Tables - FORCE WHITE backgrounds */
    div[data-testid="stDataFrame"],
    div[data-testid="stDataFrame"] > div,
    div[data-testid="stDataFrame"] > div > div {
        background-color: white !important;
        border-radius: 10px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Table styling for st.table */
    [data-testid="stTable"] table {
        width: 100% !important;
        border-collapse: collapse !important;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Table headers - Light Blue background with Dark text */
    [data-testid="stTable"] thead th {
        background-color: #DBEAFE !important;
        color: #0B3C5D !important;
        font-weight: 700 !important;
        padding: 14px 12px !important;
        text-align: left !important;
        border-bottom: 2px solid #0B3C5D !important;
    }
    
    /* Table body - White with Black text */
    [data-testid="stTable"] tbody td {
        background-color: white !important;
        color: #1E293B !important;
        padding: 12px !important;
        border-bottom: 1px solid #E2E8F0 !important;
    }
    
    /* Hover effect on rows */
    [data-testid="stTable"] tbody tr:hover td {
        background-color: #F8FAFC !important;
    }
    
    /* Enhanced Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B3C5D 0%, #072338 100%);
        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Sidebar header styling */
    [data-testid="stSidebar"] h1 {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        padding: 1rem 0 !important;
        border-bottom: 2px solid #D97706 !important;
        margin-bottom: 1.5rem !important;
    }
    
    /* Radio buttons styling */
    [data-testid="stSidebar"] .stRadio > label {
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        gap: 0.5rem !important;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        padding: 0.75rem 1rem !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(255,255,255,0.1) !important;
    }
    
    /* Selectbox styling */
    [data-testid="stSidebar"] .stSelectbox > label {
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* RESPONSIVE DESIGN */
    
    /* Tablet (portrait) and below */
    @media (max-width: 768px) {
        /* Title and headers */
        h1 {
            font-size: 1.75rem !important;
        }
        
        h2, h3 {
            font-size: 1.25rem !important;
        }
        
        /* Metric cards - stack vertically */
        [data-testid="stMetric"] {
            padding: 15px !important;
        }
        
        [data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-size: 2rem !important;
        }
        
        /* Tables - smaller text */
        [data-testid="stTable"] thead th {
            padding: 10px 8px !important;
            font-size: 0.85rem !important;
        }
        
        [data-testid="stTable"] tbody td {
            padding: 8px !important;
            font-size: 0.85rem !important;
        }
        
        /* Sidebar - auto-collapse on mobile */
        [data-testid="stSidebar"] {
            width: 280px !important;
        }
    }
    
    /* Mobile (landscape and portrait) */
    @media (max-width: 640px) {
        /* Main title */
        h1 {
            font-size: 1.5rem !important;
            padding: 0.5rem 0 !important;
        }
        
        h2 {
            font-size: 1.1rem !important;
        }
        
        h3 {
            font-size: 1rem !important;
        }
        
        /* Metrics */
        [data-testid="stMetric"] {
            padding: 12px !important;
            margin-bottom: 10px !important;
        }
        
        [data-testid="stMetric"] label {
            font-size: 0.75rem !important;
        }
        
        [data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
        
        /* Tables - much smaller */
        [data-testid="stTable"] thead th {
            padding: 8px 6px !important;
            font-size: 0.75rem !important;
        }
        
        [data-testid="stTable"] tbody td {
            padding: 6px !important;
            font-size: 0.75rem !important;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            width: 260px !important;
        }
        
        [data-testid="stSidebar"] h1 {
            font-size: 1.25rem !important;
        }
        
        /* Plotly charts - ensure they're responsive */
        .js-plotly-plot {
            width: 100% !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# Enhanced Sidebar
# ==============================
st.sidebar.markdown("# UIDAI Analytics")
st.sidebar.markdown("*State-level Performance Monitoring*")
st.sidebar.markdown("---")

# Navigation
st.sidebar.markdown("### Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["Overview", "Statistical Analysis", "Geographic Insights", "Forecasting", "State Details"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# State Selection
st.sidebar.markdown("### State Selection")
selected_state = st.sidebar.selectbox(
    "Choose a state",
    sorted(df_priority["state"].unique()),
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# Filters
st.sidebar.markdown("### Filters")
status_filter = st.sidebar.radio(
    "Filter by Performance Status",
    ["All", "DECAYING", "HEALTHY"],
    label_visibility="collapsed"
)

filtered_priority = df_priority if status_filter == "All" else df_priority[df_priority["state_status"] == status_filter]

st.sidebar.markdown("---")

# Info Section
st.sidebar.markdown("### About")
st.sidebar.markdown("**UIDAI Data Hackathon 2026**")
st.sidebar.markdown("Developed by Zuber Shaikh")
st.sidebar.markdown("[GitHub Repository](https://github.com/zubershk/UIDAI-Analytical-Dashboard.git)")
st.sidebar.markdown("")

# ==============================
# Header
# ==============================
st.title("AADHAAR OPERATIONAL ANALYTICS")
st.markdown("### Strategy & Policy Division | State-Level Update Monitoring")
st.markdown("---")

# ==============================
# PAGE: OVERVIEW
# ==============================
if page == "Overview":
    # KPIs
    col1, col2, col3 = st.columns(3)
    
    total = len(df_priority)
    decaying = (df_priority["state_status"] == "DECAYING").sum()
    healthy = (df_priority["state_status"] == "HEALTHY").sum()
    
    with col1:
        st.metric("Healthy States", healthy, delta="Good Performance", delta_color="normal")
    with col2:
        st.metric("Decaying States", decaying, delta="Needs Attention", delta_color="inverse")
    with col3:
        st.metric("Total States", total, delta="Complete Coverage", delta_color="off")
    
    st.markdown("---")
    
    # State Info
    st.subheader(f"Selected State: {selected_state}")
    
    state_filter = df_priority[df_priority['state'] == selected_state]
    if state_filter.empty:
        st.error(f"No data found for {selected_state}")
        st.stop()
    state_data = state_filter.iloc[0]
    state_ts = df_monthly[df_monthly['state'] == selected_state].sort_values('year_month')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Status", state_data['state_status'])
    with col2:
        st.metric("Priority Rank", f"#{int(state_data['priority_rank'])}")
    with col3:
        st.metric("Avg Intensity", f"{state_data['avg_update_intensity']:.2f}")
    with col4:
        if len(state_ts) >= 2:
            recent = state_ts.tail(1)['update_intensity'].values[0]
            prev = state_ts.tail(2).head(1)['update_intensity'].values[0]
            trend = ((recent - prev) / prev * 100) if prev > 0 else 0
            st.metric("Monthly Trend", f"{trend:+.1f}%")
        else:
            st.metric("Monthly Trend", "N/A")
    
    st.markdown("---")
    
    # Low Activity States Chart
    st.subheader("Low Activity States")
    bottom_10 = df_priority.nsmallest(10, "avg_update_intensity")
    fig = go.Figure(go.Bar(
        y=bottom_10["state"],
        x=bottom_10["avg_update_intensity"],
        orientation='h',
        marker_color='#b91c1c'
    ))
    fig.update_layout(
        height=400,
        yaxis={'categoryorder': 'total ascending'},
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Trend Chart
    st.subheader(f"Update Intensity Trend: {selected_state}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=state_ts['year_month'],
        y=state_ts['update_intensity'],
        mode='lines+markers',
        name='Intensity',
        line=dict(color='#0B3C5D', width=3),
        marker=dict(size=8)
    ))
    fig.add_trace(go.Scatter(
        x=state_ts['year_month'],
        y=state_ts['update_intensity_3m_avg'],
        mode='lines',
        name='3-Month Avg',
        line=dict(color='#D97706', width=2, dash='dash')
    ))
    fig.update_layout(
        height=400,
        showlegend=True,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Priority Table
    st.subheader("Priority Matrix")
    display_df = filtered_priority.sort_values("priority_rank").head(15)[
        ["state", "state_status", "avg_update_intensity", "priority_rank"]
    ].copy()
    display_df.columns = ["State Name", "Status", "Avg Update Intensity", "Priority Rank"]
    st.table(display_df)

# ==============================
# PAGE: STATISTICAL ANALYSIS
# ==============================
elif page == "Statistical Analysis":
    st.subheader("National Statistics")
    
    if not analytics['stat_summary'].empty:
        # Use actual data count instead of incorrect CSV value
        actual_states = len(df_priority)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("States/UTs Analyzed", actual_states)
        if 'states_with_significant_decline' in analytics['stat_summary'].columns:
            with col2:
                st.metric("Declining States", int(analytics['stat_summary']['states_with_significant_decline'].values[0]))
        if 'states_with_large_effect_decay' in analytics['stat_summary'].columns:
            with col3:
                st.metric("Critical States", int(analytics['stat_summary']['states_with_large_effect_decay'].values[0]))
        if 'national_median_intensity' in analytics['stat_summary'].columns:
            with col4:
                st.metric("Median Intensity", f"{analytics['stat_summary']['national_median_intensity'].values[0]:.2f}")
    
    st.markdown("---")
    
    # Benchmarking Table
    if not analytics['benchmarking'].empty:
        st.subheader("State Benchmarking")
        cols = ['state', 'avg_intensity', 'percentile', 'trend']
        available_cols = [c for c in cols if c in analytics['benchmarking'].columns]
        display_df = analytics['benchmarking'].nlargest(20, 'avg_intensity')[available_cols].copy()
        # Rename columns for better readability
        col_rename = {'state': 'State Name', 'avg_intensity': 'Avg Intensity', 'percentile': 'Percentile', 'trend': 'Trend'}
        display_df.columns = [col_rename.get(c, c) for c in display_df.columns]
        st.table(display_df)
    
    st.markdown("---")
    
    # Effect Size
    if not analytics['effect_size'].empty:
        st.subheader("Effect Size Analysis")
        cols = ['state', 'early_mean', 'recent_mean', 'change', 'cohens_d', 'magnitude']
        available_cols = [c for c in cols if c in analytics['effect_size'].columns]
        display_df = analytics['effect_size'].nsmallest(10, 'cohens_d')[available_cols].copy()
        # Rename columns for better readability
        col_rename = {'state': 'State Name', 'early_mean': 'Early Mean', 'recent_mean': 'Recent Mean', 'change': 'Change', 'cohens_d': "Cohen's D", 'magnitude': 'Magnitude'}
        display_df.columns = [col_rename.get(c, c) for c in display_df.columns]
        st.table(display_df)
    
    st.markdown("---")
    
    # Visualization Images
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Correlation Heatmap")
        if os.path.exists("data/correlation_heatmap.png"):
            st.image("data/correlation_heatmap.png", caption="9×9 Correlation Matrix", use_container_width=True)
    with col2:
        st.subheader("Confidence Intervals")
        if os.path.exists("data/confidence_intervals.png"):
            st.image("data/confidence_intervals.png", caption="95% CI for State Estimates", use_container_width=True)

# ==============================
# PAGE: GEOGRAPHIC INSIGHTS  
# ==============================
elif page == "Geographic Insights":
    st.subheader("Regional Performance")
    
    if not analytics['regional'].empty:
        reg_df = analytics['regional'].sort_values('mean_intensity', ascending=False)
        
        # Regional Performance Chart (full width)
        fig = go.Figure(go.Bar(
            x=reg_df['region'],
            y=reg_df['mean_intensity'],
            marker_color='#0B3C5D',
            text=reg_df['num_states'].apply(lambda x: f"{int(x)} states"),
            textposition='outside'
        ))
        fig.update_layout(
            height=400,
            showlegend=False,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Regional Data Table
        st.subheader("Regional Summary")
        reg_display = reg_df[['region', 'mean_intensity', 'num_states']].copy()
        reg_display.columns = ['Region', 'Mean Intensity', 'States Count']
        st.table(reg_display)
    
    st.markdown("---")
    
    # Interactive Map
    st.subheader("Interactive India Map")
    if os.path.exists("data/india_interactive_map.html"):
        with open("data/india_interactive_map.html", 'r', encoding='utf-8') as f:
            components.html(f.read(), height=600, scrolling=True)
    else:
        st.info("Interactive map available after running notebook 07")
    
    st.markdown("---")
    
    # Static Visualization Images
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Regional Comparison")
        if os.path.exists("data/regional_comparison.png"):
            st.image("data/regional_comparison.png", caption="Regional Performance Comparison", use_container_width=True)
    with col2:
        st.subheader("State Distribution")
        if os.path.exists("data/india_state_visualization.png"):
            st.image("data/india_state_visualization.png", caption="State-wise Update Intensity", use_container_width=True)

# ==============================
# PAGE: FORECASTING
# ==============================
elif page == "Forecasting":
    st.subheader("ARIMA Forecasting Results")
    
    if not analytics['forecasts'].empty and selected_state in analytics['forecasts']['state'].values:
        st_forecast = analytics['forecasts'][analytics['forecasts']['state'] == selected_state]
        
        st.markdown(f"**3-Month Forecast: {selected_state}**")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=st_forecast['forecast_month'],
            y=st_forecast['forecast_value'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#D97706', width=3),
            marker=dict(size=10)
        ))
        fig.add_trace(go.Scatter(
            x=list(st_forecast['forecast_month']) + list(st_forecast['forecast_month'])[::-1],
            y=list(st_forecast['upper_bound']) + list(st_forecast['lower_bound'])[::-1],
            fill='toself',
            fillcolor='rgba(217,119,6,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='95% CI'
        ))
        fig.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        forecast_display = st_forecast[['forecast_month', 'forecast_value', 'lower_bound', 'upper_bound']].copy()
        forecast_display.columns = ['Month', 'Forecast Value', 'Lower CI', 'Upper CI']
        st.table(forecast_display)
    
    st.markdown("---")
    
    # Forecasts Visualization Image
    st.subheader("All State Forecasts Overview")
    if os.path.exists("data/forecasts_visualization.png"):
        st.image("data/forecasts_visualization.png", caption="3-Month ARIMA Forecasts for All States", use_container_width=True)

# ==============================
# PAGE: STATE DETAILS
# ==============================
elif page == "State Details":
    st.subheader(f"Detailed Analysis: {selected_state}")
    
    state_filter = df_priority[df_priority['state'] == selected_state]
    if state_filter.empty:
        st.error(f"No data found for {selected_state}")
        st.stop()
    state_data = state_filter.iloc[0]
    state_ts = df_monthly[df_monthly['state'] == selected_state].sort_values('year_month')
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Status", state_data['state_status'])
    with col2:
        st.metric("Priority Rank", f"#{int(state_data['priority_rank'])}")
    with col3:
        st.metric("Avg Intensity", f"{state_data['avg_update_intensity']:.2f}")
    
    st.markdown("---")
    
    # Time Series
    st.subheader("Complete Time Series")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=state_ts['year_month'],
        y=state_ts['update_intensity'],
        mode='lines+markers',
        name='Update Intensity',
        line=dict(color='#0B3C5D', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=state_ts['year_month'],
        y=state_ts['update_intensity_3m_avg'],
        mode='lines',
        name='3-Month Moving Average',
        line=dict(color='#D97706', width=2, dash='dash')
    ))
    fig.update_layout(height=450, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Historical Data
    st.subheader("Historical Data")
    hist_display = state_ts[['year_month', 'update_intensity', 'update_intensity_3m_avg']].sort_values('year_month', ascending=False).copy()
    hist_display.columns = ['Year-Month', 'Update Intensity', '3-Month Average']
    st.table(hist_display)

# ==============================
# Footer
# ==============================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; color: #1E293B;'>
    <p><strong>UIDAI Data Hackathon 2026</strong> | Developed by Zuber Shaikh</p>
</div>
""", unsafe_allow_html=True)