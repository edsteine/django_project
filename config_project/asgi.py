# asgi.py
"""ASGI application entry point for the project.

Provides the interface for asynchronous web servers (e.g., Daphne, Uvicorn)
to communicate with the Django application.
Configures the ASGI application for production, using the prod_config settings.
In production,
this file interfaces with ASGI servers to handle asynchronous protocols like WebSockets.
"""

import os

from django.core.asgi import get_asgi_application

# Set the default settings module to 'prod_config' for the production environment.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config_project.settings.prod_config")

# Create and expose the ASGI application callable for asynchronous web servers to use.
application = get_asgi_application()
