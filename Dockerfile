
# Use official Python image as base
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project into the container
COPY . .

# Set the working directory to where scrapy.cfg lives
WORKDIR /app

# Default command: run the spider
CMD ["python", "-m", "scrapy", "crawl", "books"]