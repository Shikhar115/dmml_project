import os
import logging
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

logging.basicConfig(filename="ingestion.log", level=logging.INFO)

MERGED_FILE = "data/processed/merged_churn.csv"
CLEAN_FILE = "data/processed/clean_churn.csv"

def preprocess():
    """
    Preprocess the merged churn CSV:
    - Impute missing numeric & categorical values
    - One-hot encode categorical columns
    - Standardize numeric columns
    - Save cleaned CSV for downstream tasks
    """
    if not os.path.exists(MERGED_FILE):
        raise FileNotFoundError(f"Merged CSV not found: {MERGED_FILE}")

    df = pd.read_csv(MERGED_FILE)

    # Separate numeric & categorical
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    cat_cols = df.select_dtypes(exclude=['float64', 'int64']).columns

    # Impute missing values
    df[num_cols] = SimpleImputer(strategy='mean').fit_transform(df[num_cols])
    df[cat_cols] = SimpleImputer(strategy='most_frequent').fit_transform(df[cat_cols])

    # One-hot encode categorical columns
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    # Standardize numeric columns
    df[num_cols] = StandardScaler().fit_transform(df[num_cols])

    # Save cleaned CSV
    os.makedirs(os.path.dirname(CLEAN_FILE), exist_ok=True)
    df.to_csv(CLEAN_FILE, index=False)
    logging.info(f"Preprocessing complete. Cleaned CSV saved at {CLEAN_FILE}")
