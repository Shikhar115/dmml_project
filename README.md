# dmml_project

<img width="1589" height="1010" alt="image" src="https://github.com/user-attachments/assets/672a481b-cc17-46c0-a2ab-86a65ec705b5" />


.
├─ churn_pipeline_dag.py          → Airflow DAG for orchestration (ingestion → validation → prep → feature eng → train)

├─ export_to_feast_csv.py         → Exports engineered features to CSV for Feast

├─ feature_repo/                  → Feast feature store configuration
│   ├─ feature_store.yaml
│   ├─ feature_views.py
│   └─ README.md                  → metadata of features (name, source, version)

├─ raw_data/                      → Versioned raw data (tracked with DVC)
│   └─ raw_churn_csv_*.csv

├─ clean_churn_csv.csv            → Cleaned dataset (tracked with DVC)

├─ transformed_churn.csv          → Engineered features exported for Feast (tracked with DVC)

├─ transformed_churn.db           → SQLite copy of engineered features

├─ test_feature_retrieval.py      → Sample script to fetch features from the Feast store

├─ CHANGELOG.md                   → Describes data version changes and timestamps

└─ VERSIONING_WORKFLOW.md         → Step-by-step instructions for updating dataset versions with DVC
