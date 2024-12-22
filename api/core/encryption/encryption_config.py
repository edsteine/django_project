"""
File: api/core/encryption/encryption_config.py
Date updated: 2024-12-21
Author: Adil AJDAA
Email: a.ajdaa@outlook.com
Project: Ed Project
Description: Configures encryption settings, including key and algorithm, from environment variables.
Used Libraries: environ, logging
"""

import logging

from environ import Env  # type: ignore[import-untyped]

# Constants for environment types
ENV_DEV = "dev"

# Initialize the Env object to load and parse environment variables
env_variables = Env()

# Determine the environment (development or production)
environment: str = env_variables("DJANGO_ENVIRONMENT") or ENV_DEV

# Configure logging based on environment
log_level = logging.INFO if environment == ENV_DEV else logging.ERROR
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

# Load environment variables based on the environment
if environment == ENV_DEV:
    env_variables.read_env(overwrite=True)  # Load .env file for development environment

# Fetch encryption settings from the environment
ENCRYPTION_KEY: str = env_variables.str("ENCRYPTION_KEY")
ENCRYPTION_ALGORITHM: str = env_variables.str("ENCRYPTION_ALGORITHM")

# Validate encryption settings
try:
    if not ENCRYPTION_KEY:
        raise ValueError(f"No encryption key found in {environment} environment.")
    if not ENCRYPTION_ALGORITHM:
        raise ValueError(f"No encryption algorithm found in {environment} environment.")
    logger.info("%s encryption settings are securely configured.", environment.capitalize())
except ValueError as e:
    # logger.error(f"Configuration Error: {e}")
    logger.info("Configuration Error: %s", e)
    raise  # Ensure invalid settings stop the application
