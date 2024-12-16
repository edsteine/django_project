import re

from typing import Any

import phonenumbers

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

MIN_PASSWORD_LENGTH = 8


class UserDataValidator:
    @staticmethod
    def validate_password(password: str) -> None:
        """Validate password strength"""
        if len(password) < MIN_PASSWORD_LENGTH:
            raise ValidationError(_("Password must be at least {min_length} characters long").format(min_length=MIN_PASSWORD_LENGTH))

        if not re.search(r"[A-Z]", password):
            raise ValidationError(_("Password must contain at least one uppercase letter"))

        if not re.search(r"[a-z]", password):
            raise ValidationError(_("Password must contain at least one lowercase letter"))

        if not re.search(r"\d", password):
            raise ValidationError(_("Password must contain at least one number"))

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(_("Password must contain at least one special character"))

    @staticmethod
    def validate_phone(phone: str) -> None:
        """Validate phone number format"""
        try:
            phone_number = phonenumbers.parse(phone)
            if not phonenumbers.is_valid_number(phone_number):
                raise ValidationError(_("Invalid phone number format"))
        except phonenumbers.phonenumberutil.NumberParseException as err:
            raise ValidationError(_("Invalid phone number format")) from err

    @classmethod
    def validate_user_data(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Validate all user data"""
        if "password" in data:
            cls.validate_password(data["password"])

        if data.get("phone"):
            cls.validate_phone(data["phone"])

        # You can add more validation logic here for other fields (e.g., email, etc.)

        return data
