from datetime import timedelta

from .base_config import *  # noqa: F403

# Disable DEBUG and set sensible defaults
DEBUG = False
ALLOWED_HOSTS = env_variables.list("DJANGO_ALLOWED_HOSTS")  # noqa: F405
SENTRY_DSN = env_variables("SENTRY_DSN")  # noqa: F405

# Database configuration for production using environment variables
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env_variables("PROD_DB_NAME", default="prod_db"),  # noqa: F405
        "USER": env_variables("PROD_DB_USER", default="prod_user"),  # noqa: F405
        "PASSWORD": env_variables("PROD_DB_PASSWORD", default="prod_password"),  # noqa: F405
        "HOST": env_variables("PROD_DB_HOST", default="localhost"),  # noqa: F405
        "PORT": env_variables("PROD_DB_PORT", default="5432"),  # noqa: F405
        # Optional: Connection pooling and performance tuning
        "CONN_MAX_AGE": 600,  # Connection persistent for 10 minutes
        "OPTIONS": {
            "sslmode": "require",  # Enforce SSL for database connection
        },
    },
}

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Enhanced security headers
SECURE_HSTS_SECONDS = 31536000  # 1 year HSTS
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Additional security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# Performance and proxy settings
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CORS configuration
CORS_ALLOWED_ORIGINS = env_variables.list("CORS_ALLOWED_ORIGINS", default=[])  # noqa: F405
CORS_ORIGIN_WHITELIST = env_variables.list("CORS_ORIGIN_WHITELIST", default=[])  # noqa: F405

# Reduce JWT access token lifetime for security
SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(minutes=15)  # noqa: F405

# Logging setup for production (use ERROR level for fewer log entries)
LOGGING = get_logging_config(log_level="ERROR")  # noqa: F405

# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env_variables("PROD_EMAIL_HOST", default="smtp.example.com")  # noqa: F405
EMAIL_PORT = env_variables("PROD_EMAIL_PORT", default="587")  # noqa: F405
EMAIL_HOST_USER = env_variables(  # noqa: F405
    "PROD_EMAIL_HOST_USER", default="user@example.com"
)
EMAIL_HOST_PASSWORD = env_variables("PROD_EMAIL_HOST_PASSWORD")  # noqa: F405
EMAIL_USE_TLS = True

# Caching configuration
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env_variables("REDIS_CACHE_URL", default="redis://localhost:6379/1"),  # noqa: F405
        "OPTIONS": {
            "MAX_ENTRIES": 10000,
        },
    },
}

# Static and media file settings
AWS_STORAGE_BUCKET_NAME = env_variables("AWS_STORAGE_BUCKET_NAME")  # noqa: F405
AWS_S3_REGION_NAME = env_variables("AWS_S3_REGION_NAME")  # noqa: F405
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# Static files
STATIC_LOCATION = "static"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Media files
PUBLIC_MEDIA_LOCATION = "media"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Installed apps for production
INSTALLED_APPS += [  # noqa: F405
    "storages",  # For S3 file storage
]

# Rate limiting and protection
REST_FRAMEWORK.update(  # noqa: F405
    {
        "DEFAULT_THROTTLE_CLASSES": [
            "rest_framework.throttling.AnonRateThrottle",
            "rest_framework.throttling.UserRateThrottle",
        ],
        "DEFAULT_THROTTLE_RATES": {"anon": "100/day", "user": "1000/day"},
    },
)
