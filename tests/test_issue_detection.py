from src.data_loader import load_csv

def test_issue_detection_runs():
    """
    Verify that issue detection can read the dataset successfully.
    Works in both local and CI environments.
    """
    df = load_csv("data/clinical_trial_data.csv")
    assert not df.empty, "❌ DataFrame should not be empty"
    print(f"✅ Loaded dataset with {len(df)} records and {len(df.columns)} columns")
