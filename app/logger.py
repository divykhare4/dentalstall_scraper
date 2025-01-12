import logging
from logging.handlers import RotatingFileHandler
from settings import fetch_settings

# Setting up the logger
logger = logging.getLogger(fetch_settings().app_name)
logger.setLevel(fetch_settings().log_level)

# Formatter for logging messages
log_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Console logging handler
console_handler = logging.StreamHandler()
console_handler.setLevel(fetch_settings().log_level)
console_handler.setFormatter(log_formatter)

# File logging handler with rotation
log_file_path = fetch_settings().log_file
file_handler = RotatingFileHandler(
    log_file_path, maxBytes=1000000, backupCount=5)
file_handler.setLevel(fetch_settings().log_level)
file_handler.setFormatter(log_formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
