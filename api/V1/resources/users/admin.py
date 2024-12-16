from api.V1.resources.users.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
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
    # Remove 'status' and 'is_verified' from list_filter since they are properties
    list_filter = ("is_active", "is_staff", "role")  # Only filter by actual fields
    search_fields = ("first_name", "last_name", "email", "username", "phone")
    ordering = ("-id",)  # Default ordering by ID in descending order
    fieldsets = (
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
    add_fieldsets = (
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
