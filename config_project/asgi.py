"""
File: config_project/asgi.py
Date updated: 2024-12-23
Author: Adil AJDAA
Email: a.ajdaa@outlook.com
Project: Ed Project
Description: ASGI application entry point for the project.

This file provides the interface for asynchronous web servers (e.g., Daphne, Uvicorn)
to communicate with the Django application. It configures the ASGI application
for production, using the production configuration settings.
Used Libraries: os, django, environ
"""

import os

from django.core.asgi import get_asgi_application
from environ import Env  # type: ignore[import-untyped]

# Constants for environment types
ENV_DEV = "dev"

# Initialize the Env object to load and parse environment variables
env_variables = Env()

# Determine the environment (development or production)
# environment: str = env_variables("DJANGO_ENVIRONMENT") or ENV_DEV
environment: str = env_variables.str("DJANGO_ENVIRONMENT", default=ENV_DEV)

# Load environment variables based on the environment
if environment == ENV_DEV:
    env_variables.read_env(overwrite=True)  # Load .env file for development environment

DJANGO_SETTINGS_MODULE = env_variables.bool("DJANGO_SETTINGS_MODULE")
# Set the default Django settings module to production configuration
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

# Initialize the ASGI application only if the environment is production
if os.getenv("DJANGO_ENV", "production").lower() == "production":
    application = get_asgi_application()
else:
    raise OSError("ASGI application can only be initialized in the production environment.")
