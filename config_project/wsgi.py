# wsgi.py
"""WSGI application entry point for the project.

Provides the interface for web servers to communicate with the Django application.
Configures the WSGI application for deployment in a production environment.
In production, this file is used to interface with web servers like Gunicorn or uWSGI.
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the default settings module to 'prod_config' for the production environment.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config_project.settings.prod_config")

# Create and expose the WSGI application callable for the web server to use.
application = get_wsgi_application()
