# dmml_project

<img width="1589" height="1010" alt="image" src="https://github.com/user-attachments/assets/672a481b-cc17-46c0-a2ab-86a65ec705b5" />


.
dmml_project/

├─ dags/

│  └─ churn_pipeline_dag.py

├─ src/

│  ├─ __init__.py

│  ├─ ingestion/

│  │  ├─ __init__.py

│  │  └─ ingest.py

│  ├─ validation/

│  │  ├─ __init__.py

│  │  └─ validate.py

│  ├─ preprocessing/

│  │  ├─ __init__.py

│  │  └─ preprocess.py

│  ├─ versioning/

│  │  ├─ __init__.py

│  │  └─ dvc_versioning.py

│  ├─ feature_engineering/

│  │  ├─ __init__.py

│  │  └─ features.py

│  └─ feature_store/

│     ├─ __init__.py

│     └─ export.py

├─ raw_data/                 # created at runtime by ingestion

├─ ingestion.log             # same log filename as before

└─ (your Telco CSV in repo root, same as before)

