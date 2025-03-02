"""
lambda_handler.py - AWS Lambda or local entry point for the quiz module.
Loads configuration, retrieves an intermediate result, generates a quiz,
saves the final output, and updates the configuration.
Supports both AWS and local file system modes.
"""

import json
import time
from common.file_manager import get_content, save_content
from quiz import quiz_generator  # Import the core quiz generator module
from common.logger import logger
from common.config_manager import load_config, save_config

def lambda_handler(event, context):
    logger.info("Quiz process triggered.")
    overall_start = time.time()

    try:
        # Load configuration from S3 or local file system
        config = load_config()
        # Find the first record that has been extracted but not yet processed for quiz generation.
        record = next(
            (
                rec for rec in config 
                if rec.get("extracted", False) 
                and not rec.get("quiz_created", False) 
                and rec.get("intermediate_result")
            ),
            None
        )
        if not record:
            logger.info("No pending record for quiz creation found.")
            return {"statusCode": 200, "body": json.dumps("No pending record to process.")}
        
        website_url = record.get("website_url")
        storage_key = record.get("intermediate_result")

        logger.info("Processing quiz for URL: %s", website_url)

        # Retrieve intermediate content (either from S3 or local file system)
        retrieval_start = time.time()
        intermediate_content = get_content(storage_key)
        retrieval_elapsed = time.time() - retrieval_start
        logger.info("Intermediate content retrieved in %.2f seconds.", retrieval_elapsed)

        if not intermediate_content:
            raise Exception("Intermediate content is empty.")

        # Generate the quiz from the intermediate content
        quiz_start = time.time()
        quiz_output = quiz_generator.generate_quiz(intermediate_content)
        quiz_elapsed = time.time() - quiz_start
        logger.info("Quiz generation completed in %.2f seconds.", quiz_elapsed)

        if not quiz_output:
            raise Exception("Quiz generation failed.")

        # Save the final quiz output (either to S3 or local file system)
        final_key = save_content(website_url, quiz_output, folder="final")
        logger.info("Final quiz saved with key/path: %s", final_key)

        # Update the configuration record to mark the quiz as created
        record["quiz_created"] = True
        record["final_result"] = final_key
        save_config(config)

        overall_elapsed = time.time() - overall_start
        logger.info("Quiz process completed in %.2f seconds for URL: %s", overall_elapsed, website_url)
        return {"statusCode": 200, "body": json.dumps(f"Quiz created for {website_url}")}
    except Exception as e:
        logger.exception("Error in Quiz process: %s", e)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

# Allow running as a standalone script for local testing.
if __name__ == "__main__":
    lambda_handler({}, None)
