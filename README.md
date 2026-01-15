# UIDAI Aadhaar Update Decay Analysis  
**UIDAI Data Hackathon 2026**

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-green?logo=streamlit&logoColor=white)
![Analysis](https://img.shields.io/badge/Analysis-Statistical-orange)
![License](https://img.shields.io/badge/License-Government%20Use-red)

A **production-grade**, state-level analytical system to detect **declining Aadhaar update activity**, identify **priority regions**, and support **evidence-based administrative decision-making.**

---


## Live Dashboard
**[View Interactive Dashboard](https://uidai-analytical-dash.streamlit.app/)**

---

## 1. Problem Context

Aadhaar enrolment and update services are critical national infrastructure.  
However, **update activity does not remain uniform over time or geography**.

Key operational questions faced by administrators include:

- Which states show **persistent low update activity**?
- Where is update engagement **declining over time**?
- Which regions should be **prioritized for intervention**?
- How can this be detected **early**, using data alone?

This project addresses these questions by building a **reproducible, state-level analytical framework** and deploying it as a **live, interactive dashboard**.

---

## Key Findings

Our statistical analysis of Aadhaar update patterns across India reveals:

- **26 states** exhibit statistically significant declining update trends (Mann-Kendall test, p<0.05)
- **7 states** show large effect size decay (Cohen's d > 0.8), requiring immediate intervention
- **Puducherry** shows the strongest decay signal (avg intensity: 2168 → 486, -77.6% decline)
- **Northeast region** demonstrates most consistent update engagement (lowest volatility)
- **Early detection** enables **3-6 month advance warning** before critical thresholds

### Impact Metrics
- **36 states/UTs analyzed** with **1.2M+ data points**
- **Priority ranking system** covering **100% of Indian states**
- **Real-time dashboard** with **3-month forecasting** capability
- **Statistical validation** using Mann-Kendall, effect size, and confidence intervals
- **Regional patterns** identified across 6 geographical zones

---

## Visualizations

### Correlation Analysis
![Correlation Heatmap](data/correlation_heatmap.png)
*9×9 correlation matrix showing relationships between all metrics*

### State-wise Analysis
![India State Visualization](data/india_state_visualization.png)
*Geographic distribution of update intensity across Indian states*

### Regional Comparison
![Regional Comparison](data/regional_comparison.png)
*Performance comparison across 6 geographical regions*

### Forecasting Results
![Forecasts Visualization](data/forecasts_visualization.png)
*3-month ARIMA predictions with 95% confidence intervals*

### Statistical Confidence
![Confidence Intervals](data/confidence_intervals.png)
*95% confidence intervals for state-level estimates*

---

## Quick Start

### Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/zubershk/UIDAI-Analytical-Dashboard.git
cd UIDAI-Analytical-Dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch dashboard
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## Project Structure

```
UIDAI-Analytical-Dashboard/
├── app.py                    # Streamlit dashboard (main entry)
├── requirements.txt          # Python dependencies (pinned versions)
├── README.md                 # This file
├── METHODOLOGY.md            # Technical documentation
├── .gitignore                # Git exclusions
│
├── data/
│   ├── feature_engineered_monthly.csv    # Main dataset
│   ├── state_priority_classification_final.csv
│   ├── statistical_summary.csv
│   ├── regional_summary.csv
│   ├── state_forecasts_3month.csv
│   ├── state_benchmarking.csv
│   ├── effect_size_analysis.csv
│   ├── correlation_heatmap.png
│   ├── confidence_intervals.png
│   ├── forecasts_visualization.png
│   ├── india_state_visualization.png
│   ├── regional_comparison.png
│   └── india_interactive_map.html
│
├── notebooks/
│   ├── 01_data_ingestion_and_schema_check.ipynb
│   ├── 02_data_cleaning_and_alignment.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_analysis_and_visuals.ipynb
│   ├── 05_anomaly_detection_optional.ipynb
│   ├── 06_statistical_analysis.ipynb
│   ├── 07_geospatial_viz.ipynb
│   └── 08_forecasting.ipynb
│
└── src/
    ├── __init__.py           # Module exports
    ├── config.py             # Configuration settings
    ├── ingestion.py          # Data loading
    ├── preprocessing.py      # Data transformation
    ├── metrics.py            # Statistical calculations
    └── visualization.py      # Chart generation
```

---

## Problem Statement

### Official UIDAI Hackathon Challenge

**"Unlocking Societal Trends in Aadhaar Enrolment and Updates"**

> Identify meaningful patterns, trends, anomalies, or predictive indicators and translate them into clear insights or solution frameworks that can support informed decision-making and system improvements.

### Our Approach

Aadhaar enrolment and update services are critical national infrastructure. However, **update activity does not remain uniform over time or geography**.

This project addresses the challenge by:

✅ **Identifying Patterns**: Detected declining update trends across 26 states using Mann-Kendall statistical tests  
✅ **Finding Anomalies**: Identified 7 states with large effect size decay requiring immediate intervention  
✅ **Predictive Analytics**: Built ARIMA forecasting models providing 3-month advance warnings  
✅ **Decision Support**: Created priority ranking system and interactive dashboard for administrators  
✅ **System Improvements**: Proposed regional intervention strategies based on geographic clustering

### Key Questions Answered

- Which states show **persistent low update activity**? → **36 states analyzed, 28 decaying**
- Where is update engagement **declining over time**? → **26 states show significant decline (p<0.05)**
- Which regions should be **prioritized for intervention**? → **Top 10 ranked by risk score**
- How can this be detected **early**? → **3-6 month advance warning via forecasting**

---

## Methodology

### Datasets Used (Official UIDAI Data)

**Aadhaar-related aggregated/anonymized datasets** provided by UIDAI:

1. **Enrolment Data** (1,006,029 records)
   - State-wise enrolment counts
   - Age groups: 5-17 years, 18+ years
   - Monthly temporal granularity

2. **Demographic Update Data** (2,071,700 records)  
   - Name, address, photo updates
   - Age-wise breakdown (5-17, 18+)
   - State and district level aggregation

3. **Biometric Update Data** (1,861,108 records)
   - Fingerprint and iris updates
   - Age-wise breakdown (5-17, 18+)
   - Geographic distribution

**Data Characteristics**:
- ✅ Fully anonymized and aggregated at state/district level
- ✅ Non-identifiable (no PII)
- ✅ Monthly time series (12 months coverage)
- ✅ Supports univariate, bivariate, and trivariate analyses
- ✅ Multi-dimensional (age groups, update types, geography)

**Columns Used in Analysis**:
- `state`, `year_month` (temporal)
- `enrol_age_5_17`, `enrol_age_18_plus` (enrolment metrics)
- `demo_age_5_17`, `demo_age_18_plus` (demographic updates)
- `bio_age_5_17`, `bio_age_18_plus` (biometric updates)
- Derived: `update_intensity`, `update_decay_signal`, `state_status`

### Analytical Pipeline

**Step 1**: Data Ingestion & Schema Validation  
**Step 2**: Data Cleaning & Alignment (state normalization)  
**Step 3**: Feature Engineering (update intensity, rolling averages, decay signals)  
**Step 4**: Statistical Analysis (Mann-Kendall tests, effect sizes, confidence intervals)  
**Step 5**: Classification & Ranking (HEALTHY/DECAYING states)  
**Step 6**: Geospatial & Predictive Analytics (regional clustering, ARIMA forecasting)  
**Step 7**: Deployment (Streamlit Cloud dashboard)

*Full methodology available in [METHODOLOGY.md](METHODOLOGY.md)*

---

## Dashboard Features

### Five Comprehensive Pages

1. **Overview**: KPIs, state insights, priority matrix, trend charts
2. **Statistical Analysis**: Summary stats, benchmarking, correlation matrix, effect sizes
3. **Geographic Insights**: Interactive India map, regional performance, state breakdown
4. **Forecasting**: ARIMA predictions with confidence intervals, scenario analysis
5. **State Deep Dive**: Detailed time series and metrics for selected state

### Key Features

- **Interactive Controls**: State selector, status filter, navigation menu
- **KPI Cards**: Real-time statistics (Healthy/Decaying/Total states)
- **Auto-Insights**: Context-aware recommendations per state
- **Priority Matrix**: Sortable ranking table
- **Regional Charts**: Geographic zone performance
- **Trend Analysis**: Time series with rolling averages
- **Forecasting**: 3-month ARIMA predictions with 95% CI

---

## Statistical Rigor

### Tests Conducted
- **Mann-Kendall Trend Test**: Non-parametric trend detection (p-values reported)
- **Effect Size Analysis**: Cohen's d for decay magnitude quantification
- **Confidence Intervals**: 95% CI for all state estimates
- **Correlation Analysis**: 9×9 metric relationship heatmap

### Results
- **72%** of states show significant trends (p < 0.10)
- **26 states** have declining trends (p < 0.05)
- **7 states** require immediate intervention (large effect decay)

---

## Geospatial Analysis

States grouped into 6 geographical regions:
- **North**: 8 states (J&K, Ladakh, HP, Punjab, Haryana, Delhi, Uttarakhand, Chandigarh)
- **Central**: 3 states (UP, MP, Chhattisgarh)
- **East**: 4 states (Bihar, Jharkhand, West Bengal, Odisha)
- **Northeast**: 8 states (Assam, Arunachal, Nagaland, Manipur, Mizoram, Tripura, Meghalaya, Sikkim)
- **West**: 5 states (Rajasthan, Gujarat, Goa, Maharashtra, DNH-DD)
- **South**: 6 states (Karnataka, AP, Telangana, TN, Kerala, Puducherry)
- **Islands**: 2 UTs (Andaman & Nicobar, Lakshadweep)

**Finding**: Northeast region shows lowest decay rate (-2.1% avg)

---

## Forecasting

### ARIMA Models
- **3-month ahead predictions** for top 10 decaying states
- **95% confidence intervals** for all forecasts
- **Scenario analysis**: Impact of +20% / +50% intervention

### Sample Predictions
- **Puducherry**: 486 → 398 (continued decline without intervention)
- **Himachal Pradesh**: 576 → 512 (requires engagement campaign)

---

## Dependencies

```txt
streamlit==1.41.0
pandas==2.2.3
plotly==5.24.1
matplotlib==3.9.3
scipy==1.14.1
statsmodels==0.14.4
numpy==2.0.2
```

Install all: `pip install -r requirements.txt`

---

### Run the Dashboard

```bash
streamlit run app.py
```

---

## Data Usage

### Source
All datasets are **official UIDAI data** provided for the Data Hackathon 2026.

### Privacy & Compliance
- ✅ **Fully Anonymized**: No personally identifiable information (PII)
- ✅ **Aggregated Data**: State/district level only, no individual records
- ✅ **Non-Traceable**: All data points are statistical summaries
- ✅ **Ethical Use**: Strictly for analytical and administrative purposes

### Data Processing
1. **Raw Data**: Loaded from UIDAI-provided CSV files
2. **Cleaning**: State normalization, temporal alignment, missing value handling
3. **Transformation**: Feature engineering (update intensity, decay signals)
4. **Analysis**: Statistical tests, forecasting, geographic clustering
5. **Storage**: Processed CSVs (5 MB total) for dashboard

### Usage Rights
- Data used under **UIDAI Data Hackathon 2026** guidelines
- For **research, analysis, and administrative decision support**
- Not for commercial distribution or unauthorized purposes

---

## Submission Format (UIDAI Hackathon)

This project fulfills all UIDAI hackathon submission requirements:

### 1. Problem Statement and Approach ✅
- **Problem**: Identifying declining Aadhaar update trends for administrative intervention
- **Approach**: Statistical analysis + machine learning + interactive dashboard
- See sections above for detailed explanation

### 2. Datasets Used ✅
- **Enrolment Data**: 1,006,029 records
- **Demographic Update Data**: 2,071,700 records
- **Biometric Update Data**: 1,861,108 records
- All columns documented in "Datasets Used" section

### 3. Methodology ✅
- **Data Cleaning**: State name normalization, temporal alignment, missing value handling
- **Preprocessing**: Monthly aggregation, rolling averages, decay signal calculation
- **Transformations**: Update intensity metric, percentile rankings, risk scores
- Full details in [METHODOLOGY.md](METHODOLOGY.md)

### 4. Data Analysis and Visualisation ✅
- **Key Findings**: 26 states declining, 7 critical, Northeast most stable
- **Visualisations**: 8 PNG charts, 2 interactive HTML maps, live dashboard
- **Code**: 8 Jupyter notebooks included in `/notebooks` directory
- **GitHub**: Code available at [zubershk/UIDAI-Analytical-Dashboard](https://github.com/zubershk/UIDAI-Analytical-Dashboard)

---

## License

This project is developed for government/administrative use under the UIDAI Data Hackathon 2026 guidelines.

**Data Usage**: All datasets are anonymized and used strictly for analytical purposes.

---

## Developer

**Zuber Shaikh**  
- GitHub: [@zubershk](https://github.com/zubershk)
- Project Repo: [UIDAI-Analytical-Dashboard](https://github.com/zubershk/UIDAI-Analytical-Dashboard)

---

## Achievements

✅ **Live Production Dashboard**: Deployed on Streamlit Cloud  
✅ **Statistical Rigor**: Hypothesis testing with p-values  
✅ **Predictive Power**: 3-month ARIMA forecasts  
✅ **Geographic Context**: India-specific regional analysis  
✅ **Publication-Quality**: Academic-grade methodology  
✅ **Impact-Driven**: Quantified benefits (26 states identified, 3-6 month early warning)

---

## Support

For questions or issues:
1. Open an [issue](https://github.com/zubershk/UIDAI-Analytical-Dashboard/issues)
2. Check [METHODOLOGY.md](METHODOLOGY.md) for technical details
3. Review notebooks for analysis steps

---

**Last Updated**: January 2026  
**Version**: 3.0 (Flattened Structure Edition)

---

<div align="center">

**Made for UIDAI Data Hackathon 2026**

[Live Dashboard](https://uidai-analytical-dash.streamlit.app/) • [GitHub](https://github.com/zubershk/UIDAI-Analytical-Dashboard) • [Methodology](METHODOLOGY.md)

</div>

