from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader

def normalize_url(url):
    value = url.replace('\xa0', '.')
    value = value.replace(' ', '.')
    if value[:3] != 'www':
        value = 'https://www.' + value

    return value




class StockInfoTableItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    full_name_in = MapCompose(lambda x: x.strip())
    relative_url_in = MapCompose(lambda x:normalize_url(x))