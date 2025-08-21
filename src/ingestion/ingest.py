import os
import logging
from datetime import datetime
import pandas as pd
import requests

# replicate original logging target
logging.basicConfig(filename="ingestion.log", level=logging.INFO)

def ingest_csv():
    df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = f"./raw_data/raw_churn_csv_{ts}.csv"
    os.makedirs("./raw_data", exist_ok=True)
    df.to_csv(raw_path, index=False)
    logging.info(f"CSV ingested successfully: {raw_path}")

def ingest_api():
    url = "https://raw.githubusercontent.com/AnalyticsKnight/youtube/master/data/telecom_churn.json"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    df = pd.DataFrame(resp.json())
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = f"./raw_data/raw_churn_api_{ts}.csv"
    os.makedirs("./raw_data", exist_ok=True)
    df.to_csv(raw_path, index=False)
    logging.info(f"API ingested successfully: {raw_path}")
