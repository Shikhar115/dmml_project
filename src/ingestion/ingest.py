import os
import logging
from datetime import datetime
import pandas as pd
import requests

# Logging
logging.basicConfig(filename="ingestion.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

RAW_DIR = "./raw_data"
MERGED_FILE = "./processed/merged_churn.csv"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(os.path.dirname(MERGED_FILE), exist_ok=True)

# Store paths of ingested raw files
raw_files = []

def ingest_csv():
    df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
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
    logging.info(f"All ingested files merged into: {MERGED_FILE}")

if __name__ == "__main__":
    df_csv = ingest_csv()
    df_api = ingest_api()
    merge_all()
