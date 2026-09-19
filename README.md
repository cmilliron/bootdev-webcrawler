# Web Crawler

A fast, recursive Python web crawler built to traverse websites within a single domain, extract key page metadata and media, and report crawl results.

## Features

- **Recursive Domain-Scoped Crawling**: Recursively discovers and crawls internal pages starting from a base URL while strictly restricting traversal within the target domain.
- **URL Normalization**: Normalizes URLs by removing protocol schemes (`http://`, `https://`) and stripping trailing slashes to prevent duplicate page visits.
- **Structured Data Extraction**:
  - **Headings**: Extracts primary `<h1>` text, with fallback to `<h2>`.
  - **First Paragraph**: Locates body text prioritizing `<main><p>` over generic document `<p>`.
  - **Hyperlinks**: Extracts and resolves relative and absolute outbound links using `urljoin`.
  - **Image URLs**: Finds and resolves all `<img>` source URLs.
- **Polite Crawling & Network Resilience**:
  - Sets a custom `User-Agent: BootCrawler/1.0`.
  - Validates HTTP response status codes and `text/html` content types.
  - Implements polite request throttling with customizable sleep intervals.
- **Comprehensive Unit Test Suite**: 30 automated test cases covering normalization, HTML parsing, element prioritization, and edge cases.

---

## Project Structure

```text
webcrawler/
├── crawl.py          # Core crawler logic, extraction functions, and URL utilities
├── main.py           # CLI entry point and crawl orchestration
├── test_crawl.py     # Unit test suite (unittest)
├── pyproject.toml    # Project configuration and dependencies
├── uv.lock           # Dependency lockfile
└── README.md         # Project documentation
```

---

## Requirements

- **Python**: `>= 3.12`
- **Dependencies**:
  - `requests` (HTTP requests)
  - `beautifulsoup4` (HTML parsing)
  - `aiohttp`

---

## Installation & Setup

You can set up the environment using `uv` (recommended) or standard `venv`/`pip`:

### Using `uv`

```bash
# Clone the repository and navigate into the directory
cd webcrawler

# Install dependencies into virtual environment
uv sync
```

### Using standard `venv` and `pip`

```bash
# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install requests beautifulsoup4 aiohttp
```

---

## Usage

Run the crawler CLI by passing a target base URL:

```bash
# Using python
python main.py <url>

# Or with uv
uv run python main.py <url>
```

### Example

```bash
python main.py https://crawler-test.com
```

**Example Output:**

```text
starting crawl of: https://crawler-test.com...
crawling: crawler-test.com:
crawling: crawler-test.com/about:
crawling: crawler-test.com/contact:
Found 3 pages:
1. https://crawler-test.com: 14 outgoing links
2. https://crawler-test.com/about: 5 outgoing links
3. https://crawler-test.com/contact: 3 outgoing links
```

---

## Data Structure

Each crawled page produces a `PageData` record:

```python
class PageData(TypedDict):
    url: str               # The original page URL
    heading: str           # The primary h1/h2 text
    first_paragraph: str   # First paragraph text (main preferred)
    outgoing_links: list[str]  # Absolute URLs of outbound links
    image_urls: list[str]      # Absolute URLs of images found
```

---

## Running Tests

Execute the unit test suite using Python's built-in `unittest` module:

```bash
python3 -m unittest test_crawl.py
```

Or run all tests with discovery:

```bash
python3 -m unittest discover
```
