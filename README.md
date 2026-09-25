# Async Web Crawler

A high-performance, asynchronous Python web crawler built with `asyncio` and `aiohttp` to traverse websites within a single domain, extract key page metadata and media, and generate structured JSON reports.

---

## Features

- ⚡ **Asynchronous & Concurrent**: Uses `asyncio` and `aiohttp` for non-blocking HTTP requests and high-speed crawling.
- 🚦 **Concurrency & Page Limits**: Configurable worker concurrency using `asyncio.Semaphore` and configurable crawl depth/page limits.
- 🌐 **Domain-Scoped Traversal**: Discovers and crawls internal pages starting from a base URL while strictly restricting traversal within the target domain.
- 🔗 **URL Normalization & Deduplication**: Normalizes URLs by stripping protocol schemes (`http://`, `https://`) and trailing slashes to prevent redundant page visits.
- 📄 **Structured Content Extraction**:
  - **Headings**: Extracts primary `<h1>` heading text, falling back to `<h2>` if `<h1>` is absent.
  - **First Paragraph**: Locates body text, prioritizing `<main><p>` over generic document `<p>`.
  - **Hyperlinks**: Extracts and resolves relative and absolute outbound links using `urljoin`.
  - **Image URLs**: Finds and resolves all `<img>` source URLs to absolute links.
- 📊 **JSON Reporting**: Automatically exports structured page data records into `report.json` sorted alphabetically by URL.
- 🛡️ **Polite Crawling & Validation**:
  - Sets a custom `User-Agent: BootCrawler/1.0`.
  - Validates HTTP response status codes and `text/html` content types.
- 🧪 **Comprehensive Unit Test Suite**: 30 automated test cases covering normalization, HTML parsing, element prioritization, and edge cases.

---

## Project Structure

```text
webcrawler/
├── crawl.py          # Async crawler engine, HTML parsers, URL utilities, and report generator
├── main.py           # CLI entry point and orchestration
├── test_crawl.py     # Unit test suite (unittest)
├── report.json       # Generated output report from crawl runs
├── pyproject.toml    # Project metadata and dependencies
├── uv.lock           # Dependency lockfile
└── README.md         # Project documentation
```

---

## Requirements

- **Python**: `>= 3.12`
- **Dependencies**:
  - `aiohttp` (Asynchronous HTTP client)
  - `beautifulsoup4` (HTML parsing)
  - `requests` (Synchronous HTTP requests)

---

## Installation & Setup

You can set up the environment using `uv` (recommended) or standard Python `venv`/`pip`:

### Using `uv`

```bash
# Clone the repository and navigate into the project directory
cd webcrawler

# Install dependencies into virtual environment
uv sync
```

### Using standard `venv` and `pip`

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install aiohttp beautifulsoup4 requests
```

---

## Usage

Run the crawler CLI by passing the target **base URL**, **max concurrency**, and **max pages**:

```bash
# General syntax
python main.py <base_url> <max_concurrency> <max_pages>

# Or with uv
uv run python main.py <base_url> <max_concurrency> <max_pages>
```

### CLI Arguments

| Argument | Type | Description |
| :--- | :--- | :--- |
| `base_url` | `str` | The starting URL and domain scope for the crawl (e.g., `https://crawler-test.com`) |
| `max_concurrency` | `int` | Maximum number of concurrent async requests (semaphore limit) |
| `max_pages` | `int` | Maximum number of unique pages to crawl before stopping |

### Example

```bash
uv run python main.py https://crawler-test.com 3 10
```

**Console Output:**

```text
starting crawl of: https://crawler-test.com...
Crawling https://crawler-test.com (Active: 1)
Crawling https://crawler-test.com/about (Active: 2)
Crawling https://crawler-test.com/contact (Active: 3)
Reached maximum number of pages to crawl.
```

---

## Output Data Structure

The crawl results are saved to `report.json` as a list of `PageData` objects sorted by URL:

```python
class PageData(TypedDict):
    url: str                   # The original page URL
    heading: str               # The primary h1/h2 text
    first_paragraph: str       # First paragraph text (<main><p> prioritized)
    outgoing_links: list[str]  # Absolute URLs of outbound links
    image_urls: list[str]      # Absolute URLs of images found
```

### Sample `report.json`

```json
[
  {
    "url": "https://crawler-test.com",
    "heading": "Example Domain",
    "first_paragraph": "This domain is established to be used for illustrative examples in documents.",
    "outgoing_links": [
      "https://crawler-test.com/about",
      "https://crawler-test.com/contact"
    ],
    "image_urls": [
      "https://crawler-test.com/images/logo.png"
    ]
  }
]
```

---

## Running Tests

Execute the unit test suite using Python's built-in `unittest` module:

```bash
# Run unit tests
python3 -m unittest test_crawl.py

# Or with uv
uv run python -m unittest test_crawl.py
```

Or run all tests with discovery:

```bash
python3 -m unittest discover
```
