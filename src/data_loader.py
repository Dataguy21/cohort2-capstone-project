import pandas as pd
from pathlib import Path

def load_csv(path: str):
    """Load CSV into pandas DataFrame."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"{path} not found")
    return pd.read_csv(path, parse_dates=['visit_date'])

if __name__ == '__main__':
    df = load_csv('../data/clinical_trial_data.csv')
    print(df.head())
