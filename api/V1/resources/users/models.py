from api.V1.resources.users.user_managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    """Extended User model with comprehensive profile details"""

    objects = CustomUserManager()
    # Basic Information

    first_name = models.CharField(_("first name"), max_length=100, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=100, null=True, blank=True)
    maiden_name = models.CharField(_("maiden name"), max_length=100, null=True, blank=True)
    gender = models.CharField(_("gender"), max_length=50, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(_("phone number"), max_length=20, null=True, blank=True)
    username = models.CharField(
        _("username"),
        max_length=100,
        unique=True,
        null=True,  # Allow null during migration
        blank=True,
    )

    birth_date = models.DateField(_("birth date"), null=True, blank=True)
    image = models.ImageField(_("profile image"), upload_to="profile_images/%Y/%m/", null=True, blank=True)

    role = models.CharField(_("user role"), max_length=100, default="user")

    # Django-specific fields
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the user is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on each save

    # Specify the fields used for authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def age(self):
        """Computed property for calculating the age of the user"""
        if self.birth_date:
            today = timezone.now().date()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

    @property
    def status(self):
        """Status could be based on active status"""
        return "Active" if self.is_active else "Inactive"

    @property
    def is_verified(self):
        """Verification logic can be customized, for example, based on email verification"""
        return self.is_active  # Assuming a user is verified when they are active, adjust as needed

    def __str__(self):
        return self.email or self.username
