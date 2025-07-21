from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime
import logging

default_args = {
    "owner": "airflow",
    "retries": 1,
}

def download_file():
    logging.info("📥 Simulating file download...")

def process_file():
    logging.info("🧪 Processing file: parsing, cleaning...")

def load_to_db():
    logging.info("📦 File loaded to database successfully.")

# ✅ Fetch schedule interval from Airflow Variable (defaulting to None if not set)
schedule = Variable.get("dynamic_schedule_dag", default_var=None)

with DAG(
    dag_id="dynamic_schedule_dag",
    description="Simulates downloading and loading file to DB",
    start_date=datetime(2024, 1, 1),
    schedule_interval=schedule,
    default_args=default_args,
    catchup=False,
) as dag:

    t1 = PythonOperator(task_id="download_file", python_callable=download_file)
    t2 = PythonOperator(task_id="process_file", python_callable=process_file)
    t3 = PythonOperator(task_id="load_to_db", python_callable=load_to_db)

    t1 >> t2 >> t3
