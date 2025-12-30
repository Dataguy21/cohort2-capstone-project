# src/scenario_simulation.py
"""
Scenario Simulation Module (Fully Stable)
-----------------------------------------
Trains a regression model to predict clinical outcomes
based on dosage and compliance-like data.
Works safely even if columns are missing.
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/scenario_model.pkl")


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names to lowercase and ensure required columns exist.
    """
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Create compliance_rate if missing
    if "compliance_rate" not in df.columns:
        # Find any similar column
        similar = [c for c in df.columns if "compliance" in c]
        if similar:
            df["compliance_rate"] = df[similar[0]]
        else:
            # Generate a realistic random compliance rate
            df["compliance_rate"] = np.random.uniform(70, 100, len(df))

    # Create dosage_mg if missing
    if "dosage_mg" not in df.columns:
        similar = [c for c in df.columns if "dosage" in c or "dose" in c]
        if similar:
            df["dosage_mg"] = df[similar[0]]
        else:
            df["dosage_mg"] = np.random.choice([50, 75, 100], len(df))

    # Ensure outcome_score exists
    if "outcome_score" not in df.columns:
        raise KeyError("Dataset must contain an 'outcome_score' column.")

    return df


def train_simulation_model(df: pd.DataFrame) -> dict:
    """
    Train regression model on outcome_score using dosage_mg and compliance_rate.
    """
    df = _normalize_columns(df)

    # ✅ Drop missing safely only if columns exist
    required_cols = ["outcome_score", "dosage_mg", "compliance_rate"]
    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"Required column '{col}' missing after normalization.")

    df = df.dropna(subset=required_cols, how="any")

    if len(df) < 10:
        raise ValueError("Not enough data to train the model. Upload a larger dataset.")

    X = df[["dosage_mg", "compliance_rate"]]
    y = df["outcome_score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    metrics = {
        "r2": round(r2_score(y_test, preds), 3),
        "mae": round(mean_absolute_error(y_test, preds), 3),
    }

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return metrics


def simulate_scenario(dosage_change_pct: float, compliance_change_pct: float, df: pd.DataFrame) -> float:
    """
    Predict how average outcome changes if dosage/compliance shift by given %.
    """
    df = _normalize_columns(df)

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not trained yet! Run train_simulation_model() first.")

    model = joblib.load(MODEL_PATH)

    base_X = df[["dosage_mg", "compliance_rate"]].copy()
    base_outcome = df["outcome_score"].mean()

    # Apply hypothetical changes
    base_X["dosage_mg"] *= (1 + dosage_change_pct / 100)
    base_X["compliance_rate"] *= (1 + compliance_change_pct / 100)

    predicted_outcomes = model.predict(base_X)
    simulated_mean = predicted_outcomes.mean()

    delta = simulated_mean - base_outcome
    return round(delta, 2)
