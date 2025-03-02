"""
file_manager.py - Shared module for file operations.
Handles generating file names and saving/retrieving content.
Supports both AWS S3 and local file system storage.
"""

import os
import datetime
import time
from urllib.parse import urlparse
from common.logger import logger
from common.config import USE_AWS

if USE_AWS:
    import boto3
    from common.config import S3_BUCKET
    s3_client = boto3.client('s3')
else:
    from common.config import LOCAL_RESULT_FOLDER
    # Ensure local results directory exists
    if not os.path.exists(LOCAL_RESULT_FOLDER):
        os.makedirs(LOCAL_RESULT_FOLDER, exist_ok=True)

def generate_file_name(url: str, extension: str = "txt") -> str:
    """
    Generate a file name using the URL's domain and current timestamp.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace("www.", "")
    if not domain:
        domain = parsed_url.path.strip("/").replace("/", "_")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{domain}_{timestamp}.{extension}"

def save_content(url: str, content: str, folder: str = None) -> str:
    """
    Save content either to AWS S3 or the local file system.
    Returns the storage key (for S3) or file path (for local).
    """
    start_time = time.time()
    file_name = generate_file_name(url)
    if USE_AWS:
        from common.config import S3_BUCKET
        s3_key = f"{folder or 'result'}/{file_name}"
        try:
            s3_client.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=content.encode("utf-8"))
            elapsed = time.time() - start_time
            logger.info("Content saved to S3 at key: %s in %.2f seconds", s3_key, elapsed)
            return s3_key
        except Exception as e:
            logger.exception("Failed to save content to S3: %s", e)
            raise
    else:
        from common.config import LOCAL_RESULT_FOLDER
        folder_path = os.path.join(LOCAL_RESULT_FOLDER, folder or "result")
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            elapsed = time.time() - start_time
            logger.info("Content saved locally at path: %s in %.2f seconds", file_path, elapsed)
            return file_path
        except Exception as e:
            logger.exception("Failed to save content locally: %s", e)
            raise

def get_content(storage_key: str) -> str:
    """
    Retrieve content from AWS S3 or the local file system using its key or path.
    """
    start_time = time.time()
    if USE_AWS:
        from common.config import S3_BUCKET
        try:
            response = s3_client.get_object(Bucket=S3_BUCKET, Key=storage_key)
            content = response["Body"].read().decode("utf-8")
            elapsed = time.time() - start_time
            logger.info("Content retrieved from S3 for key: %s in %.2f seconds", storage_key, elapsed)
            return content
        except Exception as e:
            logger.exception("Failed to retrieve content from S3: %s", e)
            raise
    else:
        try:
            with open(storage_key, "r", encoding="utf-8") as f:
                content = f.read()
            elapsed = time.time() - start_time
            logger.info("Content retrieved locally from path: %s in %.2f seconds", storage_key, elapsed)
            return content
        except Exception as e:
            logger.exception("Failed to retrieve content locally: %s", e)
            raise
