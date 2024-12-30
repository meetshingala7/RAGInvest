import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import psycopg2
import os
from datetime import datetime

# Pipeline for handling database operations
class PostgresPipeline:
    def __init__(self):
        # Database connection parameters from environment variables
        self.db_params = {
            'dbname': os.environ['DB_NAME'],
            'user': os.environ['DB_USER'],
            'password': os.environ['DB_PASSWORD'],
            'host': os.environ['DB_HOST'],
            'port': os.environ['DB_PORT']
        }
        
    def open_spider(self, spider):
        # Connect to database when spider starts
        self.conn = psycopg2.connect(**self.db_params)
        self.cur = self.conn.cursor()

    
    def close_spider(self, spider):
        # Close database connection when spider finishes
        self.cur.close()
        self.conn.close()
    
    def process_item(self, item, spider):
        # Insert data into database
        self.cur.execute("""
            INSERT INTO stocks (url, anchor_text)
            VALUES (%s, %s)
        """, (item['url'], item['text']))
        self.conn.commit()
        return item

class StockLinksSpider(CrawlSpider):
    name = 'stock_links'
    start_urls = []
    
    rules = (
        Rule(
            LinkExtractor(
                allow=[r'/stocks/.*-share-price-.*'],
                restrict_xpaths='//a',
                unique=True
            ),
            callback='parse_item',
            follow=True
        ),
    )
    
    def __init__(self, url=None, *args, **kwargs):
        super(StockLinksSpider, self).__init__(*args, **kwargs)
        if url:
            self.start_urls = [url]
    
    def parse_item(self, response):
        link_extractor = LinkExtractor(
            allow=[r'/stocks/.*-share-price-.*'],
            restrict_xpaths='//a'
        )
        
        for link in link_extractor.extract_links(response):
            anchor = response.xpath(f'//a[@href="{link.url}"]')
            yield {
                'url': link.url,
                'text': anchor.xpath('string()').get().strip(),
            }

# Settings (save in settings.py)
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1
COOKIES_ENABLED = False
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Add the PostgreSQL pipeline to your settings
ITEM_PIPELINES = {
    'your_project_name.pipelines.PostgresPipeline': 300
}