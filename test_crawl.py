import unittest
from crawl import (
    normalize_url,
    get_heading_from_html,
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
    extract_page_data
)


class TestCrawl(unittest.TestCase):
    def test_normalize_url_1(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_2(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_3(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_4(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)
    
    def test_get_heading_from_html_1(self):
        input_html = "<h1>Hello World</h1>"
        actual = get_heading_from_html(input_html)
        expected = "Hello World"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_2(self):
        input_html = "<body><h1>Hello World</h1></body>"
        actual = get_heading_from_html(input_html)
        expected = "Hello World"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_3(self):
        input_html = "<main><h2>Hello World</h2></main>"
        actual = get_heading_from_html(input_html)
        expected = "Hello World"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_4(self):
        input_html = "<main><h3>Hello World</h3></main>"
        actual = get_heading_from_html(input_html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority_no_p_tag(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <div>Not a paragraph.</div>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Outside paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_paragraph(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    # Test get_urls_from_html
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/about"><span>About</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/about"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple_urls(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a><a href="/about"><span>About</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com", "https://crawler-test.com/about"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple_urls_not_in_base_domain(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a><a href="/about"><span>About</span></a><a href="https://google.com"><span>Google</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com", "https://crawler-test.com/about", "https://google.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_no_urls(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_no_a_tags(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><h1>Test Title</h1><p>Test Paragraph</p></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    # Test get_images_from_html 
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected) 

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://crawler-test.com/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected) 

    def test_get_images_from_html_multiple_images(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"><img src="https://crawler-test.com/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png", "https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected) 

    def test_get_images_from_html_multiple_images_not_in_base_domain(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"><img src="https://crawler-test.com/logo.png" alt="Logo"><img src="https://google.com/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png", "https://crawler-test.com/logo.png", "https://google.com/logo.png"]
        self.assertEqual(actual, expected) 

    def test_get_images_from_html_no_images(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><h1>Test Title</h1><p>Test Paragraph</p></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    # Test extract_page_data
    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_empty_html(self):
        input_url = "https://crawler-test.com"
        input_body = ""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_h2_fallback_and_main_paragraph_priority(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h2>Fallback Heading</h2>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph content.</p>
            </main>
            <a href="/docs">Docs</a>
            <img src="/images/hero.png" alt="Hero">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Fallback Heading",
            "first_paragraph": "Main paragraph content.",
            "outgoing_links": ["https://crawler-test.com/docs"],
            "image_urls": ["https://crawler-test.com/images/hero.png"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_multiple_elements_selection(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Primary Heading</h1>
            <h1>Secondary Heading</h1>
            <h2>Sub Heading</h2>
            <p>First paragraph.</p>
            <p>Second paragraph.</p>
            <div>
                <a href="/link1">Link 1</a>
                <a href="https://external.com/link2">Link 2</a>
            </div>
            <img src="/img1.png" alt="Img 1">
            <img src="https://cdn.example.com/img2.jpg" alt="Img 2">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Primary Heading",
            "first_paragraph": "First paragraph.",
            "outgoing_links": [
                "https://crawler-test.com/link1",
                "https://external.com/link2",
            ],
            "image_urls": [
                "https://crawler-test.com/img1.png",
                "https://cdn.example.com/img2.jpg",
            ],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_missing_and_empty_attributes(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h3>Not H1 or H2</h3>
            <a>Link without href</a>
            <a href="">Empty href</a>
            <img alt="Image without src">
            <img src="">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_nested_formatting_tags(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Heading with <em>emphasis</em> and <span>styling</span></h1>
            <main>
                <p>Paragraph with <strong>bold</strong> text and a <a href="/inner">link</a>.</p>
            </main>
            <a href="/outer">Outer Link</a>
            <img src="/photo.jpg" alt="Photo">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Heading with emphasis and styling",
            "first_paragraph": "Paragraph with bold text and a link.",
            "outgoing_links": [
                "https://crawler-test.com/inner",
                "https://crawler-test.com/outer",
            ],
            "image_urls": ["https://crawler-test.com/photo.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_relative_url_resolution(self):
        input_url = "https://crawler-test.com/blog/posts/test-post"
        input_body = """<html><body>
            <h1>Blog Post</h1>
            <p>Blog post content.</p>
            <a href="../page">Previous page</a>
            <a href="./author">Author</a>
            <a href="/home">Home</a>
            <img src="../images/pic.png" alt="Pic">
            <img src="./thumb.jpg" alt="Thumb">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com/blog/posts/test-post",
            "heading": "Blog Post",
            "first_paragraph": "Blog post content.",
            "outgoing_links": [
                "https://crawler-test.com/blog/page",
                "https://crawler-test.com/blog/posts/author",
                "https://crawler-test.com/home",
            ],
            "image_urls": [
                "https://crawler-test.com/blog/images/pic.png",
                "https://crawler-test.com/blog/posts/thumb.jpg",
            ],
        }
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()