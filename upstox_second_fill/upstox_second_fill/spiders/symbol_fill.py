import scrapy
from bs4 import BeautifulSoup
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
        
        return start_urls


    def start_requests(self):
        start_urls = self.get_start_urls()
        
        for url in start_urls:
            print(url)
            yield scrapy.Request(url[1], self.parse)

    def parse(self, response):
        stock_symbol = response.xpath("//p[contains(@class, 'text-[13px]') and contains(@class, 'font-medium') and contains(@class, 'leading-5')]/text()").get()
        
        company_sector = response.xpath("//span[contains(@class, 'text-sm') and contains(@class, 'font-normal')] and contains(@class, 'text-[#101010]') and contains(@class, 'group-hover:text-[#41246E]')").get()

        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all("p", class_="text-[13px] font-medium leading-5 text-[#6A6A6A] md:text-sm")
        for i in data:
            print(i.text)

        yield {
            "x": stock_symbol,
            'y': company_sector
        }