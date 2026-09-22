import time
import requests
from urllib.parse import urlparse, urljoin, urlsplit
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
import asyncio
import aiohttp
from types import TracebackType

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


def normalize_url(url: str) -> str:
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    path = parsed_url.path.rstrip("/")
    return f"{netloc}{path}"
        

def get_heading_from_html(html: str) -> str:
    """
    Extract h1 heading from html, it will turn the text of the h1 heading
    if h1 tag is not present, it will return text of h2 heading
    if h1 and h2 tags are not present, it will return empty string
    if multiple h1 tags are present, it will return the text of the first h1 tag
    if multiple h2 tags are present, it will return the text of the first h2 tag
    """
    soup = BeautifulSoup(html, "html.parser")

    h1 = soup.find("h1")
    if h1:
        return h1.get_text()
    h2 = soup.find("h2")
    if h2:
        return h2.get_text()
    return ""

    
def get_first_paragraph_from_html(html: str) -> str:
    """
    Returns the text of the first <p> tag found in the html within the <main> tag.
    If no <main> tag is found or no <p> is found within main, it will search the whold document for <p>.
    If no <p> tag is found, it returns an empty string.
    If multiple <p> tags are found, it returns the text of the first <p> tag.
    """
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")
    if main:
        p = main.find("p")
        if p:
            return p.get_text()
    p = soup.find("p")
    if p:
        return p.get_text()
    return ""


def get_urls_from_html(html: str, base_url: str) -> list[str]:
    """
    Takes the html from a page as a string and the base_url for relative links.
    Returns an un-normalized list of all the URLs found within the HTML.
    It must make sure that relative paths are converted to absolute paths.
    """
    soup = BeautifulSoup(html, "html.parser")
    a_tags = soup.find_all("a")
    urls = []
    for a in a_tags:
        if not isinstance(a, Tag):
            continue
        href = a.get("href")
        if href and isinstance(href, str):
            try:
                absolute_url = urljoin(base_url, href)
                urls.append(absolute_url)
            except Exception as e:
                print(f"{str(e)}: {href}")
    return urls


def get_images_from_html(html: str, base_url: str) -> list[str]:
    """
    Takes the html from a page as a string and the base_url for relative links.
    Returns an un-normalized list of all the image URLs found within the HTML and an error if one occors.
    It must make sure that relative paths are converted to absolute paths.
    """
    soup = BeautifulSoup(html, "html.parser")
    image_urls = []
    images = soup.find_all("img")

    for img in images:
        if not isinstance(img, Tag):
            continue
        src = img.get("src")
        if isinstance(src, str) and src:
            try:
                absolute_url = urljoin(base_url, src)
                image_urls.append(absolute_url)
            except Exception as e:
                print(f"{str(e)}: {src}")

    return image_urls
    

def extract_page_data(html: str, page_url: str) -> PageData:
    """Extract key elements and absolute URLs from an HTML document.

    Args:
        html: Raw HTML string of the webpage.
        page_url: Absolute URL of the page, used to resolve relative links.

    Returns:
        A dictionary containing:
            - 'url' (str): The provided base page URL.
            - 'heading' (str): Primary page heading (e.g., h1 content).
            - 'first_paragraph' (str): Text of the initial body paragraph.
            - 'outgoing_links' (list[str]): Fully resolved outbound hyperlinks.
            - 'image_urls' (list[str]): Fully resolved image source URLs.
    """
    heading = get_heading_from_html(html)
    first_paragraph = get_first_paragraph_from_html(html)
    outgoing_links = get_urls_from_html(html, page_url)
    image_urls = get_images_from_html(html, page_url)

    return PageData(
        url=page_url,
        heading=heading,
        first_paragraph=first_paragraph,
        outgoing_links=outgoing_links,
        image_urls=image_urls,
    )


def get_html(url: str) -> str:
    try:
        agent = "BootCrawler/1.0"
        headers = {"User-Agent": agent}
        res = requests.get(url, headers=headers)
    except Exception as e:
        raise Exception(f"network error while fetching {url}: {e}")

    if res.status_code >= 400:
        raise Exception(f"Error: {res.status_code} {res.reason}")
    
    content_type = res.headers.get("Content-Type", "")
    if "text/html" not in content_type:
        raise Exception(f"Error: Invalid content type: {content_type}")

    return res.text


# def crawl_page(
#     base_url: str,
#     current_url: str | None = None,
#     page_data: dict[str, PageData] | None = None
# ) -> dict[str, PageData]:
#     """ Crawl the page at current_url, updating the page_data accumulator as it goes.

#     Args:
#         base_url (str): The base URL of the domain to crawl.
#         current_url (str, optional): The current URL to crawl. Defaults to None.
#         page_data (dict, optional): The accumulator for storing page data. Defaults to None.

#     Returns:
#         None

#     Pseudocode:
#     X. Make sure the current_url is on the same domain as the base_url. If it's not, just return. We don't want to crawl the entire internet, just the domain in question.
#     X. Get a normalized version of the current_url.
#     X. Check if we've already crawled this page by checking if the normalized URL is already a key in the page_data dictionary. If we have, just return - we don't want to crawl the same page twice.
#     X. Get the HTML from the current URL, and add a print statement so you can watch your crawler in real-time.
#     5. Assuming all went well with the request, pass the HTML and current_url to extract_page_data() and add the result to the page_data dictionary using the normalized URL as the key.
#     6. Use the extracted page data's outgoing_links as the URLs to crawl next
#     7. Recursively crawl each URL on the page
#     """
#     if current_url is None:
#         current_url = base_url
#     if page_data is None:
#         page_data: dict[str, PageData] = {}

#     if not does_start_with_base(base_url, current_url):
#         return page_data

#     normalized_url = normalize_url(current_url)

#     if normalized_url in page_data:
#         return page_data
    
#     html = get_html(current_url)
#     if html is None:
#         return page_data
    
#     print(f"crawling: {normalized_url}:")
#     current_page_data = extract_page_data(html, current_url)
#     page_data[normalized_url] = current_page_data
#     for url in current_page_data['outgoing_links']:
#         time.sleep(0.10)
#         crawl_page(base_url, url, page_data)  
#     return page_data  

def does_start_with_base(base_url: str, current_url: str) -> bool:
    base_url_obj = urlsplit(base_url)
    current_url_obj = urlsplit(current_url)
    if current_url_obj.netloc != base_url_obj.netloc:
        return False
    return True

# async def crawl_site_async(base_url: str):
#     crawler = AsyncWebCrawler(
#         base_url=base_url,
#         base_domain=urlsplit(base_url).netloc,
#         page_data=dict[str, PageData],
#         visited=set[str],
#         lock=asyncio.Lock(),
#         max_concurrency=10,
#         semaphore=asyncio.Semaphore(1),
#         session=aiohttp.ClientSession()
#     )
#     async with crawler as crawler:
#         page_data = await crawler.crawl(base_url)
    
#     return page_data


class AsyncWebCrawler:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.base_domain = urlsplit(base_url).netloc
        self.page_data: dict[str, PageData] = {}
        self.visited: set[str] = set()
        self.lock = asyncio.Lock()
        self.max_concurrency = 3
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session: aiohttp.ClientSession | None = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.session.close()

    async def add_page_visit(self, normalized_url: str) -> bool:
        async with self.lock:
            if normalized_url in self.visited:
                return False
            self.visited.add(normalized_url)
            return True

    async def get_html(self, url: str) -> str | None:
        if self.session is None:
            return None

        try:
            agent = "BootCrawler/1.0"
            headers = {"User-Agent": agent}
            async with self.session.get(url, headers=headers) as res:
                if res.status >= 400:
                    print(f"Error: HTTP {res.status} for {url}")
                    return None
                content_type = res.headers.get("content-type", "")
                if "text/html" not in content_type:
                    print(f"Error: Invalid content type: {content_type}")
                    return None

                return await res.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None


    async def crawl_page(
        self,
        current_url: str | None = None,
    ) -> None:
        if not does_start_with_base(self.base_url, current_url):
            return
        
        normalized_url = normalize_url(current_url)
        
        is_new = await self.add_page_visit(normalized_url)
        if not is_new:
            return

        async with self.semaphore:
            print(
                f"Crawling {current_url} (Active: {self.max_concurrency - self.semaphore._value})"
            )
            html = await self.get_html(current_url)
            
            if html is None:
                return
        
            current_page_data = extract_page_data(html, current_url)

            async with self.lock:
                self.page_data[normalized_url] = current_page_data

            next_urls = current_page_data["outgoing_links"]

        tasks: list[asyncio.Task[None]] = []
        for next_url in next_urls:
            task = asyncio.create_task(self.crawl_page(next_url))
            tasks.append(task)

        if tasks:
            await asyncio.gather(*tasks)

    async def crawl(self) -> dict[str, PageData]:
        await self.crawl_page(self.base_url)
        return self.page_data


async def crawl_site_async(base_url: str) -> dict[str, PageData]:
    async with AsyncWebCrawler(base_url) as crawler:
        return await crawler.crawl()