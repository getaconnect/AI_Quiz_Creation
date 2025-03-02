import unittest
import asyncio
from crawler.crawler import crawl_website

class TestCrawler(unittest.TestCase):
    def test_invalid_url(self):
        # The crawler should raise a ValueError for an invalid URL.
        with self.assertRaises(ValueError):
            asyncio.run(crawl_website("not_a_valid_url"))

    def test_crawl_returns_content(self):
        # This test assumes you have an accessible URL that returns some content.
        # Replace the URL with one that is reliably available in your test environment.
        test_url = "https://www.example.com"
        content = asyncio.run(crawl_website(test_url))
        self.assertIsInstance(content, str)
        self.assertTrue(len(content) > 0)

if __name__ == "__main__":
    unittest.main()
