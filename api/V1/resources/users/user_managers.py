from __future__ import annotations

import uuid

from typing import TYPE_CHECKING, Any, TypedDict, TypeVar, cast

import django

from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

# Avoid circular import
if TYPE_CHECKING:
    pass


class ExtraFields(TypedDict, total=False):
    """Type definition for extra user fields."""

    is_staff: bool | None
    is_superuser: bool | None
    is_active: bool | None
    username: str | None


T = TypeVar("T", bound=django.db.models.Model)


class CustomUserManager(BaseUserManager[T]):
    """Custom user model manager using email as the unique identifier."""

    def get_by_natural_key(self, username: str | None = None) -> T:
        """
        Retrieve a user by their natural key (email).

        Args:
            username (str | None, optional): The email address of the user.

        Returns:
            UserProtocol: The user with the matching email.

        Raises:
            ValueError: If no username is provided.
        """
        if username is None:
            raise ValueError(_("Username/Email is required"))

        return self.get(email=username)

    def _create_user(self, email: str, password: str | None = None, **extra_fields: bool | str | None) -> T:
        """
        Create and save a user with the given email and password.

        Args:
            email (str): The email address for the user.
            password (Optional[str], optional): The user's password. Defaults to None.
            **extra_fields (ExtraFields): Additional user fields.

        Raises:
            ValueError: If email is invalid or not provided.

        Returns:
            UserProtocol: The created user instance.
        """
        if not email:
            raise ValueError(_("Email is required"))

        try:
            validate_email(email)
        except ValidationError as err:
            raise ValueError(_("Invalid email address")) from err

        email = self.normalize_email(email)

        # Prepare extra fields with proper typing
        processed_extra_fields: ExtraFields = {}
        if "username" not in extra_fields or not extra_fields.get("username"):
            processed_extra_fields["username"] = self._generate_unique_username(email)

        # Transfer other fields
        for key, value in extra_fields.items():
            if key in ["is_staff", "is_superuser", "is_active", "username"]:
                processed_extra_fields[key] = value  # type: ignore

        user_model = get_user_model()
        user = user_model(email=email, **processed_extra_fields)

        if password:
            user.set_password(password)
        user.save(using=self._db)

        return cast(T, user)  # Explicitly cast to the expected return type

    def _generate_unique_username(self, email: str) -> str:
        """
        Generate a unique username based on the email.

        Args:
            email (str): The email address to derive the username from.

        Returns:
            str: A unique username.
        """
        user_model = get_user_model()
        base_username = email.split("@")[0]
        username = base_username

        # Ensure username uniqueness
        counter = 1
        while user_model.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        # Fallback to UUID if still not unique
        if user_model.objects.filter(username=username).exists():
            username = f"{base_username}_{uuid.uuid4().hex[:8]}"

        return username

    def create_user(self, email: str, password: str | None = None, **extra_fields: bool | str | None) -> T:
        """
        Create a standard user.

        Args:
            email (str): User's email address.
            password (Optional[str], optional): User's password. Defaults to None.
            **extra_fields (ExtraFields): Additional user fields.

        Returns:
            The created user instance.
        """
        processed_extra_fields: dict[str, Any] = dict(extra_fields)
        processed_extra_fields.setdefault("is_staff", False)
        processed_extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **processed_extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields: bool | str | None) -> T:
        """
        Create a superuser with admin privileges.

        Args:
            email (str): Superuser's email address.
            password (Optional[str], optional): Superuser's password. Defaults to None.
            **extra_fields (ExtraFields): Additional user fields.

        Raises:
            ValueError: If superuser flags are not set correctly.

        Returns:
            user: The created superuser instance.
        """
        processed_extra_fields: dict[str, Any] = dict(extra_fields)
        processed_extra_fields.setdefault("is_staff", True)
        processed_extra_fields.setdefault("is_superuser", True)
        processed_extra_fields.setdefault("is_active", True)

        if processed_extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if processed_extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **processed_extra_fields)
