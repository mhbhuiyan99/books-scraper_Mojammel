import scrapy

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

