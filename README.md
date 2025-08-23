4️⃣ Rebuild and start fresh if already present

Steps to run this cleanly on Windows

Stop and remove existing containers (to avoid conflicts):

docker-compose down 



After cleaning up, start from scratch:

docker compose build --no-cache

docker-compose up -d --build


Finally, open the Airflow webserver at:
http://localhost:8080

now loin with credentials

check---
Check the status of containers

Run:

docker ps -a


Look for airflow_scheduler and airflow containers. If the scheduler is Restarting or Exited, it won’t work.


# DMML Project – Telco Customer Churn Prediction

This repository implements a full end-to-end churn prediction pipeline for a telecom dataset, including data ingestion, validation, preprocessing, feature engineering, model training, and feature export. The pipeline is orchestrated with Airflow, versioned using DVC + Git, and trained models are logged with MLflow.

---

## Project Structure

dmml\_project/

├─ dags/

│  └─ churn\_pipeline\_dag.py  # Airflow DAG orchestrating the pipeline

├─ src/

│  ├─ ingestion/

│  │  └─ ingest.py                    # Ingest CSV/API and merge raw data

│  ├─ validation/

│  │  └─ validate.py                  # Data quality validation

│  ├─ preprocessing/

│  │  └─ preprocess.py                # Data preprocessing on merged CSV

│  ├─ versioning/

│  │  └─ dvc\_versioning.py            # DVC versioning scripts

│  ├─ feature\_engineering/

│  │  └─ features.py                  # Derived feature creation

│  ├─ feature\_store/

│  │  └─ export.py                    # Export features to Feast CSV

│  └─ modeling/

│     └─ train.py                     # Train 7 ML models + ROC/AUC



├─ data/

│  └─ processed/
│     └─ merged\_churn.csv              # Merged raw CSV

│     └─ clean\_churn.csv               # Preprocessed CSV

│  └─ raw\_data/                        # Raw CSV/API files created at runtime

├─ models/                             # Trained model pickle files

├─ reports/

│  ├─ plots/                           # Confusion matrix, ROC curve, classification report

│  ├─ eda/

│  ├─ model\_performance\_.txt

│  └─ model\_performance\_.csv

├─ ingestion.log                        # Logging for ingestion/preprocessing

├─ modeling.log                         # Logging for modeling

├─ requirements.txt

├─ Dockercompose

├─ dockerfile

├─ constraints.txt

└─ README.md                            # Project documentation


---

