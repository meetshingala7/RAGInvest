import psycopg2
from dotenv import load_dotenv, find_dotenv
import os
import json

_ = load_dotenv(find_dotenv())


def get_countries_name():
    """
    Returns a list of countries names
    """
    conn = psycopg2.connect(
        dbname = os.environ["PG_DB_NAME"],
        user = os.environ["PG_DB_USER"],
        password = os.environ["PG_DB_PSWD"],
        host = os.environ["PG_DB_IP"],
        port = 5432
    )

    cur = conn.cursor()

    query = """
    SELECT
        countryid AS uuid,
        country_name AS name
    FROM country;
    """

    cur.execute(query)
    rows = cur.fetchall()
    countries = []
    for row in rows:
        countries.append({"uuid":row[0], "name": row[1]})
    
    if cur:
        cur.close()

    if conn:
        conn.close()

    with open("/home/meet.shingala/Desktop/Client_Project/LinkedIn_internal/RAGInvest_Flask/RAGInvest/countries.json", "w") as f:
        json.dump(countries, f)


get_countries_name()