# api/V1/resources/users/apps.py
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration class for the Users app.

    This class configures the app's name and label, as well as the
    default auto field for models.
    """

    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "api.V1.resources.users"
    label: str = "users"
