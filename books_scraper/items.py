import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst

# Define Item
class BookItem(scrapy.Item):
    """
    Represents a scraped book with all required fields
    """
    title = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    product_url = scrapy.Field()
    image_url = scrapy.Field()
    category = scrapy.Field()

# Item Loader
class BookItemLoader(ItemLoader):
    """
    Loader handles extraction only
    All cleaning happens in the pipeline
    """
    # Default output: take the first non-null value
    default_output_processor = TakeFirst()

