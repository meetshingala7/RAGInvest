from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from airflow_tasks.postgres_tasks import fetch_latest_entries
from airflow_tasks.processing import process_updates

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
    # Task 1: Fetch the latest values from DB from stock_information table
    fetch_task = PythonOperator(
        task_id = "fetch_latest_entries",
        python_callable = fetch_latest_entries
    )
    
    # Task 2: Process the rows and look for updates
    process_rows_task = PythonOperator(
        task_id = "find_updates",
        python_callable = process_updates
    )

    # Task 3: Update the findings in the run in to the DB
    update_task = PostgresOperator(
        task_id = "Insert_Findings",
        postgres_conn_id = "my_postgres_conn",
        sql = "INSERT INTO <table-name> (<columns>) VALUES {{ ti.xcom_pull(task_ids='find_updates') }})"
    )

    # Creating the dependency
    fetch_task >> process_rows_task >> update_task