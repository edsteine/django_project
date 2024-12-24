# # import logging
# # import os
# # import sys

# # from datetime import timedelta
# # from pathlib import Path

# # # Function to get the logging configuration
# # from typing import Any

# # # import environ
# # import structlog


# # # from environ import Env
# # from environ import Env  # type: ignore[import-untyped]

# # # Initialize environment variables using environ

# # env_variables = Env()

# # # Load environment variables from a `.env` file. Ensure `.env` exists in the project root.
# # # Env.read_env(".env")
# # Env.read_env()

# # logger = logging.getLogger(__name__)

# # # Base directory for project structure
# # BASE_DIR = Path(__file__).resolve().parent.parent.parent
# # LOGS_DIR = BASE_DIR / "logs"  # Directory for log files
# # os.makedirs(LOGS_DIR, exist_ok=True)  # Create logs directory if it doesn't exist

# # # Required environment variables for security and database configuration
# # required_env_vars: list[str] = [
# #     "DJANGO_SECRET_KEY",
# #     "DB_NAME",
# #     "DB_USER",
# #     "DB_PASSWORD",
# #     "DB_HOST",
# #     "DJANGO_DEBUG",
# #     "DJANGO_ALLOWED_HOSTS",
# #     "DB_ENGINE",
# #     "DB_PORT",
# #     "CACHE_BACKEND",
# #     "EMAIL_BACKEND",
# #     "TIME_ZONE",
# #     "EMAIL_HOST",
# #     "EMAIL_PORT",
# #     "EMAIL_USE_TLS",
# #     "EMAIL_HOST_USER",
# #     "EMAIL_HOST_PASSWORD",
# #     # "CORS_ALLOWED_ORIGINS",
# # ]

# # # Check for missing environment variables
# # missing_vars: list[str] = []
# # for var_name in required_env_vars:
# #     var_value = env_variables(var_name, default=None)
# #     if var_value is None or not var_value.strip():
# #         missing_vars.append(var_name)

# # # If any required environment variables are missing, print and exit
# # if missing_vars:
# #     error_message = "The following environment variables are missing or empty:\n"
# #     error_message += ", ".join(missing_vars)
# #     logger.error(error_message)
# #     sys.exit(1)

# # # Common Django settings
# # SECRET_KEY = env_variables("DJANGO_SECRET_KEY")
# # DEBUG = env_variables("DJANGO_DEBUG")
# # ALLOWED_HOSTS = env_variables.list("DJANGO_ALLOWED_HOSTS")
# # DB_ENGINE = env_variables("DB_ENGINE")
# # DB_NAME = env_variables("DB_NAME")
# # DB_USER = env_variables("DB_USER")
# # DB_PASSWORD = env_variables("DB_PASSWORD")
# # DB_HOST = env_variables("DB_HOST")
# # DB_PORT = env_variables("DB_PORT")
# # CACHE_BACKEND = env_variables("CACHE_BACKEND")
# # EMAIL_BACKEND = env_variables("EMAIL_BACKEND")
# # DJANGO_ALLOWED_HOSTS = env_variables("DJANGO_ALLOWED_HOSTS")
# # EMAIL_HOST = env_variables("EMAIL_HOST")
# # EMAIL_PORT = env_variables("EMAIL_PORT")
# # EMAIL_USE_TLS = env_variables("EMAIL_USE_TLS")
# # EMAIL_HOST_USER = env_variables("EMAIL_HOST_USER")
# # EMAIL_HOST_PASSWORD = env_variables("EMAIL_HOST_PASSWORD")
# # # CORS_ALLOWED_ORIGINS = env_variables.list("CORS_ALLOWED_ORIGINS")

# # # Installed applications for the project
# # INSTALLED_APPS = [
# #     "django.contrib.admin",
# #     "django.contrib.auth",
# #     "django.contrib.contenttypes",
# #     "django.contrib.sessions",
# #     "django.contrib.messages",
# #     "django.contrib.staticfiles",
# #     "rest_framework",
# #     "rest_framework_simplejwt",
# #     "corsheaders",
# #     "api.V1.resources.users",
# # ]

# # # Custom user model for the project
# # AUTH_USER_MODEL = "users.User"
# # ROOT_URLCONF = "config_project.project_urls"  # Adjust to match your project's URL configuration path

# # # Middleware configuration
# # MIDDLEWARE = [
# #     "django.middleware.security.SecurityMiddleware",
# #     "corsheaders.middleware.CorsMiddleware",
# #     "django.contrib.sessions.middleware.SessionMiddleware",
# #     "django.middleware.common.CommonMiddleware",
# #     "django.middleware.csrf.CsrfViewMiddleware",
# #     "django.contrib.auth.middleware.AuthenticationMiddleware",
# #     "django.contrib.messages.middleware.MessageMiddleware",
# #     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# # ]

# # # REST Framework settings
# # REST_FRAMEWORK = {
# #     "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
# #     "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
# #     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
# #     "PAGE_SIZE": 10,
# # }

# # # JWT settings
# # SIMPLE_JWT = {
# #     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
# #     "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
# #     "ROTATE_REFRESH_TOKENS": True,
# #     "BLACKLIST_AFTER_ROTATION": True,
# #     "AUTH_HEADER_TYPES": ("Bearer",),
# #     "USER_ID_FIELD": "id",
# #     "USER_ID_CLAIM": "user_id",
# # }

# # # Static file settings
# # STATIC_URL = "static/"
# # STATIC_ROOT = BASE_DIR / "staticfiles"
# # STATICFILES_DIRS = [
# #     BASE_DIR / "assets",  # Example additional directory
# # ]

# # # Internationalization settings
# # LANGUAGE_CODE = "en-us"
# # USE_I18N = True
# # USE_TZ = True
# # TIME_ZONE = env_variables("TIME_ZONE")  # Adjust default if needed

# # TEMPLATES = [
# #     {
# #         "BACKEND": "django.template.backends.django.DjangoTemplates",
# #         "DIRS": [],
# #         "APP_DIRS": True,
# #         "OPTIONS": {
# #             "context_processors": [
# #                 "django.template.context_processors.debug",
# #                 "django.template.context_processors.request",
# #                 "django.contrib.auth.context_processors.auth",
# #                 "django.contrib.messages.context_processors.messages",
# #             ],
# #         },
# #     },
# # ]

# # # Configure structlog to provide structured and human-readable logging
# # log_renderer = structlog.dev.ConsoleRenderer() if DEBUG else structlog.processors.JSONRenderer()

# # structlog.configure(
# #     processors=[
# #         structlog.contextvars.merge_contextvars,
# #         structlog.stdlib.add_logger_name,
# #         structlog.stdlib.add_log_level,
# #         structlog.processors.TimeStamper(fmt="iso"),
# #         structlog.processors.StackInfoRenderer(),
# #         structlog.processors.format_exc_info,
# #         log_renderer,  # Choose the renderer based on DEBUG
# #     ],
# #     context_class=dict,
# #     logger_factory=structlog.stdlib.LoggerFactory(),
# #     wrapper_class=structlog.stdlib.BoundLogger,
# #     cache_logger_on_first_use=True,
# # )


# # # Update the type annotation to be more specific
# # def get_logging_config(log_level: str = "INFO") -> dict[str, Any]:
# #     """Logging configuration with correct type annotations."""
# #     log_renderer = structlog.dev.ConsoleRenderer() if DEBUG else structlog.processors.JSONRenderer()

# #     return {
# #         "version": 1,
# #         "disable_existing_loggers": False,
# #         "formatters": {
# #             "structlog": {
# #                 "()": structlog.stdlib.ProcessorFormatter,
# #                 "processor": log_renderer,  # Use appropriate renderer
# #                 "foreign_pre_chain": [
# #                     structlog.stdlib.add_logger_name,
# #                     structlog.stdlib.add_log_level,
# #                     structlog.processors.TimeStamper(fmt="iso"),
# #                 ],
# #             },
# #         },
# #         "handlers": {
# #             "console": {
# #                 "level": log_level,
# #                 "class": "logging.StreamHandler",
# #                 "formatter": "structlog",
# #             },
# #             "file": {
# #                 "level": log_level,
# #                 "class": "logging.handlers.RotatingFileHandler",
# #                 "filename": LOGS_DIR / "django.log",
# #                 "maxBytes": 10 * 1024 * 1024,  # 10MB
# #                 "backupCount": 5,
# #                 "formatter": "structlog",
# #             },
# #         },
# #         "loggers": {
# #             "django": {
# #                 "handlers": ["console", "file"],
# #                 "level": log_level,
# #                 "propagate": True,
# #             },
# #         },
# #     }


# # # Apply logging configuration
# # LOGGING = get_logging_config()  # Configure logging with default log level "INFO"

# # # Disable DEBUG and set sensible defaults
# # ALLOWED_HOSTS = env_variables.list("DJANGO_ALLOWED_HOSTS")
# # SENTRY_DSN = env_variables("SENTRY_DSN")

# # # Database configuration for production using environment variables
# # DATABASES = {
# #     "default": {
# #         "ENGINE": "django.db.backends.postgresql",
# #         "NAME": env_variables("PROD_DB_NAME", default="prod_db"),
# #         "USER": env_variables("PROD_DB_USER", default="prod_user"),
# #         "PASSWORD": env_variables("PROD_DB_PASSWORD", default="prod_password"),
# #         "HOST": env_variables("PROD_DB_HOST", default="localhost"),
# #         "PORT": env_variables("PROD_DB_PORT", default="5432"),
# #         # Optional: Connection pooling and performance tuning
# #         "CONN_MAX_AGE": 600,  # Connection persistent for 10 minutes
# #         "OPTIONS": {
# #             "sslmode": "require",  # Enforce SSL for database connection
# #         },
# #     },
# # }

# # # Security settings for production
# # SECURE_SSL_REDIRECT = True
# # SESSION_COOKIE_SECURE = True
# # CSRF_COOKIE_SECURE = True

# # # Enhanced security headers
# # SECURE_HSTS_SECONDS = 31536000  # 1 year HSTS
# # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# # SECURE_HSTS_PRELOAD = True

# # # Additional security settings
# # SECURE_BROWSER_XSS_FILTER = True
# # SECURE_CONTENT_TYPE_NOSNIFF = True
# # X_FRAME_OPTIONS = "DENY"

# # # Performance and proxy settings
# # USE_X_FORWARDED_HOST = True
# # SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# # # CORS configuration
# # # CORS_ALLOWED_ORIGINS = env_variables.list("CORS_ALLOWED_ORIGINS", default=[])

# # # Reduce JWT access token lifetime for security
# # SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(minutes=15)

# # # Logging setup for production (use ERROR level for fewer log entries)
# # LOGGING = get_logging_config(log_level="ERROR")

# # # Email configuration
# # EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# # EMAIL_HOST = env_variables("PROD_EMAIL_HOST", default="smtp.example.com")
# # EMAIL_PORT = env_variables("PROD_EMAIL_PORT", default="587")
# # EMAIL_HOST_USER = env_variables("PROD_EMAIL_HOST_USER", default="user@example.com")
# # EMAIL_HOST_PASSWORD = env_variables("PROD_EMAIL_HOST_PASSWORD")
# # EMAIL_USE_TLS = True

# # # Caching configuration
# # CACHES = {
# #     "default": {
# #         "BACKEND": "django.core.cache.backends.redis.RedisCache",
# #         "LOCATION": env_variables("REDIS_CACHE_URL", default="redis://localhost:6379/1"),
# #         "OPTIONS": {
# #             "MAX_ENTRIES": 10000,
# #         },
# #     },
# # }

# # # Static and media file settings
# # AWS_STORAGE_BUCKET_NAME = env_variables("AWS_STORAGE_BUCKET_NAME")
# # AWS_S3_REGION_NAME = env_variables("AWS_S3_REGION_NAME")
# # AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# # # Static files
# # STATIC_LOCATION = "static"
# # STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
# # STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# # # Media files
# # PUBLIC_MEDIA_LOCATION = "media"
# # MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
# # DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# # # Installed apps for production
# # INSTALLED_APPS += [
# #     "storages",  # For S3 file storage
# # ]

# # # Rate limiting and protection
# # REST_FRAMEWORK.update(
# #     {
# #         "DEFAULT_THROTTLE_CLASSES": [
# #             "rest_framework.throttling.AnonRateThrottle",
# #             "rest_framework.throttling.UserRateThrottle",
# #         ],
# #         "DEFAULT_THROTTLE_RATES": {"anon": "100/day", "user": "1000/day"},
# #     },
# # )
# import logging
# import os
# import sys

# from collections.abc import Callable, MutableMapping
# from datetime import timedelta
# from pathlib import Path
# from typing import Any

# # import sentry_sdk
# import structlog

# from environ import Env  # type: ignore[import-untyped]

# # from sentry_sdk.integrations.django import DjangoIntegration

# # Constants for environment types
# ENV_DEV = "dev"
# # Initialize the Env object to load and parse environment variables
# env_variables = Env()
# # Determine the environment (development or production)
# ENVIRONMENT: str = env_variables.str("DJANGO_ENVIRONMENT") or ENV_DEV

# # Load environment variables based on the environment
# if ENVIRONMENT == ENV_DEV:
#     env_variables.read_env(overwrite=True)  # Load .env file for development environment

# # Base directory setup
# BASE_DIR = Path(__file__).resolve().parent.parent.parent
# LOGS_DIR = BASE_DIR / "logs"
# os.makedirs(LOGS_DIR, exist_ok=True)

# logger = logging.getLogger(__name__)

# # Required environment variables check
# required_env_vars: list[str] = [
#     "DJANGO_ENVIRONMENT",
#     "DJANGO_SETTINGS_MODULE",
#     "TIME_ZONE",
#     "DJANGO_SECRET_KEY",
#     "DJANGO_DEBUG",
#     "ALLOWED_HOSTS",
#     "INTERNAL_IPS",
#     "CORS_ALLOWED_ORIGINS",
#     "DB_ENGINE",
#     "DB_NAME",
#     "DB_USER",
#     "DB_PASSWORD",
#     "DB_HOST",
#     "DB_PORT",
#     "CACHE_BACKEND",
#     "REDIS_CACHE_URL",
#     "EMAIL_BACKEND",
#     "EMAIL_HOST",
#     "EMAIL_PORT",
#     "EMAIL_USE_TLS",
#     "EMAIL_HOST_USER",
#     "EMAIL_HOST_PASSWORD",
#     "SENTRY_DSN",
#     "LOGGING_LEVEL",
#     "LOGGING_BACKEND",
#     "SECURE_SSL_REDIRECT",
#     "SECURE_HSTS_SECONDS",
#     "SECURE_HSTS_INCLUDE_SUBDOMAINS",
#     "SECURE_HSTS_PRELOAD",
#     "CSRF_COOKIE_SECURE",
#     "SESSION_COOKIE_SECURE",
#     "FEATURE_X_ENABLED",
#     "CORS_ALLOW_ALL_ORIGINS",
#     "CORS_ALLOW_CREDENTIALS",
#     "USE_I18N",
#     "USE_TZ",
#     "ROTATE_REFRESH_TOKENS",
#     "BLACKLIST_AFTER_ROTATION",
#     "ENCRYPTION_KEY",
#     "ENCRYPTION_ALGORITHM",
#     # "TESTING",
#     # "ML_SERVICE_URL",
#     # "GRAPHQL_ENDPOINT",
#     # "AI_CHAT_SERVICE_URL",
#     # "AI_CHAT_API_KEY",
#     # "AI_CHAT_MODEL",
#     # "CLAUDE_API_URL",
#     # "CLAUDE_API_KEY",
#     # "DATABASE_POOL_SIZE",
#     # "DATABASE_MAX_CONNS",
#     # "DEFAULT_FILE_STORAGE",
#     # "AWS_ACCESS_KEY_ID",
#     # "AWS_SECRET_ACCESS_KEY",
#     # "AWS_S3_CUSTOM_DOMAIN",
#     # "DJANGO_DEV_TOOLBAR",
#     # "AWS_STORAGE_BUCKET_NAME",
#     # "AWS_S3_REGION_NAME",
#     # "GITHUB_API_KEY",
#     # "SENDGRID_API_KEY",
# ]

# missing_vars: list[str] = []
# for var_name in required_env_vars:
#     var_value = env_variables(var_name)
#     if var_value is None or not var_value.strip():
#         missing_vars.append(var_name)

# if missing_vars:
#     error_message = "The following environment variables are missing or empty:\n"
#     error_message += ", ".join(missing_vars)
#     logger.error(error_message)
#     sys.exit(1)

# # Core Django Settings
# # DEBUG = env_variables.bool("DJANGO_DEBUG")
# DEBUG = True
# # LOGGING_LEVEL = env_variables.str("LOGGING_LEVEL")
# LOGGING_LEVEL = "INFO"
# if LOGGING_LEVEL not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
#     raise ValueError("Invalid LOGGING_LEVEL. Use DEBUG, INFO, WARNING, ERROR, or CRITICAL.")

# SECRET_KEY = env_variables.str("DJANGO_SECRET_KEY")

# ALLOWED_HOSTS = env_variables.list("ALLOWED_HOSTS")
# INTERNAL_IPS = env_variables.list("INTERNAL_IPS")
# # Application definition
# INSTALLED_APPS = [
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#     # Third party apps
#     "rest_framework",
#     "rest_framework_simplejwt",
#     "corsheaders",
#     "debug_toolbar",
#     "django_extensions",
#     "drf_yasg",
#     "silk",
#     # Local apps
#     "api",
#     "api.V1.resources.users",
# ]

# MIDDLEWARE = [
#     "debug_toolbar.middleware.DebugToolbarMiddleware",
#     "silk.middleware.SilkyMiddleware",
#     "django.middleware.security.SecurityMiddleware",
#     "corsheaders.middleware.CorsMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
#     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# ]

# ROOT_URLCONF = "config_project.project_urls"
# AUTH_USER_MODEL = "users.User"

# # Database with connection pooling
# # Database configuration
# DATABASES = {
#     "default": {
#         "ENGINE": env_variables.str("DB_ENGINE"),
#         "NAME": env_variables.str("DB_NAME"),
#         "USER": env_variables.str("DB_USER"),
#         "PASSWORD": env_variables.str("DB_PASSWORD"),
#         "HOST": env_variables.str("DB_HOST"),
#         "PORT": env_variables.str("DB_PORT"),
#         "CONN_MAX_AGE": 60,
#         "OPTIONS": {
#             "connect_timeout": 10,
#             # "MAX_CONNS": env_variables.int("DATABASE_MAX_CONNS"),
#             # "POOL_SIZE": env_variables.int("DATABASE_POOL_SIZE"),
#             # "CONN_MAX_AGE": 60,  # Optional, controls connection persistence
#         },
#         "SSL_REQUIRE": False,
#     }
# }

# # Cache settings
# CACHES = {
#     "default": {
#         "BACKEND": env_variables.str("CACHE_BACKEND"),
#         "LOCATION": env_variables.str("REDIS_CACHE_URL"),
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             "SOCKET_CONNECT_TIMEOUT": 5,
#             "SOCKET_TIMEOUT": 5,
#             "RETRY_ON_TIMEOUT": True,
#             "MAX_CONNECTIONS": 1000,
#             "CONNECTION_POOL_KWARGS": {"max_connections": 100},
#         },
#     }
# }
# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [os.path.join(BASE_DIR, "templates")],  # Adjust this path
#         # "DIRS": [],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.debug",
#                 "django.template.context_processors.request",
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#             # "loaders": [
#             #     "django.template.loaders.filesystem.Loader",
#             #     "django.template.loaders.app_directories.Loader",
#             # ],
#             "debug": DEBUG,
#         },
#     },
# ]

# # Internationalization
# LANGUAGE_CODE = env_variables.str("LANGUAGE_CODE")
# TIME_ZONE = env_variables.str("TIME_ZONE")
# USE_I18N = env_variables.bool("USE_I18N")
# USE_TZ = env_variables.bool("USE_TZ")

# # Static files
# STATIC_URL = "static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"
# STATICFILES_DIRS = [BASE_DIR / "assets"]

# # STATIC_URL = "/static/"
# # STATICFILES_DIRS = [BASE_DIR / "static"]
# # STATIC_ROOT = BASE_DIR / "staticfiles"


# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"

# # Development security settings

# SECURE_HSTS_SECONDS = env_variables.str("SECURE_HSTS_SECONDS")
# SECURE_HSTS_INCLUDE_SUBDOMAINS = env_variables.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS")
# SECURE_HSTS_PRELOAD = env_variables.bool("SECURE_HSTS_PRELOAD")
# SECURE_SSL_REDIRECT = env_variables.bool("SECURE_SSL_REDIRECT")
# SESSION_COOKIE_SECURE = env_variables.bool("SESSION_COOKIE_SECURE")
# CSRF_COOKIE_SECURE = env_variables.bool("CSRF_COOKIE_SECURE")
# CORS_ALLOW_ALL_ORIGINS = env_variables.bool("CORS_ALLOW_ALL_ORIGINS")
# CORS_ALLOW_CREDENTIALS = env_variables.bool("CORS_ALLOW_CREDENTIALS")
# CORS_ALLOWED_ORIGINS = env_variables.list("CORS_ALLOWED_ORIGINS")
# # REST Framework settings
# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
#     "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
#     "PAGE_SIZE": 10,
#     "DEFAULT_THROTTLE_RATES": {
#         "anon": "100/minute",
#         "user": "1000/minute",
#     },
#     "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
# }
# AUTHENTICATION_BACKENDS = [
#     "django.contrib.auth.backends.ModelBackend",
# ]
# # LOGIN_URL = "/accounts/login/"  # Correct setting for login redirect
# LOGIN_URL = "/admin/login/"
# LOGIN_REDIRECT_URL = "/"  # Optional: After login, redirect to home page


# # JWT settings
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
#     "ROTATE_REFRESH_TOKENS": env_variables.bool("ROTATE_REFRESH_TOKENS"),
#     "BLACKLIST_AFTER_ROTATION": env_variables.bool("BLACKLIST_AFTER_ROTATION"),
#     "AUTH_HEADER_TYPES": ("Bearer",),
#     "USER_ID_FIELD": "id",
#     "USER_ID_CLAIM": "user_id",
# }

# # Email settings
# EMAIL_BACKEND = env_variables.str("EMAIL_BACKEND")
# EMAIL_HOST = env_variables.str("EMAIL_HOST")
# EMAIL_PORT = env_variables.int("EMAIL_PORT")
# EMAIL_HOST_USER = env_variables.str("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = env_variables.str("EMAIL_HOST_PASSWORD")
# EMAIL_USE_TLS = env_variables.bool("EMAIL_USE_TLS")

# base_processors: list[Callable[[Any, str, MutableMapping[str, Any]], Any]] = [
#     structlog.contextvars.merge_contextvars,
#     structlog.processors.add_log_level,
#     structlog.stdlib.ProcessorFormatter.remove_processors_meta,
#     structlog.processors.TimeStamper(fmt="iso"),
# ]

# log_renderer = structlog.dev.ConsoleRenderer() if DEBUG else structlog.processors.JSONRenderer()

# processors = [*base_processors, log_renderer]

# if DEBUG:
#     processors.extend([structlog.dev.ConsoleRenderer(colors=True)])
# else:
#     processors.extend([structlog.processors.dict_tracebacks, structlog.processors.JSONRenderer()])

# structlog.configure(
#     processors=processors,
#     logger_factory=structlog.stdlib.LoggerFactory(),
#     cache_logger_on_first_use=True,
#     wrapper_class=structlog.stdlib.BoundLogger,
# )

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "structlog": {
#             "()": structlog.stdlib.ProcessorFormatter,
#             "processor": log_renderer,
#             "foreign_pre_chain": [
#                 structlog.stdlib.add_logger_name,
#                 structlog.stdlib.add_log_level,
#                 structlog.processors.TimeStamper(fmt="iso"),
#             ],
#         },
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "structlog",
#             "level": LOGGING_LEVEL,
#         },
#         "file": {
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": LOGS_DIR / f"django-{ENVIRONMENT}.log",
#             "maxBytes": 10_485_760,
#             "backupCount": 5,
#             "formatter": "structlog",
#             "level": LOGGING_LEVEL,
#         },
#         "mail_admins": {
#             "class": env_variables.str("LOGGING_BACKEND"),
#             "level": "ERROR",
#         },
#     },
#     "root": {
#         "handlers": ["console", "file"],
#         "level": LOGGING_LEVEL,
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["console", "file"],
#             "level": LOGGING_LEVEL,
#             "propagate": False,
#         },
#         "django.db": {
#             "level": "INFO",
#             "propagate": True,
#         },
#         "django.request": {
#             "handlers": ["console", "mail_admins"],
#             "level": "ERROR",
#             "propagate": False,
#         },
#         "django.db.backends": {
#             "handlers": ["console"],
#             "level": LOGGING_LEVEL,
#             "propagate": False,
#         },
#     },
# }
# # Debug Toolbar settings
# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK": lambda request: True,
#     "INTERCEPT_REDIRECTS": False,
#     "SHOW_TEMPLATE_CONTEXT": True,
#     "ENABLE_STACKTRACES": True,
# }

# # Django Extensions settings
# SHELL_PLUS = "ipython"
# SHELL_PLUS_PRINT_SQL = True
# SHELL_PLUS_IMPORTS = [
#     "from datetime import datetime, timedelta, date",
#     "from django.conf import settings",
#     "from django.core.cache import cache",
#     "from django.db.models import Q, F, Count, Sum, Max, Min, Avg",
# ]

# # Default primary key field type
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# ADMINS = [("Admin Name", "admin@example.com")]


# # Feature Flags

# FEATURE_X_ENABLED = env_variables.bool("FEATURE_X_ENABLED")

# # SWAGGER_SETTINGS = {
# #     "USE_SESSION_AUTH": True,
# #     # "SECURITY_DEFINITIONS": {
# #     #     "Bearer": {
# #     #         "type": "apiKey",
# #     #         "name": "Authorization",
# #     #         "in": "header",
# #     #     },
# #     # },
# #     # "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
# # }

# SWAGGER_SETTINGS = {
#     # "DOC_EXPANSION": "list",
#     # "APIS_SORTER": "alpha",
#     # "USE_SESSION_AUTH": True,
#     # "SECURITY_DEFINITIONS": {
#     #     "basic": {
#     #         "type": "basic",
#     #     },
#     # },
#     'USE_SESSION_AUTH': False,
#     'SECURITY_DEFINITIONS': {
#         'Bearer': {
#             'type': 'apiKey',
#             'name': 'Authorization',
#             'in': 'header',
#         }
#     }
# }
# # sentry_sdk.init(
# #     dsn=env_variables.str("SENTRY_DSN"),
# #     integrations=[DjangoIntegration()],
# #     traces_sample_rate=1.0,  # Adjust as needed for performance tracking
# # )
