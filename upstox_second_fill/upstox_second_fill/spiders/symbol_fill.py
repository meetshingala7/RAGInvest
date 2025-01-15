import scrapy
import psycopg2
import os
from dotenv import load_dotenv, find_dotenv


class SymbolFillSpider(scrapy.Spider):
    name = "symbol_fill"
    allowed_domains = ["upstox.com"]
    
    def get_start_urls(self):
        _ = load_dotenv(find_dotenv())
        
        self.conn = psycopg2.connect(
            dbname = os.environ["PG_DB_NAME"],
            user = os.environ["PG_DB_USER"],
            password = os.environ["PG_DB_PSWD"],
            host = os.environ["PG_DB_IP"],
            port = 5432
        )
        self.curr = self.conn.cursor()
        
        query = """
        SELECT
            Id,
            upstox_url
        FROM
            postgres.public.stock_information;
        """

        self.curr.execute(query)
        
        start_urls = self.curr.fetchall()
        print(start_urls[0])
        return start_urls


    def start_requests(self):
        start_urls = self.get_start_urls()
        
        for url in start_urls[:2]:
            print(url)
            yield scrapy.Request(url[1], self.parse)

    def parse(self, response):
        x = response.xpath("//p[contains(@class, 'text-[13px]') and contains(@class, 'font-medium') and contains(@class, 'leading-5')]/text()").get()
        yield {
            "x": x
        }