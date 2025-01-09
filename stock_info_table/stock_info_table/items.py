# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StockInfoTableItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    relative_url = scrapy.Field()
    full_name = scrapy.Field()
    