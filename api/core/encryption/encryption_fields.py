"""
File: api/core/encryption/encryption_fields.py
Date updated: 2024-12-21
Author: Adil AJDAA
Email: a.ajdaa@outlook.com
Project: Ed Project
Description: Custom encrypted fields using the Fernet encryption scheme for secure data storage.
Used Libraries: cryptography.fernet, django.db
"""

import logging

from api.core.encryption.encryption_config import ENCRYPTION_KEY
from api.core.utils.core_constants import ENCRYPTION_KEY_LENGTH
from cryptography.fernet import Fernet, InvalidToken
from django.db import models
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Model

# Set up logging
logger = logging.getLogger(__name__)


class EncryptedCharField(models.CharField):  # type: ignore
    # class EncryptedCharField(models.CharField[str, str]):
    """Django model field that encrypts and decrypts data using Fernet encryption."""

    key: Fernet

    # def __init__(self, *args: Any, **kwargs: Any) -> None:

    def __init__(self, *args: tuple, **kwargs: dict) -> None:  # type: ignore
        super().__init__(*args, **kwargs)  # type: ignore

        # Validate encryption key length
        if len(ENCRYPTION_KEY) != ENCRYPTION_KEY_LENGTH:
            raise ValueError("Invalid ENCRYPTION_KEY length.")

        try:
            self.key = Fernet(ENCRYPTION_KEY)
        except ValueError as e:
            logger.error("Invalid ENCRYPTION_KEY: %s", e)
            raise

    def get_prep_value(self, value: str | None) -> str | None:
        """Encrypts the value before storing it in the database."""
        if value is None:
            return None

        try:
            return self.key.encrypt(value.encode()).decode()
        except Exception as e:
            logger.error("Encryption failed: %s", e)
            raise ValueError("Encryption failed.") from e

    def from_db_value(self, value: str | None, expression: Model, connection: BaseDatabaseWrapper) -> str | None:
        """Decrypts the value when retrieving it from the database."""
        if value is None:
            return None

        _ = expression  # Suppress unused argument warning
        _ = connection  # Suppress unused argument warning

        try:
            return self.key.decrypt(value.encode()).decode()
        except InvalidToken as e:
            logger.error("Decryption failed: Invalid token. %s", e)
            raise ValueError("Decryption failed. Invalid token.") from e
        except Exception as e:
            logger.error("Decryption failed: %s", e)
            raise ValueError("Decryption failed.") from e


# TODO(Adel/2024-12-22): Implement in models  and test the usage of EncryptedCharField for sensitive data storage.
# Ensure integration with Django's ORM and proper configuration.
# 002
# Example
# from django.db import models
# from api.core.encryption.encryption_fields import EncryptedCharField
# class User(models.Model):
#     username = models.CharField(max_length=100)
#     api_key = EncryptedCharField(max_length=255)
