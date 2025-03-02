"""
config_manager.py - Manages the configuration file.
Provides functions to load and update the configuration (e.g., config.json).
Supports both AWS S3 and local file system.
"""

import json
from common.logger import logger
from common.config import USE_AWS

if USE_AWS:
    import boto3
    from common.config import S3_BUCKET, CONFIG_KEY
    s3_client = boto3.client("s3")

def load_config() -> list:
    """
    Load configuration from AWS S3 or local file system.
    """
    try:
        if USE_AWS:
            response = s3_client.get_object(Bucket=S3_BUCKET, Key=CONFIG_KEY)
            config_data = response["Body"].read().decode("utf-8")
            logger.info("Configuration loaded from S3 successfully.")
        else:
            from common.config import LOCAL_CONFIG_PATH
            with open(LOCAL_CONFIG_PATH, "r", encoding="utf-8") as f:
                config_data = f.read()
            logger.info("Configuration loaded from local file successfully.")
        return json.loads(config_data)
    except Exception as e:
        logger.exception("Error loading configuration: %s", e)
        raise

def save_config(config: list) -> None:
    """
    Save configuration to AWS S3 or local file system.
    """
    try:
        config_str = json.dumps(config, indent=4)
        if USE_AWS:
            from common.config import S3_BUCKET, CONFIG_KEY
            s3_client.put_object(Bucket=S3_BUCKET, Key=CONFIG_KEY, Body=config_str.encode("utf-8"))
            logger.info("Configuration saved to S3 successfully.")
        else:
            from common.config import LOCAL_CONFIG_PATH
            with open(LOCAL_CONFIG_PATH, "w", encoding="utf-8") as f:
                f.write(config_str)
            logger.info("Configuration saved to local file successfully.")
    except Exception as e:
        logger.exception("Error saving configuration: %s", e)
        raise
