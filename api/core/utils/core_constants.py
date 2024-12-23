"""
File: api/core/utils/core_constants.py
Date updated: 2024-12-21
Author: Adil AJDAA
Email: a.ajdaa@outlook.com
Project: Ed Project
Description: Defines core constants for the application, such as pagination settings and encryption-related constants.
These constants are used consistently across the app to ensure uniform configuration.
Used Libraries: None
"""

# Constants for pagination
DEFAULT_PAGE_SIZE = 20  # Default number of items per page
MAX_PAGE_SIZE = 100  # Maximum allowed number of items per page

# Encryption related constants
ENCRYPTION_KEY_LENGTH = 44  # Length of the encryption key (for symmetric encryption like AES)
MIN_PASSWORD_LENGTH = 8  # Minimum length for user passwords
