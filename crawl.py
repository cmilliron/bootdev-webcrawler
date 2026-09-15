from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup, Tag

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
    