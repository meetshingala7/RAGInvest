import psycopg2
import pandas as pd
from datetime import datetime
import subprocess
import os

def fetch_latest_entries(ti):
    try:
        conn = psycopg2.connect(
            dbname = os.environ["PG_DB_NAME"],
            user = os.environ["PG_DB_USER"],
            password = os.environ["PG_DB_PSWD"],
            host = os.environ["PG_DB_IP"],
            port = 5432
        )

        curr = conn.cursor()

        query = """
        SELECT 
            * 
        FROM 
            stock_information
        """
        curr.execute(query)

        all_rows = curr.fetchall()

        column_names = [desc[0] for desc in curr.description]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"fetch_latest_entries_{timestamp}.parquet"
        result = subprocess.run(['pwd'], stdout=subprocess.PIPE, text=True).stdout.strip()
        directory = 'Data'
        if os.path.exists(directory):
            os.makedirs(directory)
        file_path = f"{result}/{directory}/{file_name}"

        df = pd.DataFrame(all_rows, columns = column_names)
        
        df.to_parquet(f"{file_path}", index = False)

        ti.xcom_push(key = "file_path", value = f"{file_path}")
    except Exception as e:
        conn.rollback()
    else:
        # Creating File Name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"fetch_latest_entries_{timestamp}.parquet"
        result = subprocess.run(['pwd'], stdout=subprocess.PIPE, text=True).stdout.strip()
        directory = 'Data'
        if os.path.exists(directory):
            os.makedirs(directory)
        file_path = f"{result}/{directory}/{file_name}"

        df = pd.DataFrame(all_rows, columns = column_names)
        
        df.to_parquet(f"{file_path}", index = False)

        ti.xcom_push(key = "file_path", value = f"{file_path}")
    finally:
        if conn:
            conn.close()
        if curr:
            curr.close()
        