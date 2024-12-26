import psycopg2
from dotenv import load_dotenv, find_dotenv
import os
import requests as request
import time


def insert_rest_details(val):
    print(val)
    API = f"https://restcountries.com/v3.1/name/{val}"
    response = request.get(API)
    rest_country_data = response.json()

    alpha2_code = rest_country_data[0]['cca2'] # String
    alpha3_code = rest_country_data[0]['cca3'] # String
    currency_code = list(rest_country_data[0]['currencies'].keys())[0] # String
    currency_name = list((rest_country_data[0]['currencies'].values()))[0]['name'] # String
    capital = rest_country_data[0]['capital'][0] # String
    continent = rest_country_data[0]['region'] # String
    region = rest_country_data[0]['subregion'] # String
    population = rest_country_data[0]['population'] # Integer
    timezones = rest_country_data[0]['timezones'] # List

    # if country and latitude and longitude:
    query = """
    INSERT INTO country 
        (Alpha2_code, Alpha3_code, Continent, Region, Capital, Population, Currency_code, Currency_Name, Time_Zones) 
    VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(query, (alpha2_code, alpha3_code, continent, region, capital, population, currency_code, currency_name, timezones))
    conn.commit()
    print(val)
    return None



if __name__ == "__main__":
    _ = load_dotenv(find_dotenv())

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
        insert_rest_details(row[0])
        time.sleep(2)

    if cur:
        cur.close()
    if conn:
        conn.close()









