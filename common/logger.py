"""
logger.py - Shared logging configuration for AI Quiz Creation Project.
Configures both console and file logging with rotation.
"""

import logging
from logging.handlers import RotatingFileHandler
from common.config import LOG_LEVEL

LOG_FILE = "ai_quiz.log"

logger = logging.getLogger("AIQuizLogger")
logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.DEBUG))

# Prevent adding duplicate handlers if already configured
if not logger.handlers:
    # Console handler for INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File handler for DEBUG and above with rotation
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=2)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
