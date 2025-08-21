from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

# Ensure project root is on path so 'src' imports work when Airflow runs from dags/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.ingestion.ingest import ingest_csv, ingest_api
from src.validation.validate import validate
from src.versioning.dvc_versioning import dvc_versioning
from src.preprocessing.preprocess import preprocess_csv, preprocess_api
from src.feature_engineering.features import feature_engineering
from src.feature_store.export import export_to_feast_csv

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

    ingest_csv_task = PythonOperator(
        task_id="ingest_csv",
        python_callable=ingest_csv,
    )

    ingest_api_task = PythonOperator(
        task_id="ingest_api",
        python_callable=ingest_api,
    )

    validate_task = PythonOperator(
        task_id="validate_data",
        python_callable=validate,
    )

    dvc_versioning_task = PythonOperator(
        task_id="dvc_versioning",
        python_callable=dvc_versioning,
    )

    preprocess_csv_task = PythonOperator(
        task_id="preprocess_csv",
        python_callable=preprocess_csv,
    )

    preprocess_api_task = PythonOperator(
        task_id="preprocess_api",
        python_callable=preprocess_api,
    )

    feature_engineering_task = PythonOperator(
        task_id="feature_engineering",
        python_callable=feature_engineering,
    )

    export_to_feast_task = PythonOperator(
        task_id="export_to_feast_csv",
        python_callable=export_to_feast_csv,
    )

    # ----- Dependencies (exactly the same as your original) -----
    [ingest_csv_task, ingest_api_task] >> validate_task
    validate_task >> dvc_versioning_task
    dvc_versioning_task >> [preprocess_csv_task, preprocess_api_task]
    [preprocess_csv_task, preprocess_api_task] >> feature_engineering_task
    feature_engineering_task >> export_to_feast_task
