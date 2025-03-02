"""
crawler.py - Core module for crawling websites.
Implements asynchronous crawling with retries, caching, and validations.
"""

import asyncio
import time
from typing import Dict
import validators
from crawl4ai import AsyncWebCrawler  # Ensure this dependency is installed
from common.logger import logger

# In-memory cache for recently crawled content to avoid duplicate crawling
_cache: Dict[str, str] = {}

async def crawl_website(url: str, retries: int = 3, delay: float = 1.0) -> str:
    """
    Asynchronously crawl the given URL and return its Markdown content.
    
    Parameters:
        url (str): The website URL to crawl.
        retries (int): Number of retry attempts in case of failure.
        delay (float): Delay (in seconds) between retry attempts.
    
    Returns:
        str: The crawled content in Markdown format.
    
    Raises:
        ValueError: If the provided URL is invalid.
        Exception: If crawling fails after the specified number of retries.
    """
    if not validators.url(url):
        logger.error("Invalid URL provided: %s", url)
        raise ValueError("Invalid URL provided.")

    if url in _cache:
        logger.info("Returning cached content for URL: %s", url)
        return _cache[url]

    logger.info("Initiating crawl for URL: %s", url)
    overall_start = time.time()
    attempt = 0

    while attempt < retries:
        try:
            start_time = time.time()
            async with AsyncWebCrawler() as crawler:
                result = await crawler.arun(url=url)
            elapsed = time.time() - start_time
            logger.info("Crawl attempt %d succeeded in %.2f seconds for URL: %s", attempt + 1, elapsed, url)
            content = result.markdown.strip() if result and result.markdown else ""
            if not content:
                logger.warning("No content extracted for URL: %s", url)
            else:
                logger.info("Content extracted successfully for URL: %s", url)
            _cache[url] = content
            total_time = time.time() - overall_start
            logger.info("Total crawl time for URL %s: %.2f seconds", url, total_time)
            return content
        except Exception as e:
            attempt += 1
            logger.exception("Error during crawl attempt %d for URL %s: %s", attempt, url, e)
            if attempt < retries:
                logger.info("Retrying in %.1f seconds...", delay)
                await asyncio.sleep(delay)
            else:
                logger.error("Max retries reached for URL: %s", url)
                raise Exception(f"Failed to crawl URL {url} after {retries} attempts.") from e
    return ""

def crawl_website_sync(url: str) -> str:
    """
    Synchronously execute the asynchronous crawl_website function.
    
    Parameters:
        url (str): The website URL to crawl.
    
    Returns:
        str: The crawled content.
    """
    return asyncio.run(crawl_website(url))
