"""Django's command-line utility for administrative tasks.

Primary interface for running the development server, applying migrations,
and running other Django commands. This file is created automatically when
you run `django-admin startproject`. It contains the project's command-line
interface (CLI) logic for managing and interacting with the project.
"""

import os
import sys

# from environ import Env
from environ import Env  # type: ignore[import-untyped]

# Constants for environment types
ENV_DEV = "dev"


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
    # TODO(Adel/2024-12-22): Don't forget about using config.
    # 003
    # # Specify custom .env location
    # config = Config(RepositoryEnv('.env'))
    # DEBUG = config('DEBUG', default=False, cast=bool)

    # Initialize the Env object to load and parse environment variables
    env_variables = Env()
    # Determine the environment (development or production)
    environment: str = env_variables("DJANGO_ENVIRONMENT") or ENV_DEV

    # Load environment variables based on the environment
    if environment == ENV_DEV:
        env_variables.read_env(overwrite=True)  # Load .env file for development environment

    settings_module: str = env_variables.str("DJANGO_SETTINGS_MODULE") or "config_project.settings.dev_config"
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
