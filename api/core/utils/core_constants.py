"""
File: api/core/utils/core_constants.py
Date updated: 2024-12-21
Author: Adil AJDAA
Email: a.ajdaa@outlook.com
Project: Ed Project
Description: Defines core constants for the application, such as pagination settings and encryption-related constants.
These constants are used consistently across the app to ensure uniform configuration.API settings and configuration.
Contains constants and configurations for the API behavior,
such as versioning, host, and pagination settings.
Used Libraries: hashlib
"""

import hashlib

# Constants for pagination
DEFAULT_PAGE_SIZE: int = 20  # Default number of items per page
MAX_PAGE_SIZE: int = 100  # Maximum allowed number of items per page

# Encryption related constants
ENCRYPTION_KEY_LENGTH = 44  # Length of the encryption key (for symmetric encryption like AES)
MIN_PASSWORD_LENGTH = 8  # Minimum length for user passwords


API_VERSION: str = "v1"
API_HOST: str = "api.example.com"


def get_api_version() -> str:
    """Returns the current API version."""
    return API_VERSION


def generate_api_key(user: str) -> str:
    """Generate a unique API key for the given user."""
    return hashlib.sha256(user.encode()).hexdigest()
