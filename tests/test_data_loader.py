import os
import pandas as pd
from pathlib import Path
from src.data_loader import load_csv


def test_load():
    """
    Test CSV loading from either real or temporary data.
    Works in both local and GitLab CI environments.
    """

    # Define potential data path
    data_path = Path("data/clinical_trial_data.csv")

    # If the real dataset doesn’t exist, create a mock one
    if not data_path.exists():
        print("⚠️ Data file not found — creating temporary mock CSV for CI...")
        os.makedirs("data", exist_ok=True)
        df_mock = pd.DataFrame({
            "patient_id": ["P001", "P002", "P003"],
            "trial_day": [1, 2, 3],
            "dosage_mg": [50, 100, 75],
            "compliance_pct": [95, 90, 85],
            "adverse_event_flag": [0, 1, 0],
            "doctor_notes": ["ok", "mild headache", "good"],
            "outcome_score": [80.5, 75.2, 89.1],
            "cohort": ["A", "B", "A"],
            "visit_date": ["2024-01-01", "2024-01-02", "2024-01-03"]
        })
        df_mock.to_csv(data_path, index=False)

    # Load CSV using the project’s data loader
    df = load_csv(data_path)

    # Assertions — validate essential schema and data presence
    expected_columns = [
        "patient_id", "trial_day", "dosage_mg", "compliance_pct",
        "adverse_event_flag", "doctor_notes", "outcome_score", "cohort", "visit_date"
    ]

    for col in expected_columns:
        assert col in df.columns, f"❌ Missing expected column: {col}"

    assert not df.empty, "❌ DataFrame should not be empty"
    print(f"✅ CSV loaded successfully with {len(df)} records and columns {list(df.columns)}")
