# api/core/encryption/encryption_handlers.py
"""Encryption handling logic.

Manages encryption operations for data, including encrypting and decrypting
data using the defined encryption scheme.
"""

from api.core.encryption.encryption_config import ENCRYPTION_KEY
from cryptography.fernet import Fernet


def encrypt_data(data: str) -> str:
    """Encrypts the provided data using the defined encryption scheme.

    Args:
        data (str): The plain text data to be encrypted.

    Returns:
        str: The encrypted data as a string.

    """
    fernet: Fernet = Fernet(ENCRYPTION_KEY)
    return fernet.encrypt(data.encode()).decode()


def decrypt_data(data: str) -> str:
    """Decrypts the provided data using the defined encryption scheme.

    Args:
        data (str): The encrypted data to be decrypted.

    Returns:
        str: The decrypted plain text data.

    """
    fernet: Fernet = Fernet(ENCRYPTION_KEY)
    return fernet.decrypt(data.encode()).decode()
