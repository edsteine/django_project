"""
File: config_project/wsgi.py
Date updated: 2024-12-23
Author: Adil AJDAA
Email: a.ajdaa@outlook.com
Project: Ed Project
Description: WSGI application entry point for the project.

Provides the interface for web servers to communicate with the Django application.
Configures the WSGI application for deployment in a production environment.
In production, this file is used to interface with web servers like Gunicorn or uWSGI.
Used Libraries: os, django
"""

import os

from django.core.wsgi import get_wsgi_application
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
# Set the default settings module to 'prod_config' for the production environment.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

# Create and expose the WSGI application callable for the web server to use.
application = get_wsgi_application()
