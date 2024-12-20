from typing import Any

from api.V1.resources.users.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):  # type: ignore
    """Custom admin class for the User model.

    Provides customized list display, filters, search fields,
    ordering, and fieldsets for the User admin interface.
    """

    model = User  # Type hint the model attribute
    list_display: tuple[str, ...] = (
        "id",
        "first_name",
        "last_name",
        "maiden_name",
        "gender",
        "email",
        "username",
        "phone",
        "birth_date",
        "image",
        "status",
        "role",
        "last_login",
        "is_verified",
        "created_at",
        "updated_at",
    )
    list_filter: tuple[str, ...] = ("is_active", "is_staff", "role")
    search_fields: tuple[str, ...] = (
        "first_name",
        "last_name",
        "email",
        "username",
        "phone",
    )
    ordering: tuple[str, ...] = ("-id",)
    fieldsets: tuple[Any, ...] = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "maiden_name",
                    "gender",
                    "email",
                    "phone",
                    "username",
                    "password",
                ),
            },
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "role")}),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
        ("Additional Info", {"fields": ("birth_date", "image")}),
    )
    add_fieldsets: tuple = (  # type: ignore
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


# Register the model with the customized admin interface
admin.site.register(User, CustomUserAdmin)
