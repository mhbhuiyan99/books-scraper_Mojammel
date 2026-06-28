import logging

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
