from datetime import timedelta

from .base_config import *  # noqa: F403

# Debug Toolbar Configuration
INTERNAL_IPS = env_variables.list("INTERNAL_IPS")  # noqa: F405

# Debug settings for development
DEBUG = True
ALLOWED_HOSTS = env_variables.list("ALLOWED_HOSTS")  # noqa: F405

# Disable SSL and secure cookies in development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# CORS settings for development (allow local frontend)
CORS_ALLOWED_ORIGINS = env_variables.list("CORS_ALLOWED_ORIGINS")  # noqa: F405

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
        "NAME": env_variables("DB_NAME", default="dev_db"),  # noqa: F405
        "USER": env_variables("DB_USER", default="dev_user"),  # noqa: F405
        "PASSWORD": env_variables("DB_PASSWORD", default="dev_password"),  # noqa: F405
        "HOST": env_variables("DB_HOST", default="localhost"),  # noqa: F405
        "PORT": env_variables("DB_PORT", default="5432"),  # noqa: F405
    },
}

# Django Debug Toolbar configuration
DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

# Optional performance and development tools
SHELL_PLUS = "ipython"  # If using django-extensions
