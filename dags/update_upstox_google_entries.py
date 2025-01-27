from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from airflow_tasks.postgres_tasks import fetch_latest_entries, update_postgres
from airflow_tasks.processing import process_upstox_gfin_updates

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
}

with DAG(
    dag_id = "check_stock_info",
    default_args = default_args,
    description = "DAG to check if there are any changes in Stock information from Google and Upstox URL.",
    schedule_interval = "0 2 * * *",
    start_date = days_ago(1),
    catchup = False,
    tags = ["Update Table"]
) as dag:
    # Task 1
    fetch_task = PythonOperator(
        task_id = "fetch_latest_entries",
        python_callable = fetch_latest_entries
    )
    
    process_rows_task = PythonOperator(
        task_id = "find_updates"
        python_callable = process_upstox_gfin_updates
    )

    update_task = PostgresOperator(
        task_id = "Insert Findings",
        postgress_conn_id = "my_postgres_conn",
        sql = "INSERT INTO <table-name> (<columns>) VALUES {{ ti.xcom_pull(task_ids='find_updates') }})"
    )

    fetch_task >> process_rows_task >> update_task