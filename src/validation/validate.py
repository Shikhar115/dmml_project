import os
import logging
from datetime import datetime
import pandas as pd

# same log file name as your original global config
logging.basicConfig(filename="ingestion.log", level=logging.INFO)

def validate():
    """
    Advanced data validation:
    - missing values
    - duplicated rows
    - numeric range checks
    - data type checks
    - simple anomaly/outlier detection (z-score > 3)
    - PDF data quality report
    """
    import matplotlib.pyplot as plt
    import numpy as np

    issues = []

    for fname in os.listdir("./raw_data"):
        df = pd.read_csv("./raw_data/" + fname)

        # 1. Missing values
        miss = df.isnull().sum()
        for col, cnt in miss.items():
            if cnt > 0:
                issues.append((fname, col, "missing_values", int(cnt)))

        # 2. Duplicate rows
        dup = int(df.duplicated().sum())
        if dup > 0:
            issues.append((fname, "ALL", "duplicate_rows", dup))

        # 3. Data type / range check (example)
        for col in df.columns:
            if df[col].dtype in ["int64","float64"]:
                # Range check (>= 0)
                if (df[col] < 0).any():
                    issues.append((fname, col, "negative_value", int((df[col] < 0).sum())))
                # Outlier check (z-score)
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                out_count = int((z_scores > 3).sum())
                if out_count > 0:
                    issues.append((fname, col, "outliers", out_count))
            else:
                # type check
                if not pd.api.types.is_string_dtype(df[col]):
                    issues.append((fname, col, "unexpected_type", str(df[col].dtype)))

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
