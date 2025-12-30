# src/ui/streamlit_app.py
"""
Clinical Insights Assistant - Streamlit UI
------------------------------------------
Now includes:
- Stable file upload with session persistence
- Doctor notes summarization (Gemini)
- FDA-style regulatory summary generator
"""

import os
import sys
import pandas as pd
import streamlit as st

# ✅ Ensure src package imports work regardless of run location
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.data_loader import load_csv
from src.issue_detection import detect_non_compliance, detect_adverse_events
from src.cohort_analysis import cohort_summary
from src.genai_interface import summarize_doctor_notes, generate_regulatory_summary

# ----------------------- PAGE CONFIG -----------------------
st.set_page_config(page_title="Clinical Insights Assistant", layout="wide")
st.title("💊 Clinical Insights Assistant")

st.markdown("""
Welcome to the **GenAI-powered Clinical Insights Assistant**.

This tool helps pharma teams analyze clinical trial data, detect key issues, 
summarize doctor feedback, and generate FDA-style regulatory summaries.
""")

# ----------------------- FILE UPLOAD & DATA LOAD -----------------------
if "uploaded_df" not in st.session_state:
    st.session_state.uploaded_df = None

uploaded_file = st.file_uploader("📂 Upload your clinical_trial_data.csv", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV and store it in session memory
    try:
        df_uploaded = pd.read_csv(uploaded_file, parse_dates=["visit_date"])
        st.session_state.uploaded_df = df_uploaded
        st.success("✅ File uploaded and loaded successfully!")
    except Exception as e:
        st.error(f"❌ Error reading uploaded file: {e}")

# Use uploaded data if available; otherwise, fall back to bundled sample
if st.session_state.uploaded_df is not None:
    df = st.session_state.uploaded_df
    st.info("📄 Using your uploaded dataset.")
else:
    st.info("ℹ️ No upload detected. Using bundled sample dataset.")
    sample_path = os.path.join(os.path.dirname(__file__), "../../data/clinical_trial_data.csv")
    df = load_csv(sample_path)

# ----------------------- DATA PREVIEW -----------------------
st.subheader("📊 Data Preview")
st.dataframe(df.head(10), use_container_width=True)

# ----------------------- ISSUE DETECTION -----------------------
st.header("🚨 Issue Detection")

col1, col2 = st.columns(2)

non_compliant = detect_non_compliance(df)
adverse = detect_adverse_events(df)

with col1:
    st.metric("Non-Compliant Records", len(non_compliant))
    if not non_compliant.empty:
        st.dataframe(non_compliant.head(), use_container_width=True)

with col2:
    st.metric("Adverse Events Detected", len(adverse))
    if not adverse.empty:
        st.dataframe(adverse.head(), use_container_width=True)

from src.issue_detection import detect_outcome_anomalies, summarize_issues

st.subheader("📈 Advanced Issue Summary")
summary = summarize_issues(df)
st.metric("Non-Compliance", summary["non_compliance_count"])
st.metric("Adverse Events", summary["adverse_event_count"])
st.metric("Outcome Anomalies", summary["outcome_anomaly_count"])

if st.checkbox("Show Outcome Anomalies"):
    st.dataframe(detect_outcome_anomalies(df))


# ----------------------- COHORT COMPARISON -----------------------
st.header("👥 Cohort Outcome Comparison")
summary_df = cohort_summary(df)
st.dataframe(summary_df, use_container_width=True)

# ----------------------- SCENARIO SIMULATION -----------------------
st.header("🧪 Scenario Simulation")

from src.scenario_simulation import train_simulation_model, simulate_scenario

if st.button("📈 Train Outcome Prediction Model"):
    with st.spinner("Training regression model..."):
        metrics = train_simulation_model(df)
    st.success(f"✅ Model trained! R²={metrics['r2']} | MAE={metrics['mae']}")

dosage_change = st.slider("💊 Dosage Change (%)", -50, 50, 10)
compliance_change = st.slider("✅ Compliance Change (%)", -50, 50, 10)

if st.button("🔮 Run Simulation"):
    try:
        delta = simulate_scenario(dosage_change, compliance_change, df)
        if delta > 0:
            st.success(f"📊 Predicted average outcome improvement: +{delta:.2f}")
        else:
            st.warning(f"📉 Predicted average outcome drop: {delta:.2f}")
    except Exception as e:
        st.error(f"⚠️ Simulation error: {e}")

# ----------------------- DOCTOR NOTES SUMMARY -----------------------
st.header("🧠 Doctor Notes Summary (Gemini AI)")
sample_notes = df["doctor_notes"].dropna().unique().tolist()[:25]

if st.button("🧩 Generate Doctor Notes Summary"):
    with st.spinner("Generating summary with Gemini..."):
        summary_text = summarize_doctor_notes(sample_notes)
    st.success("✅ Summary Generated")
    st.write(summary_text)
else:
    st.caption("Click to generate a GenAI summary of doctor feedback.")

# ----------------------- REGULATORY SUMMARY GENERATOR -----------------------
st.header("🧾 Regulatory Summary Generator (FDA-style)")

reg_input = st.text_area(
    "Paste or describe trial results / observations below:",
    placeholder="Example: Cohort A showed 85% compliance with mild headaches as the main adverse event. Outcome scores improved by 15%..."
)

if st.button("📄 Generate Regulatory Summary"):
    if reg_input.strip():
        with st.spinner("Generating FDA-style summary via Gemini..."):
            summary = generate_regulatory_summary(reg_input)
        st.success("✅ Regulatory Summary Generated")
        st.write(summary)
    else:
        st.warning("⚠️ Please enter trial details first.")

# ----------------------- FOOTER -----------------------
st.markdown("""
---
**Note:**  
- If you uploaded your dataset, it will stay loaded during this session.  
- The AI features use **Google Gemini 2.0 Flash** (via `.env` key).  
- To activate GenAI, ensure your `.env` file contains `GOOGLE_API_KEY=your_key_here`.
""")
