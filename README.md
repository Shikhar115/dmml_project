# dmml_project



.
dmml_project/

├─ dags/
│   └─ churn_pipeline_dag.py

├─ src/
│   ├─ __init__.py

│   ├─ ingestion/

│   │   ├─ __init__.py

│   │   └─ ingest.py

│   ├─ validation/

│   │   ├─ __init__.py

│   │   └─ validate.py

│   ├─ preprocessing/

│   │   ├─ __init__.py

│   │   └─ preprocess.py

│   ├─ versioning/

│   │   ├─ __init__.py

│   │   └─ dvc_versioning.py

│   ├─ feature_engineering/

│   │   ├─ __init__.py

│   │   └─ features.py

│   ├─ feature_store/

│   │   ├─ __init__.py

│   │   └─ export.py

│   └─ modeling/

│       ├─ __init__.py

│       └─ train.py      # (latest training script with 7 models + ROC/AUC)

├─ raw_data/      # created at runtime by ingestion

│   └─ Telco-Customer-Churn.csv (copied here after ingestion)

├─ data/

│   └─ processed/

│       └─ clean_churn.csv   # after preprocessing & feature engineering

├─ models/

│   └─ <best_model_name>_churn_model.pkl   # saved model

├─ reports/

│   ├─ plots/

│   │   ├─ <Model>_confusion_matrix.png

│   │   ├─ <Model>_roc_curve.png

│   │   └─ <Model>_classification_report.txt

│   ├─ model_performance_<timestamp>.txt

│   └─ model_performance_<timestamp>.csv

├─ ingestion.log

├─ modeling.log

└─ (Telco CSV in repo root if you kept original)

<img width="1589" height="1010" alt="image" src="https://github.com/user-attachments/assets/672a481b-cc17-46c0-a2ab-86a65ec705b5" />


