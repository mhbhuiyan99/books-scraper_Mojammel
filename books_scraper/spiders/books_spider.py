import scrapy
import random
from books_scraper.items import BookItem, BookItemLoader

class BooksSpider(scrapy.Spider):
    """
    Enterprise spider that:
        1. Discovering all categories dynamically from homepage
        2. Randomly selected 5 categories
        3. From each, randomly selects 5 books
        4. Extracts all required fields from each book's detail page
    """

    # Unique identifier for this scraper
    name = "books"

    # Where to start crawling
    start_urls = ["https://books.toscrape.com/index.html"]


    def parse(self, response):
        """
        Parse the homepage - discover all categories, then randomly select 5

        This method runs only once - for the start_url (homepage)
        """

        # Extract all category links from the sidebar
        category_elements = response.css("div.side_categories ul.nav-list li ul li a")

        # Build a list of (name, url) tuples for all categories
        all_categories = []
        for cat in category_elements:
            name = cat.css("::text").get().strip()
            url = cat.css("::attr(href)").get()
            
            all_categories.append({
                "name": name,
                "url": url,
            })

        # Randomly select Exactly 5 categories from all
        selected_categories = random.sample(all_categories, 5)

        self.logger.info(f"Discovered {len(all_categories)} total categories")
        self.logger.info(f"Randomly selected: {[c['name'] for c in selected_categories]}")

        # Follow only the 5 selected categories
        for category in selected_categories:
            yield response.follow(
                category["url"],
                callback=self.parse_category,
                meta={  # data pass to next method
                    "category_name": category["name"],
                }
            )

    def parse_category(self, response):
        """Parse a category page - collect all books, pick 5 random"""

        category_name = response.meta["category_name"] #  Data passed from previous method

        # Get all books links on this category page
        book_links = response.css("article.product_pod h3 a::attr(href)").getall()

        self.logger.info(
            f"Category '{category_name}': {len(book_links)} books found, " f"selecting 5"
        )

        # Random select exactly 5 books
        selected_books = random.sample(book_links, min(5, len(book_links)))

        for book_url in selected_books:
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

        category_name = response.meta["category"]
        
        # Use ItemLoader for clean data extraction
        loader = BookItemLoader(item=BookItem(), response=response)

        # Add data using CSS selectors - cleaning happens automatically
        loader.add_css("title", "div.product_main h1::text")
        loader.add_css("price", "p.price_color::text")
        loader.add_css("availability","p.instock.availability::text")
        loader.add_value("product_url", response.url)
        
        # Image URL needs the base URL prepended
        image_src = response.css("div.item.active img::attr(src)").get() #  return[example]: ../../../its-only-the-himalayas_981/img.jpg
        if image_src:
            # Convert relative URL to absolute
            image_url = response.urljoin(image_src) #  [example] https://books.toscrape.com/catalogue/its-only-the-himalayas_981/img.jpg
            loader.add_value("image_url", image_url)

        loader.add_value("category", category_name)

        # Load the item - all processors are applied
        yield loader.load_item()


