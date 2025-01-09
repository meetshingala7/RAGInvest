# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2
from dotenv import load_dotenv, find_dotenv
import os

class Insert_to_PGDB_Pipeline(object):
    
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        _ = load_dotenv(find_dotenv())
        self.conn = psycopg2.connect(
            dbname = os.environ["PG_DB_NAME"],
            user = os.environ["PG_DB_USER"],
            password = os.environ["PG_DB_PSWD"],
            host = os.environ["PG_DB_IP"],
            port = 5432
        )
        self.curr = self.conn.cursor()

    def store_in_db(self, item):
        try:
            query = """
            INSERT INTO stock_information (full_name, upstox_url, version_no) VALUES (%s, %s, %s)
            """
            self.curr.execute(query, (item['full_name'], item['relative_url'], 1))
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def process_item(self, item, spider):
        self.store_in_db(item)
        return item
    