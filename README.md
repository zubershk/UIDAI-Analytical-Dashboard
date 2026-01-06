# UIDAI Aadhaar Update Decay Analysis  
**UIDAI Data Hackathon 2026**

A state-level analytical system to detect **declining Aadhaar update activity**, identify **priority regions**, and support **evidence-based administrative decision-making** using anonymized UIDAI datasets.

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

## 2. What This Project Does

This system:

- Analyzes **monthly Aadhaar enrolment, demographic updates, and biometric updates**
- Computes **update intensity signals** over time
- Detects **update decay trends**
- Classifies states into **HEALTHY / DECAYING** categories
- Produces a **priority ranking** for administrative focus
- Presents insights via a **government-grade interactive dashboard**

⚠️ The system operates **strictly at the state level** and uses **only anonymized, aggregated data**.

---

## 3. Key Concepts Used

### Update Intensity
A normalized measure representing the volume of Aadhaar updates relative to enrolment activity.

### Update Decay
A consistent decline in update intensity over time, indicating reduced engagement or access.

### Rolling Average (3-Month)
Used to smooth short-term fluctuations and highlight sustained trends.

### Priority Rank
A relative ordering of states based on decay signals, volatility, and recent activity.  
This is **not an absolute score**, but a **decision-support ranking**.

---

## 4. Data Used

The analysis uses anonymized UIDAI datasets provided via the hackathon portal:

- Aadhaar Enrolment Data  
- Demographic Update Data  
- Biometric Update Data  

All datasets are:
- Aggregated
- Non-identifiable
- Used only for analytical purposes

---

## 5. Project Architecture

The project is structured to separate **analysis**, **logic**, and **presentation**.

```bash
UIDAI/
├── app.py
│
├── data/
│ ├── enrolment_clean_monthly.csv
│ ├── demographic_clean_monthly.csv
│ ├── biometric_clean_monthly.csv
│ ├── feature_engineered_monthly.csv
│ └── state_priority_classification_final.csv
│
├── notebooks/
│ ├── 01_data_ingestion_and_schema_check.ipynb
│ ├── 02_data_cleaning_and_alignment.ipynb
│ ├── 03_feature_engineering.ipynb
│ ├── 04_analysis_and_visuals.ipynb
│ └── 05_anomaly_detection_optional.ipynb
│
├── src/
│ ├── ingestion.py 
│ ├── preprocessing.py 
│ ├── metrics.py 
│ └── visualization.py 
├── requirements.txt
└── README.md
```

### Design Principles
- **Notebooks** document how insights were developed
- **`src/`** contains reusable, auditable logic
- **`app.py`** is a thin presentation layer
- **Data outputs are frozen** to ensure consistency and performance

---

## 6. Analytical Pipeline

### Step 1: Data Ingestion & Schema Validation
- Verified column consistency across datasets
- Identified aggregation level and time granularity

### Step 2: Data Cleaning & Alignment
- Normalized geographic identifiers
- Standardized time representation (monthly)
- Removed invalid or incomplete records

### Step 3: Feature Engineering
- Computed update intensity metrics
- Generated rolling averages
- Derived decay and consistency signals

### Step 4: Analysis & Classification
- Identified persistent low-update states
- Detected temporal decay patterns
- Classified states using rule-based logic

### Step 5: Deployment
- Deployed results as an interactive Streamlit dashboard
- Enabled filtering, state-level drill-down, and downloads

---

## 7. Dashboard Overview

The deployed dashboard provides:

### National Summary
- Total states analyzed
- Count of decaying vs healthy states

### State Priority Ranking
- Tabular ranking for administrative focus
- Downloadable CSV for reporting

### Persistent Low-Update States
- Horizontal bar chart of lowest average update intensity

### Update Intensity Trend
- Monthly trend with rolling average for any selected state
- Downloadable state-level time series

### Interpretation Guide
- Clear guidance on how to read and act on the insights

---

## 8. How to Run Locally

### Prerequisites
- Python 3.9+
- pip

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the Dashboard
```bash
streamlit run app.py
```