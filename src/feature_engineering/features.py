import logging
import pandas as pd
import sqlite3

logging.basicConfig(filename="ingestion.log", level=logging.INFO)

CLEAN_FILE = "data/processed/clean_churn.csv"
TRANSFORMED_DB = "transformed_churn.db"

def feature_engineering():
    """
    Create derived / aggregated features from preprocessed churn data
    and store results in SQLite database.
    """
    if not os.path.exists(CLEAN_FILE):
        raise FileNotFoundError(f"Clean CSV not found: {CLEAN_FILE}")

    df = pd.read_csv(CLEAN_FILE)

    # Example engineered features
    df['total_spend'] = df['MonthlyCharges'] * df['tenure']
    df['tenure_years'] = df['tenure'] / 12.0
    df['long_term_customer'] = (df['tenure'] > 24).astype(int)

    # Save to SQLite
    con = sqlite3.connect(TRANSFORMED_DB)
    df.to_sql("customer_features", con, if_exists="replace", index=False)
    con.close()

    logging.info(f"Feature engineering complete. Loaded into {TRANSFORMED_DB}")
