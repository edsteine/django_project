import logging
import os
import sys

from datetime import timedelta
from pathlib import Path

# Function to get the logging configuration
from typing import Any

# import environ
import structlog


# from environ import Env
from environ import Env  # type: ignore[import-untyped]

# Initialize environment variables using environ

env_variables = Env()

# Load environment variables from a `.env` file. Ensure `.env` exists in the project root.
# Env.read_env(".env")
Env.read_env()

logger = logging.getLogger(__name__)

# Base directory for project structure
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = BASE_DIR / "logs"  # Directory for log files
os.makedirs(LOGS_DIR, exist_ok=True)  # Create logs directory if it doesn't exist

# Required environment variables for security and database configuration
required_env_vars: list[str] = [
    "DJANGO_ENVIRONMENT",
    "DJANGO_SETTINGS_MODULE",
    "TIME_ZONE",
    "DJANGO_SECRET_KEY",
    "DJANGO_DEBUG",
    "ALLOWED_HOSTS",
    "INTERNAL_IPS",
    "CORS_ALLOWED_ORIGINS",
    "CORS_ORIGIN_WHITELIST",
    "DB_ENGINE",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST",
    "DB_PORT",
    "CACHE_BACKEND",
    "REDIS_CACHE_URL",
    "EMAIL_BACKEND",
    "EMAIL_HOST",
    "EMAIL_PORT",
    "EMAIL_USE_TLS",
    "EMAIL_HOST_USER",
    "EMAIL_HOST_PASSWORD",
    "ENCRYPTION_KEY",
    "ENCRYPTION_ALGORITHM",
    "SENTRY_DSN",
    "AWS_STORAGE_BUCKET_NAME",
    "AWS_S3_REGION_NAME",
    "GITHUB_API_KEY",
    "STRIPE_SECRET_KEY",
    "SENDGRID_API_KEY",
    "LOGGING_LEVEL",
    "LOGGING_BACKEND",
    "SECURE_SSL_REDIRECT",
    "SECURE_HSTS_SECONDS",
    "SECURE_HSTS_INCLUDE_SUBDOMAINS",
    "SECURE_HSTS_PRELOAD",
    "CSRF_COOKIE_SECURE",
    "SESSION_COOKIE_SECURE",
    "DEFAULT_FILE_STORAGE",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_S3_CUSTOM_DOMAIN",
    "FEATURE_X_ENABLED",
    "ML_SERVICE_URL",
    "GRAPHQL_ENDPOINT",
    "AI_CHAT_SERVICE_URL",
    "AI_CHAT_API_KEY",
    "AI_CHAT_MODEL",
    "CLAUDE_API_URL",
    "CLAUDE_API_KEY",
    "DATABASE_POOL_SIZE",
    "DATABASE_MAX_CONNS",
    "DJANGO_DEV_TOOLBAR",
]
# Check for missing environment variables
missing_vars: list[str] = []
for var_name in required_env_vars:
    var_value = env_variables(var_name, default=None)
    if var_value is None or not var_value.strip():
        missing_vars.append(var_name)

# If any required environment variables are missing, print and exit
if missing_vars:
    error_message = "The following environment variables are missing or empty:\n"
    error_message += ", ".join(missing_vars)
    logger.error(error_message)
    sys.exit(1)

# Common Django settings
SECRET_KEY = env_variables("DJANGO_SECRET_KEY")
DEBUG = env_variables("DJANGO_DEBUG")
ALLOWED_HOSTS = env_variables.list("DJANGO_ALLOWED_HOSTS")
DB_ENGINE = env_variables("DB_ENGINE")
DB_NAME = env_variables("DB_NAME")
DB_USER = env_variables("DB_USER")
DB_PASSWORD = env_variables("DB_PASSWORD")
DB_HOST = env_variables("DB_HOST")
DB_PORT = env_variables("DB_PORT")
CACHE_BACKEND = env_variables("CACHE_BACKEND")
EMAIL_BACKEND = env_variables("EMAIL_BACKEND")
DJANGO_ALLOWED_HOSTS = env_variables("DJANGO_ALLOWED_HOSTS")
EMAIL_HOST = env_variables("EMAIL_HOST")
EMAIL_PORT = env_variables("EMAIL_PORT")
EMAIL_USE_TLS = env_variables("EMAIL_USE_TLS")
EMAIL_HOST_USER = env_variables("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env_variables("EMAIL_HOST_PASSWORD")
# CORS_ALLOWED_ORIGINS = env_variables.list("CORS_ALLOWED_ORIGINS")

# Installed applications for the project
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "api.V1.resources.users",
    "debug_toolbar",
    "django_extensions",  # Recommended dev tools
    "drf_yasg",
]

# Custom user model for the project
AUTH_USER_MODEL = "users.User"
ROOT_URLCONF = "config_project.project_urls"  # Adjust to match your project's URL configuration path

# Middleware configuration
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

# JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# Static file settings
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "assets",  # Example additional directory
]

# Internationalization settings
LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_TZ = True
TIME_ZONE = env_variables("TIME_ZONE")  # Adjust default if needed

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Configure structlog to provide structured and human-readable logging
log_renderer = structlog.dev.ConsoleRenderer() if DEBUG else structlog.processors.JSONRenderer()

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        log_renderer,  # Choose the renderer based on DEBUG
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)


# Update the type annotation to be more specific
def get_logging_config(log_level: str = "INFO") -> dict[str, Any]:
    """Logging configuration with correct type annotations."""
    log_renderer = structlog.dev.ConsoleRenderer() if DEBUG else structlog.processors.JSONRenderer()

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "structlog": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": log_renderer,  # Use appropriate renderer
                "foreign_pre_chain": [
                    structlog.stdlib.add_logger_name,
                    structlog.stdlib.add_log_level,
                    structlog.processors.TimeStamper(fmt="iso"),
                ],
            },
        },
        "handlers": {
            "console": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "structlog",
            },
            "file": {
                "level": log_level,
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOGS_DIR / "django.log",
                "maxBytes": 10 * 1024 * 1024,  # 10MB
                "backupCount": 5,
                "formatter": "structlog",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": True,
            },
        },
    }


# Apply logging configuration
LOGGING = get_logging_config()  # Configure logging with default log level "INFO"

# Debug Toolbar Configuration
INTERNAL_IPS = env_variables.list("INTERNAL_IPS")

# Debug settings for development
ALLOWED_HOSTS = env_variables.list("ALLOWED_HOSTS")

# Disable SSL and secure cookies in development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# CORS settings for development (allow local frontend)
# CORS_ALLOWED_ORIGINS = env_variables.list("CORS_ALLOWED_ORIGINS")

# Extend JWT access token lifetime for development convenience
SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(hours=1)

# Logging setup for development (use INFO level for more verbose logs)
LOGGING = get_logging_config(log_level="INFO")

# Optional: Email backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env_variables("DB_NAME", default="dev_db"),
        "USER": env_variables("DB_USER", default="dev_user"),
        "PASSWORD": env_variables("DB_PASSWORD", default="dev_password"),
        "HOST": env_variables("DB_HOST", default="localhost"),
        "PORT": env_variables("DB_PORT", default="5432"),
    },
}

# Django Debug Toolbar configuration
DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

# Optional performance and development tools
SHELL_PLUS = "ipython"  # If using django-extensions
