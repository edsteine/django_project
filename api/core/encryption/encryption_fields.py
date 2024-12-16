"""api/core/encryption/encryption_fields.py
Custom encrypted fields.

Implements encryption on model fields by using the Fernet encryption
scheme to securely store and retrieve encrypted values.
"""

from api.core.encryption.encryption_config import ENCRYPTION_KEY
from cryptography.fernet import Fernet
from django.db import models


class EncryptedCharField(models.CharField):
    """Custom Django model field that encrypts and decrypts data using the
    Fernet encryption scheme.

    This field can be used to securely store sensitive data in the database.
    It encrypts data when saving to the database and decrypts it when retrieving.

    Attributes:
        key (Fernet): The Fernet encryption key used to encrypt and decrypt data.

    """

    def __init__(self, *args, **kwargs):
        """Initializes the EncryptedCharField with the given arguments and
        sets up the Fernet encryption key.

        Args:
            *args: Additional arguments passed to the parent class.
            **kwargs: Additional keyword arguments passed to the parent class.

        """
        self.key = Fernet(ENCRYPTION_KEY)
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        """Prepares the value for storage by encrypting it.

        Args:
            value (str): The value to be encrypted.

        Returns:
            str: The encrypted value as a string.

        """
        return self.key.encrypt(value.encode()).decode()

    def from_db_value(self, value, expression, connection):
        """Decrypts the stored value when retrieving it from the database.

        Args:
            value (str): The encrypted value from the database.
            expression: The SQL expression used to fetch the value.
            connection: The database connection.

        Returns:
            str: The decrypted value.

        """
        # Suppress unused argument warnings by explicitly ignoring them
        del expression  # Unused argument
        del connection  # Unused argument

        return self.key.decrypt(value.encode()).decode()
