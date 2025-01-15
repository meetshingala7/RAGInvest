import scrapy
from bs4 import BeautifulSoup


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["upstox.com"]
    start_urls = ["https://upstox.com/stocks/20-microns-ltd-share-price/INE144J01027/"]

    def parse(self, response):
        stock_symbol = response.xpath("//p[contains(@class, 'text-[13px]') and contains(@class, 'font-medium') and contains(@class, 'leading-5')]/text()").get()
        
        company_sector = response.xpath("//span[contains(@class, 'text-sm') and contains(@class, 'font-normal')] and contains(@class, 'text-[#101010]') and contains(@class, 'group-hover:text-[#41246E]')").get()

        soup = BeautifulSoup(response.text, 'html.parser')
        data_div = soup.find_all("td", class_ = "flex items-center gap-2 py-2")
        print("data_div", data_div)
        print("data_div", len(data_div))

        # data = soup.find_all("p", class_="text-[13px] font-medium leading-5 text-[#6A6A6A] md:text-sm")
        # for i in data:
        #     print(i.text)

        yield {
            "x": stock_symbol,
            'y': company_sector
        }