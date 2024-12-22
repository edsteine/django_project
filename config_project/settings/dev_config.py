import logging
import os
import sys

from datetime import timedelta
from pathlib import Path

import structlog

from environ import Env  # type: ignore[import-untyped]

# Initialize environment

# Constants for environment types
ENV_DEV = "dev"
# Initialize the Env object to load and parse environment variables
env_variables = Env()
# Determine the environment (development or production)
environment: str = env_variables("DJANGO_ENVIRONMENT") or ENV_DEV

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
    "TESTING",
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
    "CORS_ALLOW_ALL_ORIGINS",
    "CORS_ALLOW_CREDENTIALS",
    "USE_I18N",
    "USE_TZ",
    "ROTATE_REFRESH_TOKENS",
    "BLACKLIST_AFTER_ROTATION",
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
DEBUG = env_variables.bool("DJANGO_DEBUG") or True
# LOGGING_LEVEL = env_variables.str("LOGGING_LEVEL") or "INFO")
LOGGING_LEVEL = "INFO"
if LOGGING_LEVEL not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    raise ValueError("Invalid LOGGING_LEVEL. Use DEBUG, INFO, WARNING, ERROR, or CRITICAL.")

SECRET_KEY = env_variables("DJANGO_SECRET_KEY") or "django-insecure-dev-key-change-this"

ALLOWED_HOSTS = env_variables.list("ALLOWED_HOSTS") or ["localhost", "127.0.0.1"]
INTERNAL_IPS = env_variables.list("INTERNAL_IPS") or ["127.0.0.1"]

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
        "ENGINE": env_variables("DB_ENGINE") or "django.db.backends.postgresql",
        "NAME": env_variables("DB_NAME") or "dev_db",
        "USER": env_variables("DB_USER") or "postgres",
        "PASSWORD": env_variables("DB_PASSWORD") or "postgres",
        "HOST": env_variables("DB_HOST") or "localhost",
        "PORT": env_variables("DB_PORT") or "5432",
        "CONN_MAX_AGE": 60,
        "OPTIONS": {
            "connect_timeout": 10,
        },
        "SSL_REQUIRE": False,
    }
}

# Cache settings
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env_variables("REDIS_CACHE_URL") or "redis://127.0.0.1:6379/1",
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
LANGUAGE_CODE = "en-us"
TIME_ZONE = env_variables("TIME_ZONE") or "UTC"
USE_I18N = env_variables.bool("USE_I18N") or True
USE_TZ = env_variables.bool("USE_TZ") or True

# Static files
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "assets"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Development security settings

SECURE_HSTS_SECONDS = env_variables("SECURE_HSTS_SECONDS") or 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_variables.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS") or False
SECURE_HSTS_PRELOAD = env_variables.bool("SECURE_HSTS_PRELOAD") or False
SECURE_SSL_REDIRECT = env_variables.bool("SECURE_SSL_REDIRECT") or False
SESSION_COOKIE_SECURE = env_variables.bool("SESSION_COOKIE_SECURE") or False
CSRF_COOKIE_SECURE = env_variables.bool("CSRF_COOKIE_SECURE") or False
CORS_ALLOW_ALL_ORIGINS = env_variables.bool("CORS_ALLOW_ALL_ORIGINS") or True
CORS_ALLOW_CREDENTIALS = env_variables.bool("CORS_ALLOW_CREDENTIALS") or True
CORS_ALLOWED_ORIGINS = env_variables.list("CORS_ALLOWED_ORIGINS") or ["http://localhost:3000", "http://127.0.0.1:3000"]

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
    "ROTATE_REFRESH_TOKENS": env_variables.bool("ROTATE_REFRESH_TOKENS") or True,
    "BLACKLIST_AFTER_ROTATION": env_variables.bool("BLACKLIST_AFTER_ROTATION") or True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# Email settings
EMAIL_BACKEND = env_variables("EMAIL_BACKEND") or "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = env_variables("EMAIL_HOST") or "localhost"
EMAIL_PORT = env_variables.int("EMAIL_PORT") or 1025
EMAIL_HOST_USER = env_variables("EMAIL_HOST_USER") or ""
EMAIL_HOST_PASSWORD = env_variables("EMAIL_HOST_PASSWORD") or ""
EMAIL_USE_TLS = env_variables.bool("EMAIL_USE_TLS") or False

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
            "class": "django.utils.log.AdminEmailHandler",
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
            "level": env_variables("LOGGING_LEVEL") or "INFO",
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

FEATURE_X_ENABLED = env_variables.bool("FEATURE_X_ENABLED") or False


# Testing & Coverage
TESTING = env_variables.bool("TESTING") or True
if TESTING:
    DATABASES["default"] = {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
