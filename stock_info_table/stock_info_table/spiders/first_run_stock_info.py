import scrapy
from stock_info_table.items import StockInfoTableItem
from stock_info_table.itemloaders import StockInfoTableItemLoader 
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class FirstRunStockInfoSpider(scrapy.Spider):
    name = "first_run_stock_info"
    allowed_domains = ["upstox.com"]
    start_urls = ["https://upstox.com/stocks-market/share-market-listed-company-in-india/"]

    def parse(self, response):
        table_rows = response.css('div.stocks-list-wraper table tr a').getall()
        netloc = urlparse(response.url).netloc

        for a_tag in table_rows:
            urls = StockInfoTableItemLoader(item=StockInfoTableItem(), selector=a_tag)
            # urls.add_css('full_name', netloc + '::text')
            # urls.add_css('relative_url', '::attr(href)')
            soup = BeautifulSoup(a_tag, 'html.parser')
            a_tag = soup.find('a')
            full_name = a_tag.text.strip()
            relative_url = netloc + a_tag.get('href')

            urls.add_value('full_name', full_name)
            urls.add_value('relative_url', relative_url)
            yield urls.load_item()
            
