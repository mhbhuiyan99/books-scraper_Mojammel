import scrapy
import random
from books_scraper.items import BookItem, BookItemLoader

class BooksSpider(scrapy.Spider):
    # Unique identifier for this scraper
    name = "books"

    # Where to start crawling
    start_urls = ["https://books.toscrape.com/index.html"]


    def parse(self, response):
        """Parse the homepage - discover all categories"""

        # Get category links
        categories = response.css("div.side_categories ul.nav-list li ul li a")

        for category in categories:
            category_name = category.css("::text").get().strip()
            category_url = category.css("::attr(href)").get()

            # Follow the category link
            yield response.follow(
                category_url,
                callback=self.parse_category,
                meta={  # data pass to next method
                    "category": category_name,
                }
            )

    def parse_category(self, response):
        """Parse a category page - collect all books, pick 5 random"""

        category_name = response.meta["category"] #  Data passed from previous method

        # Get all books links on this category page
        book_links = response.css("article.product_pod h3 a::attr(href)").getall()

        # Random select exactly 5 books
        selected = random.sample(book_links, min(5, len(book_links)))

        for book_url in selected:
            # Follow each selected book's link
            yield response.follow(
                book_url,
                callback=self.parse_book,
                meta={
                    "category": category_name
                }
            )

    def parse_book(self, response):
        """Parse a single book's detail page"""
        
        # Use ItemLoader for clean data extraction
        loader = BookItemLoader(item=BookItem(), response=response)

        # Add data using CSS selectors - cleaning happens automatically
        loader.add.css("title", "div.product_main h1::text")
        loader.add.css("price", "p.price_color::text")
        loader.add.css("availability","p.availability::text")
        loader.add_value("product_url", response.url)
        loader.add.css("image_url","div.item.active img::attr(src)")
        loader.add_value("category", response.meta["category"])

        # Load the item - all processors are applied
        yield loader.load_item()
