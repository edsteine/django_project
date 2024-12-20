import hashlib

from api.api_settings import API_VERSION


def get_api_version() -> str:
    """Returns the current API version."""
    return API_VERSION


def generate_api_key(user: str) -> str:
    """Generate a unique API key for the given user."""
    return hashlib.sha256(user.encode()).hexdigest()
