# import logging
# import os
# import sys

# from datetime import timedelta
# from pathlib import Path

# # Function to get the logging configuration
# from typing import Any

# # import environ
# import structlog


# # from environ import Env
# from environ import Env  # type: ignore[import-untyped]

# # Initialize environment variables using environ

# env_variables = Env()

# # Load environment variables from a `.env` file. Ensure `.env` exists in the project root.
# # Env.read_env(".env")
# Env.read_env()

# logger = logging.getLogger(__name__)

# # Base directory for project structure
# BASE_DIR = Path(__file__).resolve().parent.parent.parent
# LOGS_DIR = BASE_DIR / "logs"  # Directory for log files
# os.makedirs(LOGS_DIR, exist_ok=True)  # Create logs directory if it doesn't exist

# # Required environment variables for security and database configuration
# required_env_vars: list[str] = [
#     "DJANGO_SECRET_KEY",
#     "DB_NAME",
#     "DB_USER",
#     "DB_PASSWORD",
#     "DB_HOST",
#     "DJANGO_DEBUG",
#     "DJANGO_ALLOWED_HOSTS",
#     "DB_ENGINE",
#     "DB_PORT",
#     "CACHE_BACKEND",
#     "EMAIL_BACKEND",
#     "TIME_ZONE",
#     "EMAIL_HOST",
#     "EMAIL_PORT",
#     "EMAIL_USE_TLS",
#     "EMAIL_HOST_USER",
#     "EMAIL_HOST_PASSWORD",
#     # "CORS_ALLOWED_ORIGINS",
# ]

# # Check for missing environment variables
# missing_vars: list[str] = []
# for var_name in required_env_vars:
#     var_value = env_variables(var_name, default=None)
#     if var_value is None or not var_value.strip():
#         missing_vars.append(var_name)

# # If any required environment variables are missing, print and exit
# if missing_vars:
#     error_message = "The following environment variables are missing or empty:\n"
#     error_message += ", ".join(missing_vars)
#     logger.error(error_message)
#     sys.exit(1)

# # Common Django settings
# SECRET_KEY = env_variables("DJANGO_SECRET_KEY")
# DEBUG = env_variables("DJANGO_DEBUG")
# ALLOWED_HOSTS = env_variables.list("DJANGO_ALLOWED_HOSTS")
# DB_ENGINE = env_variables("DB_ENGINE")
# DB_NAME = env_variables("DB_NAME")
# DB_USER = env_variables("DB_USER")
# DB_PASSWORD = env_variables("DB_PASSWORD")
# DB_HOST = env_variables("DB_HOST")
# DB_PORT = env_variables("DB_PORT")
# CACHE_BACKEND = env_variables("CACHE_BACKEND")
# EMAIL_BACKEND = env_variables("EMAIL_BACKEND")
# DJANGO_ALLOWED_HOSTS = env_variables("DJANGO_ALLOWED_HOSTS")
# EMAIL_HOST = env_variables("EMAIL_HOST")
# EMAIL_PORT = env_variables("EMAIL_PORT")
# EMAIL_USE_TLS = env_variables("EMAIL_USE_TLS")
# EMAIL_HOST_USER = env_variables("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = env_variables("EMAIL_HOST_PASSWORD")
# # CORS_ALLOWED_ORIGINS = env_variables.list("CORS_ALLOWED_ORIGINS")

# # Installed applications for the project
# INSTALLED_APPS = [
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#     "rest_framework",
#     "rest_framework_simplejwt",
#     "corsheaders",
#     "api.V1.resources.users",
# ]

# # Custom user model for the project
# AUTH_USER_MODEL = "users.User"
# ROOT_URLCONF = "config_project.project_urls"  # Adjust to match your project's URL configuration path

# # Middleware configuration
# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "corsheaders.middleware.CorsMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

# # REST Framework settings
# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
#     "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
#     "PAGE_SIZE": 10,
# }

# # JWT settings
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
#     "ROTATE_REFRESH_TOKENS": True,
#     "BLACKLIST_AFTER_ROTATION": True,
#     "AUTH_HEADER_TYPES": ("Bearer",),
#     "USER_ID_FIELD": "id",
#     "USER_ID_CLAIM": "user_id",
# }

# # Static file settings
# STATIC_URL = "static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"
# STATICFILES_DIRS = [
#     BASE_DIR / "assets",  # Example additional directory
# ]

# # Internationalization settings
# LANGUAGE_CODE = "en-us"
# USE_I18N = True
# USE_TZ = True
# TIME_ZONE = env_variables("TIME_ZONE")  # Adjust default if needed

# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.debug",
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]

# # Configure structlog to provide structured and human-readable logging
# log_renderer = structlog.dev.ConsoleRenderer() if DEBUG else structlog.processors.JSONRenderer()

# structlog.configure(
#     processors=[
#         structlog.contextvars.merge_contextvars,
#         structlog.stdlib.add_logger_name,
#         structlog.stdlib.add_log_level,
#         structlog.processors.TimeStamper(fmt="iso"),
#         structlog.processors.StackInfoRenderer(),
#         structlog.processors.format_exc_info,
#         log_renderer,  # Choose the renderer based on DEBUG
#     ],
#     context_class=dict,
#     logger_factory=structlog.stdlib.LoggerFactory(),
#     wrapper_class=structlog.stdlib.BoundLogger,
#     cache_logger_on_first_use=True,
# )


# # Update the type annotation to be more specific
# def get_logging_config(log_level: str = "INFO") -> dict[str, Any]:
#     """Logging configuration with correct type annotations."""
#     log_renderer = structlog.dev.ConsoleRenderer() if DEBUG else structlog.processors.JSONRenderer()

#     return {
#         "version": 1,
#         "disable_existing_loggers": False,
#         "formatters": {
#             "structlog": {
#                 "()": structlog.stdlib.ProcessorFormatter,
#                 "processor": log_renderer,  # Use appropriate renderer
#                 "foreign_pre_chain": [
#                     structlog.stdlib.add_logger_name,
#                     structlog.stdlib.add_log_level,
#                     structlog.processors.TimeStamper(fmt="iso"),
#                 ],
#             },
#         },
#         "handlers": {
#             "console": {
#                 "level": log_level,
#                 "class": "logging.StreamHandler",
#                 "formatter": "structlog",
#             },
#             "file": {
#                 "level": log_level,
#                 "class": "logging.handlers.RotatingFileHandler",
#                 "filename": LOGS_DIR / "django.log",
#                 "maxBytes": 10 * 1024 * 1024,  # 10MB
#                 "backupCount": 5,
#                 "formatter": "structlog",
#             },
#         },
#         "loggers": {
#             "django": {
#                 "handlers": ["console", "file"],
#                 "level": log_level,
#                 "propagate": True,
#             },
#         },
#     }


# # Apply logging configuration
# LOGGING = get_logging_config()  # Configure logging with default log level "INFO"

# # Disable DEBUG and set sensible defaults
# ALLOWED_HOSTS = env_variables.list("DJANGO_ALLOWED_HOSTS")
# SENTRY_DSN = env_variables("SENTRY_DSN")

# # Database configuration for production using environment variables
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": env_variables("PROD_DB_NAME", default="prod_db"),
#         "USER": env_variables("PROD_DB_USER", default="prod_user"),
#         "PASSWORD": env_variables("PROD_DB_PASSWORD", default="prod_password"),
#         "HOST": env_variables("PROD_DB_HOST", default="localhost"),
#         "PORT": env_variables("PROD_DB_PORT", default="5432"),
#         # Optional: Connection pooling and performance tuning
#         "CONN_MAX_AGE": 600,  # Connection persistent for 10 minutes
#         "OPTIONS": {
#             "sslmode": "require",  # Enforce SSL for database connection
#         },
#     },
# }

# # Security settings for production
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# # Enhanced security headers
# SECURE_HSTS_SECONDS = 31536000  # 1 year HSTS
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# # Additional security settings
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = "DENY"

# # Performance and proxy settings
# USE_X_FORWARDED_HOST = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# # CORS configuration
# # CORS_ALLOWED_ORIGINS = env_variables.list("CORS_ALLOWED_ORIGINS", default=[])

# # Reduce JWT access token lifetime for security
# SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(minutes=15)

# # Logging setup for production (use ERROR level for fewer log entries)
# LOGGING = get_logging_config(log_level="ERROR")

# # Email configuration
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = env_variables("PROD_EMAIL_HOST", default="smtp.example.com")
# EMAIL_PORT = env_variables("PROD_EMAIL_PORT", default="587")
# EMAIL_HOST_USER = env_variables("PROD_EMAIL_HOST_USER", default="user@example.com")
# EMAIL_HOST_PASSWORD = env_variables("PROD_EMAIL_HOST_PASSWORD")
# EMAIL_USE_TLS = True

# # Caching configuration
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": env_variables("REDIS_CACHE_URL", default="redis://localhost:6379/1"),
#         "OPTIONS": {
#             "MAX_ENTRIES": 10000,
#         },
#     },
# }

# # Static and media file settings
# AWS_STORAGE_BUCKET_NAME = env_variables("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_REGION_NAME = env_variables("AWS_S3_REGION_NAME")
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# # Static files
# STATIC_LOCATION = "static"
# STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# # Media files
# PUBLIC_MEDIA_LOCATION = "media"
# MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# # Installed apps for production
# INSTALLED_APPS += [
#     "storages",  # For S3 file storage
# ]

# # Rate limiting and protection
# REST_FRAMEWORK.update(
#     {
#         "DEFAULT_THROTTLE_CLASSES": [
#             "rest_framework.throttling.AnonRateThrottle",
#             "rest_framework.throttling.UserRateThrottle",
#         ],
#         "DEFAULT_THROTTLE_RATES": {"anon": "100/day", "user": "1000/day"},
#     },
# )
