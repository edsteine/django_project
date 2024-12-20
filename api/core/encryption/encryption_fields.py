"""api/core/encryption/encryption_fields.py
Custom encrypted fields.

Implements encryption on model fields by using the Fernet encryption
scheme to securely store and retrieve encrypted values.
"""

from typing import Any

from api.core.encryption.encryption_config import ENCRYPTION_KEY
from cryptography.fernet import Fernet
from django.db import models
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models import Model


class EncryptedCharField(models.CharField[str, str]):
    """Custom Django model field that encrypts and decrypts data using the Fernet encryption scheme.

    This field can be used to securely store sensitive data in the database.
    It encrypts data when saving to the database and decrypts it when retrieving.

    Attributes:
        key (Fernet): The Fernet encryption key used to encrypt and decrypt data.

    """

    key: Fernet

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """
        Initializes the EncryptedCharField with the given arguments and
        sets up the Fernet encryption key.

        Args:
            *args: Additional arguments passed to the parent class.
            **kwargs: Additional keyword arguments passed to the parent class.
        """
        super().__init__(*args, **kwargs)
        self.key = Fernet(ENCRYPTION_KEY)

    def get_prep_value(self, value: str | None) -> str | None:
        """Prepares the value for storage by encrypting it.

        Args:
            value (Optional[str]): The value to be encrypted.

        Returns:
            Optional[str]: The encrypted value as a string, or None if no value.

        """
        if value is None:
            return None
        return self.key.encrypt(value.encode()).decode()

    def from_db_value(self, value: str | None, expression: Model, connection: BaseDatabaseWrapper) -> str | None:
        """Decrypts the stored value when retrieving it from the database.

        Args:
            value (Optional[str]): The encrypted value from the database.
            expression: The SQL expression used to fetch the value.
            connection: The database connection.

        Returns:
            Optional[str]: The decrypted value, or None if no value.

        """
        if value is None:
            return None

        # Suppress unused argument warnings explicitly
        _ = expression
        _ = connection

        return self.key.decrypt(value.encode()).decode()
