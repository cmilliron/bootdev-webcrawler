import sys
from crawl import (
    normalize_url,
    get_heading_from_html,
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
    extract_page_data
)


def main():
    if len(sys.argv) < 2:
        print("no website provided\n\nUsage: python main.py <url>")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided\n\nUsage: python main.py <url>")
        sys.exit(1)
    base_url = sys.argv[1]
    print(f"starting crawl of: {base_url}")
    sys.exit(0)


if __name__ == "__main__":
    main()
