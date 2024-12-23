import logging
import os
import sys

from datetime import timedelta
from pathlib import Path

# import sentry_sdk
import structlog

from environ import Env  # type: ignore[import-untyped]

# from sentry_sdk.integrations.django import DjangoIntegration

# Constants for environment types
ENV_DEV = "dev"
# Initialize the Env object to load and parse environment variables
env_variables = Env()
# Determine the environment (development or production)
environment: str = env_variables.str("DJANGO_ENVIRONMENT") or ENV_DEV

# Load environment variables based on the environment
if environment == ENV_DEV:
    env_variables.read_env(overwrite=True)  # Load .env file for development environment

# Base directory setup
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = BASE_DIR / "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

logger = logging.getLogger(__name__)

# Required environment variables check
required_env_vars: list[str] = [
    "DJANGO_ENVIRONMENT",
    "DJANGO_SETTINGS_MODULE",
    "TIME_ZONE",
    "DJANGO_SECRET_KEY",
    "DJANGO_DEBUG",
    "ALLOWED_HOSTS",
    "INTERNAL_IPS",
    "CORS_ALLOWED_ORIGINS",
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
    "SENTRY_DSN",
    "LOGGING_LEVEL",
    "LOGGING_BACKEND",
    "SECURE_SSL_REDIRECT",
    "SECURE_HSTS_SECONDS",
    "SECURE_HSTS_INCLUDE_SUBDOMAINS",
    "SECURE_HSTS_PRELOAD",
    "CSRF_COOKIE_SECURE",
    "SESSION_COOKIE_SECURE",
    "FEATURE_X_ENABLED",
    "CORS_ALLOW_ALL_ORIGINS",
    "CORS_ALLOW_CREDENTIALS",
    "USE_I18N",
    "USE_TZ",
    "ROTATE_REFRESH_TOKENS",
    "BLACKLIST_AFTER_ROTATION",
    "ENCRYPTION_KEY",
    "ENCRYPTION_ALGORITHM",
    # "TESTING",
    # "ML_SERVICE_URL",
    # "GRAPHQL_ENDPOINT",
    # "AI_CHAT_SERVICE_URL",
    # "AI_CHAT_API_KEY",
    # "AI_CHAT_MODEL",
    # "CLAUDE_API_URL",
    # "CLAUDE_API_KEY",
    # "DATABASE_POOL_SIZE",
    # "DATABASE_MAX_CONNS",
    # "DEFAULT_FILE_STORAGE",
    # "AWS_ACCESS_KEY_ID",
    # "AWS_SECRET_ACCESS_KEY",
    # "AWS_S3_CUSTOM_DOMAIN",
    # "DJANGO_DEV_TOOLBAR",
    # "AWS_STORAGE_BUCKET_NAME",
    # "AWS_S3_REGION_NAME",
    # "GITHUB_API_KEY",
    # "SENDGRID_API_KEY",
]

missing_vars: list[str] = []
for var_name in required_env_vars:
    var_value = env_variables(var_name)
    if var_value is None or not var_value.strip():
        missing_vars.append(var_name)

if missing_vars:
    error_message = "The following environment variables are missing or empty:\n"
    error_message += ", ".join(missing_vars)
    logger.error(error_message)
    sys.exit(1)

# Core Django Settings
DEBUG = env_variables.bool("DJANGO_DEBUG")
LOGGING_LEVEL = env_variables.str("LOGGING_LEVEL")
# LOGGING_LEVEL = "INFO"
if LOGGING_LEVEL not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    raise ValueError("Invalid LOGGING_LEVEL. Use DEBUG, INFO, WARNING, ERROR, or CRITICAL.")

SECRET_KEY = env_variables.str("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = env_variables.list("ALLOWED_HOSTS")
INTERNAL_IPS = env_variables.list("INTERNAL_IPS")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "debug_toolbar",
    "django_extensions",
    "drf_yasg",
    "silk",
    # Local apps
    "api",
    "api.V1.resources.users",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "silk.middleware.SilkyMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config_project.project_urls"
AUTH_USER_MODEL = "users.User"

# Database with connection pooling
# Database configuration
DATABASES = {
    "default": {
        "ENGINE": env_variables.str("DB_ENGINE"),
        "NAME": env_variables.str("DB_NAME"),
        "USER": env_variables.str("DB_USER"),
        "PASSWORD": env_variables.str("DB_PASSWORD"),
        "HOST": env_variables.str("DB_HOST"),
        "PORT": env_variables.str("DB_PORT"),
        "CONN_MAX_AGE": 60,
        "OPTIONS": {
            "connect_timeout": 10,
            # "MAX_CONNS": env_variables.int("DATABASE_MAX_CONNS"),
            # "POOL_SIZE": env_variables.int("DATABASE_POOL_SIZE"),
            # "CONN_MAX_AGE": 60,  # Optional, controls connection persistence
        },
        "SSL_REQUIRE": False,
    }
}

# Cache settings
CACHES = {
    "default": {
        "BACKEND": env_variables.str("CACHE_BACKEND"),
        "LOCATION": env_variables.str("REDIS_CACHE_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "RETRY_ON_TIMEOUT": True,
            "MAX_CONNECTIONS": 1000,
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
        },
    }
}
# Templates
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
            "debug": DEBUG,
        },
    },
]

# Internationalization
LANGUAGE_CODE = env_variables.str("LANGUAGE_CODE")
TIME_ZONE = env_variables.str("TIME_ZONE")
USE_I18N = env_variables.bool("USE_I18N")
USE_TZ = env_variables.bool("USE_TZ")

# Static files
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "assets"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Development security settings

SECURE_HSTS_SECONDS = env_variables.str("SECURE_HSTS_SECONDS")
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_variables.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS")
SECURE_HSTS_PRELOAD = env_variables.bool("SECURE_HSTS_PRELOAD")
SECURE_SSL_REDIRECT = env_variables.bool("SECURE_SSL_REDIRECT")
SESSION_COOKIE_SECURE = env_variables.bool("SESSION_COOKIE_SECURE")
CSRF_COOKIE_SECURE = env_variables.bool("CSRF_COOKIE_SECURE")
CORS_ALLOW_ALL_ORIGINS = env_variables.bool("CORS_ALLOW_ALL_ORIGINS")
CORS_ALLOW_CREDENTIALS = env_variables.bool("CORS_ALLOW_CREDENTIALS")
CORS_ALLOWED_ORIGINS = env_variables.list("CORS_ALLOWED_ORIGINS")
# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/minute",
        "user": "1000/minute",
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": env_variables.bool("ROTATE_REFRESH_TOKENS"),
    "BLACKLIST_AFTER_ROTATION": env_variables.bool("BLACKLIST_AFTER_ROTATION"),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# Email settings
EMAIL_BACKEND = env_variables.str("EMAIL_BACKEND")
EMAIL_HOST = env_variables.str("EMAIL_HOST")
EMAIL_PORT = env_variables.int("EMAIL_PORT")
EMAIL_HOST_USER = env_variables.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env_variables.str("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env_variables.bool("EMAIL_USE_TLS")

# Structlog configuration
log_renderer = structlog.dev.ConsoleRenderer() if DEBUG else structlog.processors.JSONRenderer()

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        log_renderer,
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "structlog": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": log_renderer,
            "foreign_pre_chain": [
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
            ],
        },
    },
    "handlers": {
        "console": {
            "level": LOGGING_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "structlog",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": env_variables.str("LOGGING_BACKEND"),
        },
        "file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "django-dev.log",
            "maxBytes": 10 * 1024 * 1024,  # 10MB
            "backupCount": 5,
            "formatter": "structlog",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": LOGGING_LEVEL,
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

# Debug Toolbar settings
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
    "INTERCEPT_REDIRECTS": False,
    "SHOW_TEMPLATE_CONTEXT": True,
    "ENABLE_STACKTRACES": True,
}

# Django Extensions settings
SHELL_PLUS = "ipython"
SHELL_PLUS_PRINT_SQL = True
SHELL_PLUS_IMPORTS = [
    "from datetime import datetime, timedelta, date",
    "from django.conf import settings",
    "from django.core.cache import cache",
    "from django.db.models import Q, F, Count, Sum, Max, Min, Avg",
]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ADMINS = [("Admin Name", "admin@example.com")]


# Feature Flags

FEATURE_X_ENABLED = env_variables.bool("FEATURE_X_ENABLED")


# sentry_sdk.init(
#     dsn=env_variables.str("SENTRY_DSN"),
#     integrations=[DjangoIntegration()],
#     traces_sample_rate=1.0,  # Adjust as needed for performance tracking
# )
