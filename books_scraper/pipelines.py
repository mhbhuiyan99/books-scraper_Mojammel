import logging
import sqlite3
from books_scraper.items import BookItem

logger = logging.getLogger(__name__)

class BookCleaningPipeline:
    """
    Pipeline for cleaning and normalizing scraped book data
    Processing steps:
        1. Strip whitespace from all text fields
        2. Remove currency symbol from price and convert to float
        3. Normalize availability to boolean
    """

    def process_item(self, item, spider):
        """Clean and normalize a BookItem before storage/export"""

        spider.logger.info(f"Processing item: {item.get('title', 'Unknown')}")

        # Strip whitespace
        item["title"] = self._strip_field(item.get("title"))
        item["category"] = self._strip_field(item.get("category"))
        item["product_url"] = self._strip_field(item.get("product_url"))
        item["image_url"] = self._strip_field(item.get("image_url"))

        # Clean price (remove £, convert to float)
        item["price"] = self._clean_price(item.get("price"))

        # Normalize availability to boolean
        item["availability"] = self._normalize_availability(item.get("availability"))

        return item


    def _strip_field(self, value):
        """Remove leading/trailing whitespace"""
        
        if value is None:
            return ""
        return str(value).strip()
    
    def _clean_price(self, price_str):
        """Remove currency symbol and convert to float"""

        if not price_str:
            return 0.0
        
        # Remove the £ symbol and any whitespace
        cleaned = price_str.replace("£", "").strip()
        
        try:
            return float(cleaned)
        except ValueError:
            logger.warning(f"Could not convert price: {price_str}")
            return 0.0

    def _normalize_availability(self, availability_str):
        """Convert availability text to boolean"""

        if not availability_str:
            return False
        
        # Check if "in stock" appears anywhere in the text
        return "in stock" in availability_str.lower()


class DatabasePipeline:
    """
    Pipeline for storing cleaned items in SQLite database.
    Runs after the cleaning pipeline
    """

    def __init__(self, db_path="books.db"):
        """
        Initialize the pipeline.
        This is called when the spider starts.
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def open_spider(self, spider):
        """
        Called when the spider opens.
        Create the database connection and table.
        """

        spider.logger.info("Opening database connection...")

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        self._create_table()

        spider.logger.info(f"Database '{self.db_path}' ready.")

    def _create_table(self):
        """
        Create the books table if it doesn't exist.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price REAL,
                availability INTEGER,
                product_url TEXT,
                image_url TEXT,
                category TEXT
            )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        """
        Insert a book into the database.
        Called for EVERY item that passes through the pipeline.
        """
        try:
            self.cursor.execute("""
                INSERT INTO books (title, price, availability, product_url, image_url, category)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                item.get("title", ""),
                item.get("price", 0.0),
                1 if item.get("availability") else 0,  # Boolean → Integer
                item.get("product_url", ""),
                item.get("image_url", ""),
                item.get("category", ""),
            ))
            self.conn.commit()
            
            spider.logger.info(f"Stored in DB: {item.get('title')}")
            
        except sqlite3.Error as e:
            spider.logger.error(f"Database error: {e}")
        
        return item 
    
    def close_spider(self, spider):
        """
        Called when the spider closes.
        Close the database connection.
        """
        spider.logger.info("Closing database connection...")
        
        if self.conn:
            self.conn.close()
