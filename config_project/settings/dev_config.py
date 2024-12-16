"""Development-specific settings.

Extends base_config.py with development-specific settings.
Configures development-level database, debugging, and logging.
"""

from .base_config import *  # noqa: F403

# Debug Toolbar Configuration
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

# Debug settings for development
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Disable SSL and secure cookies in development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# CORS settings for development (allow local frontend)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Example React dev server
    "http://127.0.0.1:3000",
]

# Extend JWT access token lifetime for development convenience
SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(hours=1)  # noqa: F405

# Logging setup for development (use INFO level for more verbose logs)
LOGGING = get_logging_config(log_level="INFO")  # noqa: F405

# Optional: Email backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Development-specific installed apps
INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
    "django_extensions",  # Recommended dev tools
]

# Development middleware
MIDDLEWARE += [  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DB_NAME,  # noqa: F405
        "USER": DB_USER,  # noqa: F405
        "PASSWORD": DB_PASSWORD,  # noqa: F405
        "HOST": DB_HOST,  # noqa: F405
        "PORT": DB_PORT,  # noqa: F405
    },
}

# Django Debug Toolbar configuration
DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

# Optional performance and development tools
SHELL_PLUS = "ipython"  # If using django-extensions
