import os
import logging
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Logging
logging.basicConfig(filename="ingestion.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

MERGED_FILE = "./processed/merged_churn.csv"

def validate():
    """
    Validate merged churn data:
    - missing values
    - duplicated rows
    - numeric range checks
    - data type checks
    - simple anomaly/outlier detection (z-score > 3)
    - PDF data quality report
    """
    if not os.path.exists(MERGED_FILE):
        logging.error(f"Merged file not found: {MERGED_FILE}")
        return

    df = pd.read_csv(MERGED_FILE)
    issues = []

    # 1. Missing values
    miss = df.isnull().sum()
    for col, cnt in miss.items():
        if cnt > 0:
            issues.append(("merged_churn", col, "missing_values", int(cnt)))

    # 2. Duplicate rows
    dup = int(df.duplicated().sum())
    if dup > 0:
        issues.append(("merged_churn", "ALL", "duplicate_rows", dup))

    # 3. Data type / range / outlier checks
    for col in df.columns:
        if df[col].dtype in ["int64", "float64"]:
            # Range check (>= 0)
            if (df[col] < 0).any():
                issues.append(("merged_churn", col, "negative_value", int((df[col] < 0).sum())))
            # Outlier check (z-score > 3)
            if df[col].std() > 0:  # avoid division by zero
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                out_count = int((z_scores > 3).sum())
                if out_count > 0:
                    issues.append(("merged_churn", col, "outliers", out_count))
        else:
            if not pd.api.types.is_string_dtype(df[col]):
                issues.append(("merged_churn", col, "unexpected_type", str(df[col].dtype)))

    # ------ Generate PDF report ------
    report_path = f"data_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis("off")
    table = ax.table(
        cellText=issues if len(issues) > 0 else [["(no issues)", "", "", ""]],
        colLabels=["file", "column", "issue_type", "count"],
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.4)
    plt.title("Data Quality Report")
    plt.savefig(report_path, bbox_inches="tight")
    plt.close()

    logging.info(f"✅ Data validation completed. Report written to: {report_path}")

if __name__ == "__main__":
    validate()
