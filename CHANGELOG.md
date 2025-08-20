# Dataset Change Log

## v1.0.0 — Initial Commit
- Source: WA_Fn-UseC_-Telco-Customer-Churn.csv + API data
- Timestamp: 2025-08-20
- Description: Initial ingestion of raw churn data (CSV + API) and transformation into clean & feature-engineered datasets.
- Files tracked: 
  - raw_data/raw_churn_csv_*.csv
  - raw_data/raw_churn_api_*.csv
  - clean_churn_csv.csv
  - clean_churn_api.csv
  - transformed_churn.db

---

## v1.1.0 — Example Future Update
- Source: Additional monthly churn dataset added
- Timestamp: YYYY-MM-DD
- Description: Ingested new month of churn data, re-ran preprocessing & feature engineering
- Files tracked:
  - raw_data/raw_churn_csv_new.csv
  - clean_churn_csv_v2.csv
  - transformed_churn.db (updated)
