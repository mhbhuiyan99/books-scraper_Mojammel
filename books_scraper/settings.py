
BOT_NAME = "books_scraper"

SPIDER_MODULES = ["books_scraper.spiders"]
NEWSPIDER_MODULE = "books_scraper.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure pipelines
ITEM_PIPELINES = {
    "books_scraper.pipelines.BookCleaningPipeline": 100,   # Clean first
    "books_scraper.pipelines.DatabasePipeline": 200,        # Then store
}

# --- FEED EXPORTS ---
# This single dict tells Scrapy to output ALL formats automatically!

FEEDS = {
    # JSON format
    "output/books.json": {
        "format": "json",
        "encoding": "utf8",
        "indent": 4,          
        "overwrite": True,      # Replace existing file
    },
    
    # CSV format
    "output/books.csv": {
        "format": "csv",
        "encoding": "utf8",
        "overwrite": True,
    },
    
    # XML format
    "output/books.xml": {
        "format": "xml",
        "encoding": "utf8",
        "overwrite": True,
    },
}
