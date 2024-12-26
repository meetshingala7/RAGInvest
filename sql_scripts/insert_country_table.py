import pandas as pd
import numpy as np
import psycopg2
from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv())

df = pd.read_csv("sql_scripts/Data/countries.csv")
# print(df.head())
na_country_index = list(df[df['country'].isnull()].index)
na_latitude_index = list(df[df['latitude'].isnull()].index)

na_index = na_country_index + na_latitude_index

df = df.drop(na_index)

print('1')
conn = psycopg2.connect(
    dbname = os.environ["PG_DB_NAME"],
    user = os.environ["PG_DB_USER"],
    password = os.environ["PG_DB_PSWD"],
    host = os.environ["PG_DB_IP"],
    port = 5432
)

# Create a cursor
cur = conn.cursor()
print('2')

def insert_country_lat_lon(val):
    print(val)
    country = val['name']
    latitude = val['latitude']
    longitude = val['longitude']
    if country and latitude and longitude:
        print(country, latitude, longitude)
        query = "INSERT INTO country (Country_Name, Latitude, Longitude) VALUES (%s, %s, %s)"
        cur.execute(query, (country, latitude, longitude, ))
        conn.commit()
        return None
    print(val)

df.apply(insert_country_lat_lon, axis = 1)
if cur:
    cur.close()
if conn:
    conn.close()