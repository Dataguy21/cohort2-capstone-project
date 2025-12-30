import pandas as pd

def cohort_summary(df: pd.DataFrame, group_col='cohort'):
    """Return mean outcome_score and counts per cohort."""
    return df.groupby(group_col).agg(
        mean_outcome=('outcome_score','mean'),
        count=('patient_id','nunique')
    ).reset_index()
