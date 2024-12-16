# api/test_config.py
"""Test environment specific settings.

Configures test database and test-specific features.
Sets up test runners and test-specific configurations.
Optimizes settings for testing environment.
"""

from .base_config import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    },
}

# Logging setup for testing (usually DEBUG or INFO)
LOGGING = get_logging_config(log_level="DEBUG")  # Use DEBUG level for testing # noqa: F405
