from __future__ import annotations  # Add this for better type hinting

from typing import ClassVar, cast

from api.V1.resources.users.user_managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Change this import to avoid circular import


class User(AbstractBaseUser, PermissionsMixin):
    """Extended User model with comprehensive profile details.

    This model adds fields for personal information, roles, status, and age calculation.
    It also supports customized user authentication via email.
    """

    objects = CustomUserManager()

    # Basic Information
    # first_name: str | None = models.CharField(_("first name"), max_length=100, null=True, blank=True)
    first_name: str | None = cast(
        str | None,
        models.CharField(_("first name"), max_length=100, null=True, blank=True),
    )

    last_name = cast(
        str | None,
        models.CharField(_("last name"), max_length=100, null=True, blank=True),
    )
    maiden_name = cast(
        str | None,
        models.CharField(_("maiden name"), max_length=100, null=True, blank=True),
    )
    gender = cast(str | None, models.CharField(_("gender"), max_length=50, null=True, blank=True))
    email = cast(str, models.EmailField(_("email address"), unique=True))
    phone = cast(
        str | None,
        models.CharField(_("phone number"), max_length=20, null=True, blank=True),
    )

    username: str | None = cast(
        str | None,
        models.CharField(_("username"), max_length=100, unique=True, null=True, blank=True),
    )

    birth_date = models.DateField(_("birth date"), null=True, blank=True)

    image: models.ImageField | None = cast(
        models.ImageField | None,
        models.ImageField(_("profile image"), upload_to="profile_images/%Y/%m/", null=True, blank=True),
    )

    role: str = cast(str, models.CharField(_("user role"), max_length=100, default="user"))

    is_staff: bool = cast(bool, models.BooleanField(default=False))
    is_active: bool = cast(bool, models.BooleanField(default=True))
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = ["username"]

    @property
    def age(self) -> int | None:
        """Computed property for calculating the age of the user.

        Returns:
            Optional[int]: The age of the user, or None if birth_date is not set.
        """
        if self.birth_date:
            today = timezone.now().date()
            # pylint: disable=no-member
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

    @property
    def status(self) -> str:
        """Status based on active status.

        Returns:
            str: "Active" if the user is active, otherwise "Inactive".
        """
        return "Active" if self.is_active else "Inactive"

    @property
    def is_verified(self) -> bool:
        """Verification status, assumed true if active.

        Returns:
            bool: True if the user is active, indicating verified status.
        """
        return self.is_active  # Assuming a user is verified when they are active, adjust as needed

    def __str__(self) -> str:
        """String representation of the User object.

        Returns:
            str: The email or username of the user.
        """
        return self.email or self.username or ""
