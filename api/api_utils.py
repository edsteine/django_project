# api/config_api/api_utils.py
"""API utility functions.

Provides helper functions for API operations, such as retrieving the
current API version and generating unique API keys for users.
"""

import hashlib

from api.api_settings import API_VERSION


def get_api_version():
    """Returns the current API version."""
    return API_VERSION


def generate_api_key(user):
    """Generate a unique API key for the given user."""
    return hashlib.sha256(user.encode()).hexdigest()
