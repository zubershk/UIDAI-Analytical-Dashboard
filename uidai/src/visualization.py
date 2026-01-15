import plotly.express as px


def low_update_bar_chart(df, color):
    """
    Horizontal bar chart showing states with persistently low update intensity.
    """
    fig = px.bar(
        df,
        x="avg_update_intensity",
        y="state",
        orientation="h",
        title="States with Persistently Low Update Activity",
        labels={
            "avg_update_intensity": "Average Update Intensity",
            "state": "State"
        },
        color_discrete_sequence=[color]
    )
    return fig


def update_trend_chart(df, colors, state_name):
    """
    Line chart showing update intensity and rolling average for a selected state.
    """
    fig = px.line(
        df,
        x="year_month",
        y=["update_intensity", "update_intensity_3m_avg"],
        title=f"Update Intensity Trend: {state_name}",
        labels={
            "year_month": "Month",
            "value": "Update Intensity",
            "variable": "Metric"
        },
        color_discrete_sequence=colors
    )
    return fig
