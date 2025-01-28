import pandas as pd


def process_upstox(ti):
    pass

def process_google_finance(ti):
    pass

def process_updates(ti):
    file_path = ti.xcom_pull(task_ids = "fetch_latest_entries", key = "file_path")
    try:
        file_path = "abc.parquet"
        df = pd.read_parquet(file_path)
        df.apply(lambda row: process_upstox(row), axis = 1)
    except FileNotFoundError as fnfe:
        pass
    except Exception as e:
        pass

