import scrapy

class BooksSpider(scrapy.Spider):
    # Unique identifier for this scraper
    name = "books"

    # Where to start crawling
    start_urls = ["https://books.toscrape.com/index.html"]

    # Parse method: called for every downloaded page
    def parse(self, response):
        pass