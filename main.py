import sys
import asyncio
from crawl import (
    crawl_site_async
)


async def main():
    if len(sys.argv) < 2:
        print("no website provided\n\nUsage: python main.py <url>")
        sys.exit(1)
    if len(sys.argv) > 2:
        print("too many arguments provided\n\nUsage: python main.py <url>")
        sys.exit(1)
    base_url = sys.argv[1]

    print(f"starting crawl of: {base_url}...")
    
    page_data = await crawl_site_async(base_url)

    print(f"Found {len(page_data)} pages:")
    for i, page in enumerate(page_data.values(), 1):
        print(f"{i}. {page['url']}: {len(page['outgoing_links'])} outgoing links")

    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
