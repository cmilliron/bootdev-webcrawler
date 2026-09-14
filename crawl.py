from urllib.parse import urlparse
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


def get_urls_from_html(html, base_url):
    pass


def get_images_from_html(html, base_url):
    pass