import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

# ==============================
# Import from src
# ==============================
from src.ingestion import load_monthly_features, load_priority_table
from src.preprocessing import get_state_timeseries
import src.visualization as viz

# ==============================
# Page Config
# ==============================
st.set_page_config(
    page_title="UIDAI Analytical Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# 1. DESIGN SYSTEM & ASSETS
# ==============================
UIDAI_THEME = {
    "bg_app": "#98B5DCFF",       
    "bg_surface": "#FFFFFF",   
    "text_primary": "#1E293B", 
    "text_secondary": "#64748B",
    "brand_blue": "#0B3C5D",   
    "brand_orange": "#D97706", 
    "success": "#15803d",      
    "danger": "#b91c1c",       
    "border": "#E2E8F0"        
}

GITHUB_SVG = """
<svg height="20" width="20" viewBox="0 0 16 16" fill="white" style="vertical-align: middle; margin-right: 8px;">
    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
</svg>
"""

# ==============================
# 2. SIDEBAR
# ==============================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/c/cf/Aadhaar_Logo.svg/1200px-Aadhaar_Logo.svg.png", width=140)

st.sidebar.markdown("### SYSTEM CONTROLS")

@st.cache_data
def load_data():
    monthly = load_monthly_features("data/feature_engineered_monthly.csv")
    priority = load_priority_table("data/state_priority_classification_final.csv")
    return monthly, priority

df_monthly, df_priority = load_data()

selected_state = st.sidebar.selectbox(
    "Select Region",
    sorted(df_priority["state"].unique())
)

status_options = ["All Categories"] + sorted(df_priority["state_status"].unique().tolist())
selected_status_radio = st.sidebar.radio(
    "Filter Status",
    status_options
)

if selected_status_radio == "All Categories":
    filtered_priority = df_priority
else:
    filtered_priority = df_priority[df_priority["state_status"] == selected_status_radio]

st.sidebar.divider()

st.sidebar.markdown("### DEVELOPER INFO")
st.sidebar.markdown(
    f"""
    <div style='background-color: rgba(255,255,255,0.08); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.15);'>
        <a href="https://github.com/zubershk" target="_blank" style="text-decoration: none; color: white; display: flex; align-items: center; margin-bottom: 12px; font-weight: 500;">
           {GITHUB_SVG} <span>GitHub Profile</span>
        </a>
        <a href="https://github.com/zubershk/UIDAI-Analytical-Dashboard" target="_blank" style="text-decoration: none; color: white; display: flex; align-items: center; font-weight: 500;">
           {GITHUB_SVG} <span>Project Repository</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# ==============================
# 3. CSS STYLING
# ==============================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: {UIDAI_THEME['text_primary']};
        background-color: {UIDAI_THEME['bg_app']};
    }}
    
    .stApp {{
        background-color: {UIDAI_THEME['bg_app']};
    }}

    .dashboard-header {{
        background: linear-gradient(135deg, #0B3C5D 0%, #1e3a8a 100%);
        padding: 30px;
        border-radius: 12px;
        border-bottom: 5px solid {UIDAI_THEME['brand_orange']};
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
    }}

    .dashboard-header h1 {{
        color: #fff;
        font-family: 'Inter', sans-serif !important;
    }}
    
    .kpi-container {{
        background-color: {UIDAI_THEME['bg_surface']};
        padding: 25px;
        border-radius: 10px;
        border-left: 6px solid; /* Color defined inline */
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }}
    
    .kpi-container:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }}
    
    .kpi-val {{
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1.2;
    }}
    
    .kpi-lbl {{
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
        color: {UIDAI_THEME['text_secondary']};
    }}
    
    section[data-testid="stSidebar"] {{
        background-color: {UIDAI_THEME['brand_blue']};
    }}
    section[data-testid="stSidebar"] h3 {{
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    div[data-testid="stRadio"] label {{
        color: white !important;
    }}
    div[data-testid="stSelectbox"] label {{
        color: white !important;
    }}

    div[data-testid="stDataFrame"], div[data-testid="stPlotlyChart"] {{
        background-color: {UIDAI_THEME['bg_surface']};
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid {UIDAI_THEME['border']};
    }}

    .stMarkdown h2, .stMarkdown h3 {{
        color: {UIDAI_THEME['brand_blue']};
        font-weight: 700 !important;
    }}

    div[data-testid="stCaptionContainer"] {{
        color: {UIDAI_THEME['text_secondary']} !important;
        font-size: 0.9rem !important;
    }}
    
    .stCaption {{
        color: {UIDAI_THEME['text_secondary']} !important;
    }}

    .stMarkdown p {{
        color: {UIDAI_THEME['bg_app']} !important;
    }}
    
</style>
""", unsafe_allow_html=True)

# ==============================
# 4. MAIN LAYOUT
# ==============================

# --- Header ---
st.markdown("""
<div class="dashboard-header">
    <h1 style="margin: 0; font-size: 2rem;">AADHAAR OPERATIONAL ANALYTICS</h1>
    <p style="color: #e2e8f0; margin-top: 8px; font-size: 1.1rem;">
        Strategy & Policy Division | State-Level Update Monitoring System
    </p>
</div>
""", unsafe_allow_html=True)

# --- KPI Section ---
col1, col2, col3 = st.columns(3)
total_states = df_priority.shape[0]
decaying_count = (df_priority["state_status"] == "DECAYING").sum()
healthy_count = (df_priority["state_status"] == "HEALTHY").sum()

with col1:
    st.markdown(f"""
    <div class="kpi-container" style="border-left-color: {UIDAI_THEME['success']}; background: linear-gradient(135deg, #0B3C5D 0%, #1e3a8a 100%)">
        <div class="kpi-val" style="color: {UIDAI_THEME['success']}">{healthy_count}</div>
        <div class="kpi-lbl">Healthy Regions</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-container" style="border-left-color: {UIDAI_THEME['danger']}; background: linear-gradient(135deg, #0B3C5D 0%, #1e3a8a 100%)">
        <div class="kpi-val" style="color: {UIDAI_THEME['danger']}">{decaying_count}</div>
        <div class="kpi-lbl">Critical / Decaying</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-container" style="border-left-color: {UIDAI_THEME['brand_orange']}; background: linear-gradient(135deg, #0B3C5D 0%, #1e3a8a 100%)">
        <div class="kpi-val" style="color: {UIDAI_THEME['brand_orange']}">{total_states}</div>
        <div class="kpi-lbl">Total Covered</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- Priority Matrix ---
st.markdown("### Regional Priority Matrix")

priority_display = filtered_priority.sort_values("priority_rank").reset_index(drop=True)

st.dataframe(
    priority_display.style.background_gradient(cmap="Blues", subset=["priority_rank"]),
    use_container_width=True,
    height=350
)

col_dl, _ = st.columns([1, 4])
with col_dl:
    st.download_button(
        "Download Report",
        data=priority_display.to_csv(index=False),
        file_name="priority_report.csv",
        mime="text/csv",
        use_container_width=True
    )

st.divider()

# --- Visualization ---
col_left, col_right = st.columns(2)

# Chart 1: Low Activity
with col_left:
    st.markdown("### Low Activity Zones")
    st.caption("Top 10 regions requiring immediate engagement intervention.")
    
    low_update = (
        df_monthly.groupby("state", as_index=False)
        .agg(avg_update_intensity=("update_intensity", "mean"))
        .sort_values("avg_update_intensity")
        .head(10)
    )

    fig_low = viz.low_update_bar_chart(low_update, color=UIDAI_THEME['brand_blue'])
    
    fig_low.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black', family="Inter"),
        height=420,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(
            gridcolor="#E2E8F0",
            zeroline=False,
            title_font=dict(size=12, color='black'),
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            gridcolor="#E2E8F0",
            zeroline=False,
            title_font=dict(size=12, color='black'),
            tickfont=dict(color='black')
        )
    )
    st.plotly_chart(fig_low, use_container_width=True)

# Chart 2: Trends
with col_right:
    st.markdown(f"### Performance Trend: {selected_state}")
    st.caption("Historical activity vs 3-month rolling average.")

    state_trend = get_state_timeseries(df_monthly, selected_state)

    fig_trend = viz.update_trend_chart(
        state_trend,
        colors=[UIDAI_THEME['brand_orange'], UIDAI_THEME['brand_blue']],
        state_name=selected_state
    )

    fig_trend.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black', family="Inter"),
        height=420,
        margin=dict(l=20, r=35, t=30, b=20),
        legend=dict(
            orientation="h", 
            yanchor="bottom", y=1.02, 
            xanchor="right", x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(color='black') 
        ),
        xaxis=dict(
            gridcolor="#E2E8F0",
            zeroline=False,
            tickfont=dict(color='black')
        ),
        yaxis=dict(
            gridcolor="#E2E8F0",
            zeroline=False,
            tickfont=dict(color='black')
        )
    )
    st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #64748B; font-size: 0.85rem; padding-bottom: 30px;'>
        <strong>UIDAI Data Hackathon 2026</strong> <br>
        Confidential & Proprietary | Government of India
    </div>
    """,
    unsafe_allow_html=True
)