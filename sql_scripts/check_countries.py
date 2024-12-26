import psycopg2
from dotenv import load_dotenv, find_dotenv
import os
import requests as request
import time


def insert_rest_details(val):
    API = f"https://restcountries.com/v3.1/name/{val}"
    response = request.get(API)
    try:
        print(val, response.status_code, response.json()[0]['cca2'])
        return None
    except KeyError as e:
        print(str(e))
        print(val, response.status_code)
        return val
        




if __name__ == "__main__":
    _ = load_dotenv(find_dotenv())

    not_found = set()

    conn = psycopg2.connect(
        dbname = os.environ["PG_DB_NAME"],
        user = os.environ["PG_DB_USER"],
        password = os.environ["PG_DB_PSWD"],
        host = os.environ["PG_DB_IP"],
        port = 5432
    )

    # Create a cursor
    cur = conn.cursor()

    query = """
    SELECT
        COUNTRY_NAME
    FROM
        postgres.public.country;
    """

    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        not_found.add(insert_rest_details(row[0]))
        time.sleep(1)
    print(not_found)
    if cur:
        cur.close()
    if conn:
        conn.close()

