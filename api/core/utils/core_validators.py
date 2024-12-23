"""
File: api/core/utils/core_validators.py
Date updated: 2024-12-21
Author: Adil AJDAA
Email: a.ajdaa@outlook.com
Project: Ed Project
Description: Implements general validation logic for commonly used validation patterns such as email and phone numbers.
These validators ensure data integrity across the application by validating user inputs and other relevant data formats.
Used Libraries: re, phonenumbers, django.core.exceptions.ValidationError
"""

import re

import phonenumbers

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_email(email: str) -> bool:
    """Validates email format."""
    email_regex: str = r"(^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$)"
    return re.match(email_regex, email) is not None


def validate_phone(phone: str) -> None:
    """Validate phone number format."""
    try:
        phone_number = phonenumbers.parse(phone)
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError(_("Invalid phone number format"))
    except phonenumbers.phonenumberutil.NumberParseException as err:
        raise ValidationError(_("Invalid phone number format")) from err


# TODO(Adel/2024-12-22): Implement validation logic in models for email and phone fields using core_validators.
# Ensure that model fields leverage the validators for data integrity.
# Test the integration of validation logic within models, not directly in this file.
# 002
# Example:
# from django.db import models
# from api.core.utils.core_validators import validate_email, validate_phone
# class User(models.Model):
#     email = models.CharField(max_length=100, validators=[validate_email])
#     phone = models.CharField(max_length=20, validators=[validate_phone])
