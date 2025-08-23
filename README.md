4️⃣ Rebuild and start fresh

Steps to run this cleanly on Windows

Stop and remove existing containers (to avoid conflicts):

docker-compose down 

After cleaning up, start from scratch:

docker compose build --no-cache

docker-compose up -d --build


Then initialize the database and create admin user:

docker-compose run airflow airflow db init
docker-compose run airflow airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com

for ex---

docker-compose exec airflow airflow users create --username churnproject --password dmml --firstname shikhar --lastname nigam --role Admin --email shikharnigam22@gmail.com


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

├─ raw\_data/                           # Raw CSV/API files created at runtime

├─ data/

│  └─ processed/
│     └─ merged\_churn.csv              # Merged raw CSV

│     └─ clean\_churn.csv               # Preprocessed CSV

├─ models/                             # Trained model pickle files

├─ reports/

│  ├─ plots/                           # Confusion matrix, ROC curve, classification report

│  ├─ model\_performance\_.txt

│  └─ model\_performance\_.csv

├─ ingestion.log                        # Logging for ingestion/preprocessing

├─ modeling.log                         # Logging for modeling

└─ README.md                            # Project documentation


---

## Pipeline Overview

The pipeline orchestrates the following steps:

1. **Data Ingestion & Merging**

   * Ingest CSV (`Telco-Customer-Churn.csv`) and API JSON.
   * Merge into a single CSV (`data/processed/merged_churn.csv`).
   * Version raw + merged data using DVC.

2. **Data Validation**

   * Checks for missing values, duplicates, invalid types, and outliers.
   * Generates PDF data quality reports.

3. **Preprocessing**

   * Imputes missing values for numeric and categorical features.
   * One-hot encodes categorical columns.
   * Standardizes numeric features.
   * Saves cleaned CSV (`data/processed/clean_churn.csv`).

4. **Feature Engineering**

   * Creates derived features:

     * `total_spend = MonthlyCharges * tenure`
     * `tenure_years = tenure / 12`
     * `long_term_customer = (tenure > 24)`
   * Stores features in SQLite database (`transformed_churn.db`).

5. **Feature Export**

   * Exports engineered features from SQLite to Feast-compatible CSV (`transformed_churn.csv`).
   * Adds `event_timestamp`.

6. **Model Training**

   * Trains 7 models: Logistic Regression, Random Forest, Gradient Boosting, SVM, Decision Tree, KNN, XGBoost.
   * Evaluates metrics: Accuracy, Precision, Recall, F1-score, ROC/AUC.
   * Saves best model, performance reports, confusion matrices, and ROC curves.

---

## Pipeline DAG (Simple ASCII Diagram)

```
Ingest CSV/API -> Merge -> DVC
          |
          v
     Validate Data
          |
          v
      Preprocess
          |
          v
  Feature Engineering
       /       \
      v         v
Export to Feast  Train Models
```

**Legend:**

* Data flows from top to bottom.
* Feature Engineering splits into feature export and model training.

---

## DVC Workflow

1. **Initialize DVC**

```
git init
dvc init
```

2. **Add raw or merged datasets**

```
dvc add data/processed/merged_churn.csv
git add data/processed/merged_churn.csv.dvc .gitignore
git commit -m "Add merged churn dataset"
```

3. **Push to remote (optional)**

```
dvc remote add -d myremote gdrive://<folder-id>
dvc push
```

4. **Version updates**

* Re-run pipeline → updated CSV → `dvc add` → commit → DVC push.
* Use Git tags to mark dataset/model versions.

---

## Airflow DAG

* DAG: `churn_pipeline_dag`
* Flow:

```
Ingest CSV/API -> Merge -> DVC
          |
      Validate Data
          |
       Preprocess
          |
  Feature Engineering
       /       \
Export to Feast  Train Models
```

* Tasks are implemented as PythonOperators calling functions from `src/`.

---

## Usage

1. **Run DAG in Airflow**

```
airflow db init
airflow webserver --port 8080
airflow scheduler
```

* Trigger `churn_pipeline_dag` from the Airflow UI or CLI.

2. **Check Logs**

* `ingestion.log` → ingestion/preprocessing.
* `modeling.log` → training metrics and errors.

3. **Explore Models & Reports**

* `models/` → saved models.
* `reports/` → evaluation metrics and plots.
* `data/processed/` → merged & cleaned CSV.
* `transformed_churn.db` → engineered features.
* `transformed_churn.csv` → CSV for Feast feature store.

---

## Dependencies

* Python 3.8+
* pandas, numpy, scikit-learn, xgboost, matplotlib, seaborn
* mlflow, airflow
* DVC
* SQLite3

---

## Contact / Maintainer

* Project maintained by \[Your Name].
* For questions or issues, please open a GitHub issue or contact via email.
