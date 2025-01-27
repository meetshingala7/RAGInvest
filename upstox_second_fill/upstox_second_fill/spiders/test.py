import scrapy
from bs4 import BeautifulSoup
import json

class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["upstox.com"]
    start_urls = ["https://upstox.com/stocks/20-microns-ltd-share-price/INE144J01027/"]

    def parse(self, response):
        
        soup = BeautifulSoup(response.text, 'html.parser')

        stock_symbol = soup.find("p", class_ = "text-[13px] font-medium leading-5 text-[#6A6A6A]").text
        company_sector = soup.find("span", class_ = "text-sm font-normal text-[#101010] group-hover:text-[#41246E]").text
        data_div = soup.find_all("td", class_ = "flex items-center gap-2 py-2")

        print("stock_symbol_bs4", stock_symbol)
        print("company_sector", company_sector)
        # print("data_div", data_div)

        
        shareholding_pattern = {}
        for data in data_div:
            value = data.find("p", class_ = "text-[13px] font-medium leading-5 text-[#6A6A6A] md:text-sm").text
            # print(value)
            value = value.split("(")
            shareholder = value[0].strip(" ")
            percentage = value[1].replace("%)", "")
            shareholding_pattern[shareholder] = float(percentage)
            # print(shareholder, percentage, float(percentage))
            # print(x.text)

        # print(shareholding_pattern)

        yield {
            "stock_symbol": stock_symbol,
            "company_sector": company_sector,
            "shareholding_pattern": shareholding_pattern
        }