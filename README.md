# Enterprise Web Scraping Pipeline - Books Data Engineering System

A production-ready Scrapy application for scraping book data from [Books to Scrape](https://books.toscrape.com), featuring dynamic category discovery, random book selection, multi-format data export, SQLite storage, Docker containerization, and Scrapyd deployment.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation Guide](#installation-guide)
- [Environment Setup](#environment-setup)
- [Running the Spider](#running-the-spider)
- [Docker Setup Guide](#docker-setup-guide)
- [Scrapyd Deployment Guide](#scrapyd-deployment-guide)
- [Output Format Description](#output-format-description)
- [Database Configuration](#database-configuration)
- [Architecture Diagram](#architecture-diagram)
- [Folder Structure](#folder-structure)
- [Design Decisions](#design-decisions)
- [Known Limitations](#known-limitations)

---

## Features

- **Dynamic Category Discovery**: Automatically discovers all book categories from the homepage without hardcoding
- **Random Selection**: Randomly selects 5 categories, then 5 books from each (25 books total)
- **Multi-Format Export**: Exports data to JSON, CSV, and XML simultaneously
- **SQLite Database Storage**: Stores cleaned data via Scrapy Item Pipelines
- **Data Cleaning Pipeline**: Strips whitespace, converts prices to numeric values, normalizes availability to boolean
- **OOP, SOLID & DRY Principles**: Clean, modular, maintainable codebase
- **Comprehensive Logging**: Tracks crawling progress and errors
- **Docker Containerization**: Fully containerized application
- **Scrapyd Deployment**: Deployable via Scrapyd API

---

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Programming language |
| Scrapy | 2.11+ | Web scraping framework |
| SQLite | 3.x | Lightweight database (built into Python) |
| itemloaders | 1.1+ | Structured data extraction |
| Docker | Latest | Containerization |
| Scrapyd | 1.4+ | Spider deployment service |
| scrapyd-client | Latest | Deployment client |

---

## Installation Guide

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone the Project

```bash
git clone https://github.com/mhbhuiyan99/books-scraper_Mojammel.git
cd books-scraper_Mojammel
```

### Step 2: Create Virtual Environment

```bash
python -m venv .venv
```

### Step 3: Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Setup

The project uses the following configuration files:

| File | Purpose |
|------|---------|
| `settings.py` | Scrapy settings, pipelines, feed exports |
| `scrapy.cfg` | Scrapyd deployment configuration |
| `requirements.txt` | Python package dependencies |

No additional environment variables are required.

---

## Running the Spider

### Method 1: Direct Execution

```bash
python -m scrapy crawl books
```

This will:
1. Discover all categories dynamically
2. Randomly select 5 categories
3. Select 5 random books from each category
4. Extract data from each book's detail page
5. Clean data through the pipeline
6. Save to SQLite database
7. Export to `output/books.json`, `output/books.csv`, and `output/books.xml`

### Method 2: Run and Test (Quick Output)

```bash
python -m scrapy crawl books -o test.json
```

### Method 3: With Logging

```bash
python -m scrapy crawl books -L INFO
```

### Verify Output

Check the generated files:

```bash
# View database
python -c "import sqlite3; conn = sqlite3.connect('books.db'); c = conn.cursor(); print(c.execute('SELECT COUNT(*) FROM books').fetchone()[0], 'books stored')"

# List output files
ls output/
```

---

## Docker Setup Guide

### Prerequisites

- Docker installed on your system

### Step 1: Build Docker Image

```bash
docker build -t books-scraper .
```

### Step 2: Run Container

```bash
docker run books-scraper
```

The spider will execute inside the container and output files will be generated within the container's filesystem.

### Docker with Volume Mount (Save Output to Host)

```bash
docker run -v "$(pwd)/output:/app/output" books-scraper
```

This saves the output files to your local `output/` directory.

### Dockerfile Overview

The Dockerfile:
1. Uses `python:3.11-slim` as base image
2. Installs all dependencies from `requirements.txt`
3. Copies the project into `/app`
4. Runs the spider via `CMD`

---

## Scrapyd Deployment Guide

### Step 1: Start Scrapyd Server

Open a **separate terminal** and run:

```bash
scrapyd
```

Server starts at `http://localhost:6800`.

### Step 2: Deploy Project

In your project directory (with venv activated):

```bash
python -m scrapyd-deploy default
```

### Step 3: Verify Deployment

```bash
curl http://localhost:6800/listprojects.json
```

Expected response:
```json
{"status": "ok", "projects": ["books_scraper"]}
```

### Step 4: List Available Spiders

```bash
curl http://localhost:6800/listspiders.json?project=books_scraper
```

### Step 5: Schedule Spider Run

```bash
curl http://localhost:6800/schedule.json -d project=books_scraper -d spider=books
```

Returns a job ID:
```json
{"status": "ok", "jobid": "a1b2c3d4..."}
```

### Step 6: Check Job Status

```bash
curl http://localhost:6800/listjobs.json?project=books_scraper
```

### Cancel a Job

```bash
curl http://localhost:6800/cancel.json -d project=books_scraper -d job=JOB_ID_HERE
```

### Windows PowerShell Alternative

If `curl` is not available, use:

```powershell
Invoke-RestMethod -Uri http://localhost:6800/schedule.json -Method Post -Body @{project="books_scraper"; spider="books"}
```

---

## Output Format Description

### JSON (`output/books.json`)

```json
[
  {
    "title": "It's Only the Himalayas",
    "price": 45.17,
    "availability": true,
    "product_url": "https://books.toscrape.com/catalogue/...",
    "image_url": "https://books.toscrape.com/media/cache/...",
    "category": "Travel"
  }
]
```

- Pretty-printed with 4-space indentation
- Price stored as float (currency symbol removed)
- Availability stored as boolean

### CSV (`output/books.csv`)

```csv
title,price,availability,product_url,image_url,category
It's Only the Himalayas,45.17,True,https://...,https://...,Travel
```

- UTF-8 encoded
- Header row included
- Boolean values as `True`/`False`

### XML (`output/books.xml`)

```xml
<?xml version="1.0" encoding="utf-8"?>
<items>
  <item>
    <title>It's Only the Himalayas</title>
    <price>45.17</price>
    <availability>True</availability>
    <product_url>https://...</product_url>
    <image_url>https://...</image_url>
    <category>Travel</category>
  </item>
</items>
```

---

## Database Configuration

### SQLite Database (`books.db`)

**Table Schema:**

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY AUTOINCREMENT | Unique identifier |
| title | TEXT NOT NULL | Book title |
| price | REAL | Numeric price (GBP) |
| availability | INTEGER | 1 = In stock, 0 = Out of stock |
| product_url | TEXT | Link to product page |
| image_url | TEXT | Link to book cover image |
| category | TEXT | Book category |

### Query Examples

```sql
-- Count total books
SELECT COUNT(*) FROM books;

-- View all books
SELECT * FROM books;

-- Books by category
SELECT category, COUNT(*) FROM books GROUP BY category;

-- Average price
SELECT AVG(price) FROM books;
```

### Python Verification Script

```python
import sqlite3

conn = sqlite3.connect("books.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM books")
print(f"Total books stored: {cursor.fetchone()[0]}")

cursor.execute("SELECT title, price, category FROM books LIMIT 5")
for row in cursor.fetchall():
    print(row)

conn.close()
```

---

## Architecture Diagram

```
+-------------------------------------------------------------+
|                    TARGET WEBSITE                            |
|         https://books.toscrape.com/index.html               |
+-------------------------------------------------------------+
                            |
                            v
+-------------------------------------------------------------+
|  +-------------------+    +-------------------------------+ |
|  |  HOMEPAGE SPIDER  |--->|  1. Discover ALL categories  | |
|  |   (parse method)  |    |  2. Randomly select 5        | |
|  +-------------------+    +-------------------------------+ |
|            |                           |                    |
|            |  Follow 5 category URLs   |                    |
|            v                           v                    |
|  +-------------------+    +-------------------------------+ |
|  |  CATEGORY PARSER  |--->|  1. Collect ALL book links   | |
|  |(parse_category)   |    |  2. Randomly select 5        | |
|  +-------------------+    +-------------------------------+ |
|            |                           |                    |
|            |  Follow 25 book URLs      |                    |
|            v                           v                    |
|  +-------------------+    +-------------------------------+ |
|  |  BOOK DETAIL      |--->|  Extract: title, price,      | |
|  |  (parse_book)     |    |  availability, URLs, category | |
|  +-------------------+    +-------------------------------+ |
|            |                                                |
+------------|------------------------------------------------+
             |
             v
+-------------------------------------------------------------+
|  +-------------------+                                      |
|  | BookItemLoader    |  Extract & structure raw data        |
|  +-------------------+                                      |
|            |                                                |
|            v                                                |
|  +-------------------+    +-------------------------------+ |
|  | Cleaning Pipeline |--->|  Strip whitespace             | |
|  | (Priority: 100)   |    |  Remove currency symbol       | |
|  +-------------------+    |  Convert price to float       | |
|            |              |  Normalize availability       | |
|            |              +-------------------------------+ |
|            v                                                |
|  +-------------------+    +-------------------------------+ |
|  | Database Pipeline |--->|  Insert into SQLite           | |
|  | (Priority: 200)   |    |  books.db                     | |
|  +-------------------+    +-------------------------------+ |
|            |                                                |
|            v                                                |
|  +-----------------------------------------------------+    |
|  |               FEED EXPORTS                           |    |
|  |  output/books.json  output/books.csv  output/books.xml |    |
|  +-----------------------------------------------------+    |
+-------------------------------------------------------------+
                            |
                            v
+-------------------------------------------------------------+
|                    DEPLOYMENT LAYER                          |
|  +-------------------+    +-------------------------------+ |
|  | Docker Container  |    | Scrapyd Server                | |
|  | (Dockerfile)      |    | (scrapyd + API endpoints)     | |
|  +-------------------+    +-------------------------------+ |
+-------------------------------------------------------------+
```

---

## Folder Structure

```
books-scraper_Mojammel/
|
|-- .venv/                          # Virtual environment
|-- output/                         # Exported files (JSON, CSV, XML)
|   |-- books.json
|   |-- books.csv
|   |-- books.xml
|
|-- books_scraper/                  # Main project package
|   |-- __init__.py                 # Package marker
|   |-- items.py                    # BookItem & BookItemLoader
|   |-- middlewares.py              # Scrapy middleware (auto-generated)
|   |-- pipelines.py                # BookCleaningPipeline & DatabasePipeline
|   |-- settings.py                 # Scrapy configuration & feed exports
|   |-- spiders/
|       |-- __init__.py             # Package marker
|       |-- books_spider.py         # Main spider
|
|-- scrapy.cfg                      # Scrapyd deployment configuration
|-- requirements.txt                # Python dependencies
|-- Dockerfile                      # Docker container recipe
|-- .dockerignore                   # Docker ignore rules
|-- books.db                        # SQLite database (auto-generated)
|-- README.md                       # This file
```

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| **SQLite over MongoDB** | SQLite requires no separate server, is built into Python, and is sufficient for this dataset size |
| **Pipeline-based cleaning** | Centralizes all data transformation in one place (DRY principle) rather than duplicating in loaders |
| **ItemLoader for extraction** | Provides clean, structured data extraction with built-in output processing |
| **Random category then book selection** | Instructor clarification: 5 random categories selected first, then 5 random books per category |
| `min(5, len(links))` | Prevents `ValueError` when a category has fewer than 5 books |
| **Docker + Scrapyd** | Meets assignment deployment requirements; Scrapyd provides API-based spider scheduling |
| **No hardcoded URLs** | All category URLs and names are discovered dynamically from the homepage |
| **Return `None` instead of `DropItem`** | Avoids import issues across different Scrapy versions while achieving the same effect |

---

## Known Limitations

| Limitation | Description | Workaround |
|------------|-------------|------------|
| **Website availability** | Target site may be down or changed | Assignment uses a stable demo site; no mitigation needed |
| **No retry logic** | Network failures cause spider to skip items | Scrapy has built-in retry middleware (enabled by default) |
| **Single-threaded per domain** | Scrapy respects `DOWNLOAD_DELAY` | Default concurrent requests are limited by `CONCURRENT_REQUESTS_PER_DOMAIN` |
| **Docker output persistence** | Output files exist only inside container unless volume is mounted | Use `docker run -v` flag to mount host directory |
| **Scrapyd runs locally** | Default Scrapyd deployment is local only | For production, deploy Scrapyd to a remote server |
| **No authentication** | Target site requires no login | Not applicable for this assignment |
| **Static website only** | JavaScript-rendered sites are not supported | This target site is static HTML; no JS execution needed |



