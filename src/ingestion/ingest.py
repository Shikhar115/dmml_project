import os
import logging
from datetime import datetime
import pandas as pd
import requests

# Logging configuration
logging.basicConfig(filename="ingestion.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

RAW_DIR = "raw_data"
MERGED_FILE = "data/processed/merged_churn.csv"
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(os.path.dirname(MERGED_FILE), exist_ok=True)

# Store raw file paths dynamically
raw_files = []

def ingest_csv():
    df = pd.read_csv("Telco-Customer-Churn.csv")  # adjust path if needed
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = f"{RAW_DIR}/raw_churn_csv_{ts}.csv"
    df.to_csv(raw_path, index=False)
    raw_files.append(raw_path)
    logging.info(f"CSV ingested successfully: {raw_path}")
    return df

def ingest_api():
    url = "https://raw.githubusercontent.com/AnalyticsKnight/youtube/master/data/telecom_churn.json"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    df = pd.DataFrame(resp.json())
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = f"{RAW_DIR}/raw_churn_api_{ts}.csv"
    df.to_csv(raw_path, index=False)
    raw_files.append(raw_path)
    logging.info(f"API ingested successfully: {raw_path}")
    return df

def merge_all():
    """Merge all ingested DataFrames into one CSV"""
    merged_df = pd.DataFrame()
    for file_path in raw_files:
        df = pd.read_csv(file_path)
        merged_df = pd.concat([merged_df, df], ignore_index=True)
    merged_df.to_csv(MERGED_FILE, index=False)
    logging.info(f"Merged CSV saved at: {MERGED_FILE}")
    return MERGED_FILE

def run_dvc_versioning():
    """Automatically run DVC versioning after ingestion"""
    import subprocess
    versioning_script = os.path.join("src", "versioning", "dvc_versioning.py")
    if os.path.exists(versioning_script):
        subprocess.run(f"python {versioning_script}", shell=True, check=True)
        logging.info("DVC versioning executed successfully.")
    else:
        logging.warning(f"DVC versioning script not found: {versioning_script}")

if __name__ == "__main__":
    # Step 1: Ingest CSV + API
    ingest_csv()
    ingest_api()

    # Step 2: Merge all raw files
    merge_all()

    # Step 3: Run DVC versioning automatically
    run_dvc_versioning()
