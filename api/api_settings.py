# api/config_api/api_settings.py
"""API settings and configuration.

Contains constants and configurations for the API behavior,
such as versioning, host, and pagination settings.
"""

API_VERSION: str = "v1"
API_HOST: str = "api.example.com"
DEFAULT_PAGE_SIZE: int = 20
MAX_PAGE_SIZE: int = 100
