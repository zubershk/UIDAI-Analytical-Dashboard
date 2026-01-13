import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit.components.v1 as components
import os

# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="UIDAI Analytical Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# UIDAI Original Theme
# ==============================
UIDAI_THEME = {
    "bg_app": "#98B5DCFF",       # Original light blue
    "bg_surface": "#FFFFFF",     # White cards
    "text_primary": "#1E293B",   # Dark text
    "text_secondary": "#64748B", # Muted text
    "brand_blue": "#0B3C5D",     # UIDAI dark blue
    "brand_orange": "#D97706",   # Orange accent
    "success": "#15803d",        # Green
    "danger": "#b91c1c",         # Red
    "border": "#E2E8F0"          # Light border
}

# ==============================
# Data Loading
# ==============================
@st.cache_data
def load_data():
    from src.ingestion import load_monthly_features, load_priority_table
    monthly = load_monthly_features("data/feature_engineered_monthly.csv")
    priority = load_priority_table("data/state_priority_classification_final.csv")
    return monthly, priority

@st.cache_data
def load_analytics():
    def safe_load(path):
        try:
            return pd.read_csv(path)
        except:
            return pd.DataFrame()
    
    return {
        'stat_summary': safe_load("data/statistical_summary.csv"),
        'regional': safe_load("data/regional_summary.csv"),
        'forecasts': safe_load("data/state_forecasts_3month.csv"),
        'benchmarking': safe_load("data/state_benchmarking.csv"),
        'effect_size': safe_load("data/effect_size_analysis.csv")
    }

df_monthly, df_priority = load_data()
analytics = load_analytics()

# ==============================
# CSS Styling - Professional & User-Friendly
# ==============================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp {{
        background-color: {UIDAI_THEME['bg_app']};
    }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {UIDAI_THEME['brand_blue']} 0%, #0a2f47 100%);
    }}
    
    section[data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    section[data-testid="stSidebar"] label {{
        font-weight: 500 !important;
    }}
    
    /* Main header */
    .dashboard-header {{
        background: linear-gradient(135deg, {UIDAI_THEME['brand_blue']} 0%, #1e3a8a 100%);
        padding: 35px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        margin-bottom: 30px;
        border-left: 6px solid {UIDAI_THEME['brand_orange']};
    }}
    
    .dashboard-header h1 {{
        color: white;
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
    }}
    
    .dashboard-header p {{
        color: #E2E8F0;
        margin: 12px 0 0 0;
        font-size: 1.1rem;
    }}
    
    /* KPI Cards */
    .kpi-card {{
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
        border-left: 5px solid;
        transition: transform 0.2s;
    }}
    
    .kpi-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }}
    
    .kpi-value {{
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 8px;
    }}
    
    .kpi-label {{
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 600;
        color: {UIDAI_THEME['text_secondary']};
    }}
    
    /* Content cards */
    .content-card {{
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }}
    
    .content-card h3 {{
        color: {UIDAI_THEME['brand_blue']};
        margin-top: 0;
        margin-bottom: 20px;
        font-size: 1.3rem;
        font-weight: 600;
    }}
    
    /* Insight box */
    .insight-box {{
        background: white;
        padding: 25px;
        border-radius: 10px;
        border-left: 4px solid {UIDAI_THEME['brand_blue']};
        margin: 20px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }}
    
    .insight-box p {{
        margin: 0;
        color: {UIDAI_THEME['text_primary']};
        line-height: 1.8;
        font-size: 1.05rem;
    }}
    
    /* Page title */
    .page-title {{
        color: {UIDAI_THEME['brand_blue']};
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 3px solid {UIDAI_THEME['brand_orange']};
    }}
    
    /* Visualization container */
    .viz-container {{
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }}
    
    .viz-container img {{
        border-radius: 8px;
        width: 100%;
        height: auto;
    }}
    
    /* Responsive */
    @media (max-width: 768px) {{
        .dashboard-header h1 {{
            font-size: 1.5rem;
        }}
        .kpi-value {{
            font-size: 2rem;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ==============================
# Sidebar
# ==============================
st.sidebar.markdown("""
<div style='padding: 20px 0; text-align: center; border-bottom: 2px solid rgba(255,255,255,0.2);'>
    <h1 style='margin: 0; font-size: 1.8rem;'>AADHAAR</h1>
    <p style='margin: 5px 0 0 0; font-size: 0.85rem; opacity: 0.9;'>Analytics Dashboard</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

page = st.sidebar.radio(
    "NAVIGATION",
    ["Overview", "Statistical Analysis", "Geographic Insights", "Forecasting", "State Deep Dive"]
)

st.sidebar.markdown("---")

selected_state = st.sidebar.selectbox(
    "Select State",
    sorted(df_priority["state"].unique())
)

status_filter = st.sidebar.radio(
    "Filter by Status",
    ["All Categories", "DECAYING", "HEALTHY"]
)

filtered_priority = df_priority if status_filter == "All Categories" else df_priority[df_priority["state_status"] == status_filter]

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.markdown("UIDAI Data Hackathon 2026")
st.sidebar.markdown("[GitHub](https://github.com/zubershk)")

# ==============================
# Header
# ==============================
st.markdown("""
<div class="dashboard-header">
    <h1>AADHAAR OPERATIONAL ANALYTICS</h1>
    <p>Strategy & Policy Division | State-Level Update Monitoring System</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# Helper Function for KPI Cards
# ==============================
def render_kpi(value, label, color):
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: {color};">
        <div class="kpi-value" style="color: {color};">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

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
        render_kpi(healthy, "HEALTHY REGIONS", UIDAI_THEME['success'])
    with col2:
        render_kpi(decaying, "CRITICAL / DECAYING", UIDAI_THEME['danger'])
    with col3:
        render_kpi(total, "TOTAL COVERED", UIDAI_THEME['brand_orange'])
    
    # State Insights
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### State Insights")
    
    state_data = df_priority[df_priority['state'] == selected_state].iloc[0]
    state_ts = df_monthly[df_monthly['state'] == selected_state].sort_values('year_month')
    
    if len(state_ts) >= 2:
        recent = state_ts.tail(1)['update_intensity'].values[0]
        prev = state_ts.tail(2).head(1)['update_intensity'].values[0]
        trend_pct = ((recent - prev) / prev * 100) if prev > 0 else 0
        trend = "Increasing" if trend_pct > 0 else "Declining" if trend_pct < 0 else "Stable"
    else:
        trend_pct = 0
        trend = "Stable"
    
    status = state_data['state_status']
    rank = int(state_data['priority_rank'])
    color = UIDAI_THEME['danger'] if status == "DECAYING" else UIDAI_THEME['success']
    
    st.markdown(f"""
    <div class="insight-box" style="border-left-color: {color};">
        <p>
            <strong style='color: {UIDAI_THEME['brand_blue']}; font-size: 1.3rem;'>{selected_state}</strong><br><br>
            <strong>Status:</strong> <span style='color: {color}; font-weight: 700;'>{status}</span> | 
            <strong>Priority Rank:</strong> #{rank} of {total}<br>
            <strong>Recent Trend:</strong> {trend_pct:+.1f}% ({trend})<br><br>
            <strong>Recommendation:</strong> {
                "Immediate intervention required. Deploy targeted engagement campaigns."
                if status == "DECAYING" else
                "Performance stable. Continue monitoring."
            }
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Priority Matrix")
        display_df = filtered_priority.sort_values("priority_rank").head(15)[
            ["state", "state_status", "avg_update_intensity", "priority_rank"]
        ]
        st.dataframe(display_df, use_container_width=True, height=400, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Low Activity Regions")
        bottom_10 = df_priority.nsmallest(10, "avg_update_intensity")
        fig = go.Figure(go.Bar(
            y=bottom_10["state"],
            x=bottom_10["avg_update_intensity"],
            orientation='h',
            marker_color=UIDAI_THEME['danger'],
            marker=dict(line=dict(width=0))
        ))
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            height=380,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # State Trend
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown(f"### Update Trend: {selected_state}")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=state_ts['year_month'], 
        y=state_ts['update_intensity'],
        mode='lines+markers',
        name='Update Intensity',
        line=dict(color=UIDAI_THEME['brand_blue'], width=3),
        marker=dict(size=8, color=UIDAI_THEME['brand_blue'])
    ))
    fig.add_trace(go.Scatter(
        x=state_ts['year_month'],
        y=state_ts['update_intensity_3m_avg'],
        mode='lines',
        name='3-Month Average',
        line=dict(color=UIDAI_THEME['brand_orange'], width=2, dash='dash')
    ))
    fig.update_layout(
        height=400,
        hovermode='x unified',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# PAGE: STATISTICAL ANALYSIS
# ==============================
elif page == "Statistical Analysis":
    st.markdown('<div class="page-title">Statistical Analysis Results</div>', unsafe_allow_html=True)
    
    # KPIs
    if not analytics['stat_summary'].empty:
        df_stat = analytics['stat_summary']
        col1, col2, col3, col4 = st.columns(4)
        
        metrics = [
            (col1, 'total_states', 'STATES', UIDAI_THEME['brand_blue']),
            (col2, 'states_with_significant_decline', 'DECLINING', UIDAI_THEME['danger']),
            (col3, 'states_with_large_effect_decay', 'CRITICAL', UIDAI_THEME['brand_orange']),
            (col4, 'national_median_intensity', 'MEDIAN', UIDAI_THEME['success'])
        ]
        
        for col, key, label, color in metrics:
            if key in df_stat.columns:
                val = df_stat[key].values[0]
                val_str = str(int(val)) if key != 'national_median_intensity' else f"{val:.2f}"
                with col:
                    render_kpi(val_str, label, color)
    
    # Visualizations - Links only to avoid memory errors
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Correlation Matrix")
        if os.path.exists("data/correlation_heatmap.png"):
            st.markdown("""  
            Large visualization available for download:  
            [Open Correlation Heatmap](data/correlation_heatmap.png)
            """)
            st.info("View in data folder to avoid memory issues in browser")
        else:
            st.info("Visualization will be generated after running notebook 06")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Confidence Intervals")
        if os.path.exists("data/confidence_intervals.png"):
            st.markdown("""  
            Large visualization available for download:  
            [Open Confidence Intervals](data/confidence_intervals.png)
            """)
            st.info("View in data folder to avoid memory issues in browser")
        else:
            st.info("Visualization will be generated after running notebook 06")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Data Tables
    if not analytics['benchmarking'].empty:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### State Benchmarking")
        cols = ['state']
        for c in ['avg_intensity', 'percentile', 'trend']:
            if c in analytics['benchmarking'].columns:
                cols.append(c)
        display_df = analytics['benchmarking'].nlargest(20, cols[1])[cols] if len(cols) > 1 else analytics['benchmarking']
        st.dataframe(display_df, use_container_width=True, height=400, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if not analytics['effect_size'].empty:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Effect Size Analysis")
        cols = ['state', 'early_mean', 'recent_mean', 'change', 'cohens_d', 'magnitude']
        display_df = analytics['effect_size'].nsmallest(10, 'cohens_d')[[c for c in cols if c in analytics['effect_size'].columns]]
        st.dataframe(display_df, use_container_width=True, height=350, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# PAGE: GEOGRAPHIC INSIGHTS
# ==============================
elif page == "Geographic Insights":
    st.markdown('<div class="page-title">Geographic Analysis</div>', unsafe_allow_html=True)
    
    # Interactive Map
    st.markdown('<div class="viz-container">', unsafe_allow_html=True)
    st.markdown("### Interactive India Map")
    if os.path.exists("data/india_interactive_map.html"):
        with open("data/india_interactive_map.html", 'r', encoding='utf-8') as f:
            html_content = f.read()
        components.html(html_content, height=600, scrolling=True)
    else:
        st.info("Interactive map will be available after running notebook 07")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # State Visualization - Link only
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### State-wise Breakdown")
    if os.path.exists("data/india_state_visualization.png"):
        st.markdown("""  
        Large India state visualization (1000+ rows):  
        [Open India State Visualization](data/india_state_visualization.png)  
        """)
        st.info("Large image - view offline to avoid memory issues")
    else:
        st.info("State visualization will be available after running notebook 07")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Regional Data
    if not analytics['regional'].empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("### Regional Performance")
            reg_df = analytics['regional'].sort_values('mean_intensity', ascending=False)
            fig = go.Figure(go.Bar(
                x=reg_df['region'],
                y=reg_df['mean_intensity'],
                marker_color=UIDAI_THEME['brand_blue'],
                text=reg_df['num_states'].apply(lambda x: f"{int(x)} states"),
                textposition='outside',
                marker=dict(line=dict(width=0))
            ))
            fig.update_layout(
                height=350,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("### Regional Data")
            st.dataframe(reg_df[['region', 'mean_intensity', 'num_states']], 
                        use_container_width=True, height=350, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# PAGE: FORECASTING
# ==============================
elif page == "Forecasting":
    st.markdown('<div class="page-title">Predictive Analytics</div>', unsafe_allow_html=True)
    
    # Forecast visualization - Link only
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### ARIMA Forecasts (Top 10 Decaying States)")
    if os.path.exists("data/forecasts_visualization.png"):
        st.markdown("""  
        Large forecast visualization with multiple subplots:  
        [Open Forecast Visualization](data/forecasts_visualization.png)  
        """)
        st.info("Large composite image - view offline to avoid memory issues")
    else:
        st.info("Forecast visualization will be available after running notebook 08")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # State-specific forecast
    if not analytics['forecasts'].empty and selected_state in analytics['forecasts']['state'].values:
        st_forecast = analytics['forecasts'][analytics['forecasts']['state'] == selected_state]
        
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown(f"### 3-Month Forecast: {selected_state}")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=st_forecast['forecast_month'], 
            y=st_forecast['forecast_value'],
            mode='lines+markers',
            name='Forecast',
            line=dict(color=UIDAI_THEME['brand_orange'], width=3),
            marker=dict(size=10)
        ))
        
        fig.add_trace(go.Scatter(
            x=list(st_forecast['forecast_month']) + list(st_forecast['forecast_month'])[::-1],
            y=list(st_forecast['upper_bound']) + list(st_forecast['lower_bound'])[::-1],
            fill='toself',
            fillcolor='rgba(217,119,6,0.15)',
            line=dict(color='rgba(255,255,255,0)'),
            name='95% Confidence Interval'
        ))
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(st_forecast[['forecast_month', 'forecast_value', 'lower_bound', 'upper_bound']], 
                    use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# PAGE: STATE DEEP DIVE
# ==============================
elif page == "State Deep Dive":
    state_data = df_priority[df_priority['state'] == selected_state].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    
    status = state_data['state_status']
    color = UIDAI_THEME['danger'] if status == "DECAYING" else UIDAI_THEME['success']
    
    with col1:
        render_kpi(status, "STATUS", color)
    with col2:
        render_kpi(f"#{int(state_data['priority_rank'])}", "PRIORITY", UIDAI_THEME['brand_blue'])
    with col3:
        render_kpi(f"{state_data['avg_update_intensity']:.2f}", "AVG INTENSITY", UIDAI_THEME['brand_orange'])
    
    # Time series
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Complete Time Series Analysis")
    
    state_ts = df_monthly[df_monthly['state'] == selected_state].sort_values('year_month')
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=state_ts['year_month'], 
        y=state_ts['update_intensity'],
        mode='lines+markers',
        name='Update Intensity',
        line=dict(color=UIDAI_THEME['brand_blue'], width=3),
        marker=dict(size=7)
    ))
    fig.add_trace(go.Scatter(
        x=state_ts['year_month'],
        y=state_ts['update_intensity_3m_avg'],
        mode='lines',
        name='3-Month Moving Average',
        line=dict(color=UIDAI_THEME['brand_orange'], width=2, dash='dash')
    ))
    fig.update_layout(
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Historical Data")
    st.dataframe(state_ts[['year_month', 'update_intensity', 'update_intensity_3m_avg']], 
                use_container_width=True, height=400, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# Footer
# ==============================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 25px; color: #64748B;'>
    <p style='margin: 5px; font-size: 0.95rem;'><strong>UIDAI Data Hackathon 2026</strong></p>
    <p style='margin: 5px; font-size: 0.85rem;'>Developed by Zuber Shaikh | Built with Streamlit & Python</p>
</div>
""", unsafe_allow_html=True)