# api/V1/resources/users/apps.py
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.V1.resources.users"
    label = "users"  # Explicitly set the label
