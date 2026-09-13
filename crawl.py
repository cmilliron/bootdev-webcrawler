from urllib.parse import urlparse

def normalize_url(url: str) -> str:
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    path = parsed_url.path.rstrip("/")

    return f"{netloc}{path}"
        