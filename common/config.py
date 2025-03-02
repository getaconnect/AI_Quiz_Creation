"""
config.py - Shared configuration module for AI Quiz Creation Project.
Loads environment variables from the .env file and exposes configuration constants.
Supports both AWS and local file system modes.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# GOOGLE_API_KEY is required for quiz generation and should always be defined.
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY environment variable.")

# Operating mode: AWS or Local (default True for AWS)
USE_AWS: bool = os.getenv("USE_AWS", "True").lower() in ("true", "1", "yes")

if USE_AWS:
    # AWS S3 configuration
    S3_BUCKET: str = os.getenv("S3_BUCKET")
    if not S3_BUCKET:
        raise ValueError("Missing S3_BUCKET environment variable.")
    CONFIG_KEY: str = os.getenv("CONFIG_KEY", "config/config.json")
else:
    # Local file system configuration
    LOCAL_CONFIG_PATH: str = os.getenv("LOCAL_CONFIG_PATH", "config.json")

# Logging configuration
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "DEBUG")

# System prompt for quiz generation
SYSTEM_PROMPT: str = (
    "Please refer the attached file. It is a summary of a website.\n"
    "Using the attached file, identify the website's target customer.\n\n"
    "If the target customer is a business (B2B), create a quiz/assessment for them.\n\n"
    "If the target customer is a consumer (B2C), create a quiz/assessment for potential partners.\n\n"
    "The quiz should help the audience understand the problem solved by the website and its offerings. "
    "Keep it simple (10-15 questions), but extend if needed. Finally, calculate a score and provide "
    "a personalized message based on the score range."
)

if not USE_AWS:
    LOCAL_RESULT_FOLDER: str = os.getenv("LOCAL_RESULT_FOLDER", "results")
