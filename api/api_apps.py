# api/api_apps.py
"""Django API application configuration.

Registers API as a Django app.
Contains API app-specific configurations.
Defines app settings and startup logic.
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Configuration class for the 'api' application.

    Registers the API app, sets its verbose name, and includes any
    application-specific startup logic.
    """

    name: str = "api"
    verbose_name: str = "API"

    def ready(self) -> None:
        """Perform app-specific initialization when the app is ready.

        This method can be overridden to add any application-specific
        startup logic, such as signal registrations or third-party
        integrations.
        """
        # pass
