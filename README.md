# DMML Project – Telco Customer Churn Prediction

This repository implements a **full end-to-end churn prediction pipeline** for a telecom dataset, including **data ingestion, validation, preprocessing, feature engineering, model training, and feature export**. The pipeline is orchestrated with **Airflow**, versioned using **DVC + Git**, and trained models are logged with **MLflow**.

---

## **Project Structure**

dmml_project/

├─ dags/

│ └─ churn_pipeline_dag.py # Airflow DAG orchestrating the pipeline

├─ src/

│ ├─ ingestion/

│ │ └─ ingest.py # Ingest CSV/API and merge raw data

│ ├─ validation/

│ │ └─ validate.py # Data quality validation

│ ├─ preprocessing/

│ │ └─ preprocess.py # Data preprocessing on merged CSV

│ ├─ versioning/

│ │ └─ dvc_versioning.py # DVC versioning scripts

│ ├─ feature_engineering/

│ │ └─ features.py # Derived feature creation

│ ├─ feature_store/

│ │ └─ export.py # Export features to Feast CSV

│ └─ modeling/

│ └─ train.py # Train 7 ML models + ROC/AUC

├─ raw_data/ # Raw CSV/API files created at runtime

├─ data/

│ └─ processed/

│ └─ merged_churn.csv # Merged raw CSV

│ └─ clean_churn.csv # Preprocessed CSV

├─ models/ # Trained model pickle files

├─ reports/

│ ├─ plots/ # Confusion matrix, ROC curve, classification report

│ ├─ model_performance_.txt

│ └─ model_performance_.csv

├─ ingestion.log # Logging for ingestion/preprocessing

├─ modeling.log # Logging for modeling

└─ README.md # Project documentation

markdown
Copy
Edit

---

## **Pipeline Overview**

The pipeline orchestrates the following steps:

1. **Data Ingestion & Merging**
   - Ingest CSV (`Telco-Customer-Churn.csv`) and API JSON.
   - Merge into a single CSV (`data/processed/merged_churn.csv`).
   - Version raw + merged data using **DVC**.

2. **Data Validation**
   - Checks for missing values, duplicates, invalid types, and outliers.
   - Generates PDF data quality reports.

3. **Preprocessing**
   - Imputes missing values for numeric and categorical features.
   - One-hot encodes categorical columns.
   - Standardizes numeric features.
   - Saves cleaned CSV (`data/processed/clean_churn.csv`).

4. **Feature Engineering**
   - Creates derived features:
     - `total_spend = MonthlyCharges * tenure`
     - `tenure_years = tenure / 12`
     - `long_term_customer = (tenure > 24)`
   - Stores features in SQLite database (`transformed_churn.db`).

5. **Feature Export**
   - Exports engineered features from SQLite to **Feast-compatible CSV** (`transformed_churn.csv`).
   - Adds `event_timestamp`.

6. **Model Training**
   - Trains 7 models:
     - Logistic Regression, Random Forest, Gradient Boosting, SVM, Decision Tree, KNN, XGBoost
   - Evaluates metrics: Accuracy, Precision, Recall, F1-score, ROC/AUC
   - Saves:
     - Best model (`models/<best_model_name>_churn_model.pkl`)
     - Performance reports (`reports/`)
     - Confusion matrix, ROC curve plots

---

## **Pipeline DAG (Simple ASCII Diagram)**

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
/
v v
Export to Feast Train Models

yaml
Copy
Edit

**Legend:**  
- Data flows from top to bottom.  
- Feature Engineering splits into feature export and model training.

---

## **DVC Workflow**

1. **Initialize DVC**
```bash
git init
dvc init
Add raw or merged datasets

bash
Copy
Edit
dvc add data/processed/merged_churn.csv
git add data/processed/merged_churn.csv.dvc .gitignore
git commit -m "Add merged churn dataset"
Push to remote (optional)

bash
Copy
Edit
dvc remote add -d myremote gdrive://<folder-id>
dvc push
Version updates

Re-run pipeline → updated CSV → dvc add → commit → DVC push

Use Git tags to mark dataset/model versions.

Airflow DAG
DAG: churn_pipeline_dag

Flow:

rust
Copy
Edit
Ingest CSV/API -> Merge -> DVC
          |
      Validate Data
          |
       Preprocess
          |
  Feature Engineering
       /       \
Export to Feast  Train Models
Tasks are implemented as PythonOperators calling functions from src/.

Usage
Run DAG in Airflow

bash
Copy
Edit
airflow db init
airflow webserver --port 8080
airflow scheduler
Trigger churn_pipeline_dag from the Airflow UI or CLI.

Check Logs

ingestion.log → ingestion/preprocessing

modeling.log → training metrics and errors

Explore Models & Reports

models/ → saved models

reports/ → evaluation metrics and plots

data/processed/ → merged & cleaned CSV

transformed_churn.db → engineered features

transformed_churn.csv → CSV for Feast feature store

Dependencies
Python 3.8+

pandas, numpy, scikit-learn, xgboost, matplotlib, seaborn

mlflow, airflow

DVC

SQLite3

Contact / Maintainer
Project maintained by [Your Name]

For questions or issues, please open a GitHub issue or contact via email.
