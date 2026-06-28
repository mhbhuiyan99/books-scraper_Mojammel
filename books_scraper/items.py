import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join

# Input Processors
def strip_whitespace(value):
    """Remove leading/trailing whitespace"""
    return value.strip() if value else value

def remove_currency(value):
    """Remove £ symbol from price"""
    return value.replace("£","") if value else value

def normalize_availability(value):
    """Convert availability text to boolean"""
    if value and "in stock" in value.lower():
        return True
    return False

# Define Item
class BookItem(scrapy.Item):
    """
    Represents a scraped book with all required field
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
    Custom loader for BookItem with automatic data cleaning
    """
    # Default output: take the first non-null value
    default_output_processor = TakeFirst()

    # Field-spacific input processors
    title_in = MapCompose(strip_whitespace)
    price_in = MapCompose(strip_whitespace, remove_currency)
    availability_in = MapCompose(strip_whitespace, normalize_availability)
    category_in = MapCompose(strip_whitespace)

