from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

# Ensure project root is on path so 'src' imports work when Airflow runs from dags/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.ingestion.ingest import ingest_csv, ingest_api, merge_all, run_dvc_versioning
from src.validation.validate import validate
from src.preprocessing.preprocess import preprocess
from src.feature_engineering.features import feature_engineering
from src.feature_store.export import export_to_feast_csv
from src.modeling.train import train_and_evaluate

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id="churn_pipeline_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    # --------------------------
    # Task 1: Ingest CSV + API, merge, DVC versioning
    # --------------------------
    def ingest_merge_version():
        ingest_csv()
        ingest_api()
        merge_all()
        run_dvc_versioning()

    ingest_task = PythonOperator(
        task_id="ingest_merge_version",
        python_callable=ingest_merge_version,
    )

    # --------------------------
    # Task 2: Data validation
    # --------------------------
    validate_task = PythonOperator(
        task_id="validate_data",
        python_callable=validate,
    )

    # --------------------------
    # Task 3: Preprocessing
    # --------------------------
    preprocess_task = PythonOperator(
        task_id="preprocess",
        python_callable=preprocess,
    )

    # --------------------------
    # Task 4: Feature engineering
    # --------------------------
    feature_engineering_task = PythonOperator(
        task_id="feature_engineering",
        python_callable=feature_engineering,
    )

    # --------------------------
    # Task 5: Export features to Feast
    # --------------------------
    export_task = PythonOperator(
        task_id="export_to_feast_csv",
        python_callable=export_to_feast_csv,
    )

    # --------------------------
    # Task 6: Train models
    # --------------------------
    train_task = PythonOperator(
        task_id="train_models",
        python_callable=train_and_evaluate,
    )

    # --------------------------
    # DAG dependencies
    # --------------------------
    ingest_task >> validate_task >> preprocess_task >> feature_engineering_task
    feature_engineering_task >> export_task
    feature_engineering_task >> train_task
    export_task >> train_task  # optional: ensures export finishes before training
