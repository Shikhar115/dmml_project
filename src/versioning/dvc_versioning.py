import logging
import pandas as pd

logging.basicConfig(filename="ingestion.log", level=logging.INFO)

def feature_engineering():
    """
    Create derived / aggregated features and store results in SQLite.
    """
    import sqlite3
    df = pd.read_csv("clean_churn_csv.csv")

    # Example engineered features (exactly as before)
    df['total_spend'] = df['MonthlyCharges'] * df['tenure']
    df['tenure_years'] = df['tenure'] / 12.0
    df['long_term_customer'] = (df['tenure'] > 24).astype(int)

    # Save to SQLite
    con = sqlite3.connect("transformed_churn.db")
    df.to_sql("customer_features", con, if_exists="replace", index=False)
    con.close()

    logging.info("Feature engineering complete. Loaded into transformed_churn.db")
