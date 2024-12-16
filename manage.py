"""Django's command-line utility for administrative tasks.

Primary interface for running the development server, applying migrations,
and running other Django commands. This file is created automatically when
you run `django-admin startproject`. It contains the project's command-line
interface (CLI) logic for managing and interacting with the project.
"""

import os
import sys


def main() -> None:
    """Set up and run Django management commands.

    Sets the default settings module to the development configuration and
    handles the execution of Django management commands. Configures the
    environment and runs the appropriate command line operation.

    This function serves as the entry point for running commands like
    'runserver', 'migrate', etc.

    Raises:
        ImportError: If Django is not properly installed or accessible.
        ImproperlyConfigured: If Django settings are not properly configured.

    """
    settings_module = os.environ.get("DJANGO_SETTINGS_MODULE", "config_project.settings.dev_config")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?",
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
