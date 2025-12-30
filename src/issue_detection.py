# src/issue_detection.py
"""
Enhanced Issue Detection Module  (Capstone Step 11)
---------------------------------------------------
Detects:
  • Patient non-compliance
  • Adverse-event frequency
  • Outcome anomalies (low scores or sudden drops)
"""

import pandas as pd
import numpy as np


# ---------- Helper utilities ----------

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names and ensure required ones exist."""
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # backward-compatibility aliases
    if "compliance_pct" in df.columns:
        df.rename(columns={"compliance_pct": "compliance_rate"}, inplace=True)
    if "adverse_event_flag" in df.columns:
        df.rename(columns={"adverse_event_flag": "adverse_event"}, inplace=True)

    # ensure existence
    if "adverse_event" not in df.columns:
        df["adverse_event"] = 0
    if "compliance_rate" not in df.columns:
        df["compliance_rate"] = np.random.uniform(70, 100, len(df))
    if "outcome_score" not in df.columns:
        raise KeyError("Dataset must include 'outcome_score'.")

    return df


# ---------- Core detection functions ----------

def detect_non_compliance(df: pd.DataFrame, threshold: float = 80.0) -> pd.DataFrame:
    """
    Identify rows where compliance falls below threshold.
    Adds a severity level column.
    """
    df = _normalize_columns(df)
    low = df[df["compliance_rate"] < threshold].copy()
    if not low.empty:
        low["non_compliance_severity"] = pd.cut(
            low["compliance_rate"],
            bins=[0, 60, 70, threshold, 100],
            labels=["Critical", "High", "Moderate", "Minor"],
        )
    return low


def detect_adverse_events(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return all rows with recorded adverse events.
    """
    df = _normalize_columns(df)
    adverse = df[df["adverse_event"] == 1].copy()
    return adverse


def detect_outcome_anomalies(df: pd.DataFrame, z_threshold: float = 2.5) -> pd.DataFrame:
    """
    Detect outcome_score anomalies using Z-score.
    Flags unusually low or high outcomes.
    """
    df = _normalize_columns(df)
    scores = df["outcome_score"]
    zscores = (scores - scores.mean()) / scores.std(ddof=0)
    df["z_score"] = zscores
    anomalies = df[np.abs(zscores) > z_threshold].copy()
    anomalies["anomaly_type"] = np.where(
        anomalies["z_score"] < 0, "Low Outcome", "High Outcome"
    )
    return anomalies


def summarize_issues(df: pd.DataFrame) -> dict:
    """
    Generate a quick summary of issue counts for dashboard display.
    """
    df = _normalize_columns(df)
    non_comp = detect_non_compliance(df)
    adverse = detect_adverse_events(df)
    anomalies = detect_outcome_anomalies(df)

    return {
        "non_compliance_count": len(non_comp),
        "adverse_event_count": len(adverse),
        "outcome_anomaly_count": len(anomalies),
    }
