import scrapy

class BooksSpider(scrapy.Spider):
    # Unique identifier for this scraper
    name = "books"

    # Where to start crawling
    start_urls = ["https://books.toscrape.com/index.html"]

    # Parse method: called for every downloaded page
    # Website returns HTML, response contains the page
    def parse(self, response):
        # --- CATEGORY EXTRACTION (Homepage) ---

        # Get all category links from sidebar
        category_links = response.css("div.side_categories ul.nav-list li a::attr(href)").getall()
        
        # Get category names
        category_names = response.css("div.side_categories ul.nav-list a::text").getall()


        # --- BOOK EXTRACTION (Category page) ---

        # Get all book containers
        books = response.css("article.product_pod")

        for book in books:
            # Extract title from <a>
            title = book.css("h3 a::attr(title)").get()

            # Extract price
            price = book.css("p.price_color::text").get()

            # Extract availability
            avilabilty = book.css("p.availability::text").get()

            yield {
                "title": title,
                "price": price,
                "availability": availability,
            }