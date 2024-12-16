import uuid

from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Email is required"))

        try:
            validate_email(email)
        except ValidationError as err:
            raise ValueError(_("Invalid email address")) from err

        email = self.normalize_email(email)

        # Generate a unique username if not provided
        if "username" not in extra_fields or not extra_fields["username"]:
            extra_fields["username"] = self._generate_unique_username(email)

        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def _generate_unique_username(self, email):
        """Generate a unique username based on email or UUID"""
        base_username = email.split("@")[0]
        username = base_username

        # Append a unique identifier if username already exists
        counter = 1
        while self.model.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        # Fallback to UUID if username conflict persists
        if self.model.objects.filter(username=username).exists():
            username = f"{base_username}_{uuid.uuid4().hex[:8]}"

        return username

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **extra_fields)
