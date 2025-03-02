"""
lambda_handler.py - AWS Lambda or local entry point for the crawler module.
Loads configuration, crawls a website, saves the result, updates config, and optionally triggers the quiz process.
Supports both AWS and local modes.
"""

import json
import time
import asyncio
from crawler import crawler  # Import your crawler logic
from common.file_manager import save_content
from common.logger import logger
from common.config_manager import load_config, save_config
from common.config import USE_AWS

if USE_AWS:
    import boto3
    lambda_client = boto3.client("lambda")

def lambda_handler(event, context):
    logger.info("Crawler process triggered.")
    overall_start = time.time()

    try:
        # Load configuration
        config = load_config()
        # Find the first record that hasn't been processed
        record = next((rec for rec in config if not rec.get("extracted", False)), None)
        if not record:
            logger.info("No pending URL found in configuration.")
            return {"statusCode": 200, "body": json.dumps("No pending URL to process.")}
        
        website_url = record.get("website_url")
        if not website_url:
            logger.error("Configuration record missing 'website_url'.")
            return {"statusCode": 400, "body": json.dumps("Invalid configuration record.")}
        
        logger.info("Starting crawl for URL: %s", website_url)
        crawl_start = time.time()
        website_content = asyncio.run(crawler.crawl_website(website_url))
        crawl_elapsed = time.time() - crawl_start
        logger.info("Crawling completed in %.2f seconds for URL: %s", crawl_elapsed, website_url)

        if not website_content:
            logger.error("No content retrieved from URL: %s", website_url)
            raise Exception("No content retrieved.")

        # Save crawled content
        intermediate_key = save_content(website_url, website_content, folder="intermediate")
        logger.info("Intermediate content saved with key/path: %s", intermediate_key)

        # Update configuration to mark URL as processed
        record["extracted"] = True
        record["intermediate_result"] = intermediate_key
        save_config(config)

        overall_elapsed = time.time() - overall_start
        logger.info("Crawler process completed in %.2f seconds for URL: %s", overall_elapsed, website_url)

        # Optionally trigger Quiz process if running in AWS mode
        if USE_AWS:
            quiz_event = {"website_url": website_url, "s3_key": intermediate_key}
            try:
                lambda_client.invoke(
                    FunctionName="QuizLambda",  # Update with your Quiz Lambda function name if needed
                    InvocationType="Event",
                    Payload=json.dumps(quiz_event)
                )
                logger.info("Quiz Lambda invoked for URL: %s", website_url)
            except lambda_client.exceptions.ResourceNotFoundException as e:
                logger.warning("Quiz Lambda not found. Skipping invocation: %s", e)
        else:
            logger.info("Local mode: Skipping Quiz Lambda invocation.")

        return {"statusCode": 200, "body": json.dumps(f"Crawling complete for {website_url}")}
    except Exception as e:
        logger.exception("Error in crawler process: %s", e)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

# Allow running as a script in local mode
if __name__ == "__main__":
    lambda_handler({}, None)
