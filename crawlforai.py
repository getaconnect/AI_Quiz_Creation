import asyncio
from crawl4ai import *

website_url = "https://groq.com/" #Change this to the url that you want to scrape

output_file_name = "result_groq" #Change this according to the website name used for scrapping and the location you want to store it in your local system

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=website_url, #change the link 
        )
        with open(output_file_name + ".txt", "w", encoding="utf-8") as file:
            file.write(result.markdown)
        # print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())