# api/core/encryption/encryption_handlers.py
"""Encryption handling logic.

Manages encryption operations for data, including encrypting and decrypting
data using the defined encryption scheme.
"""

from api.core.encryption.encryption_config import ENCRYPTION_KEY
from cryptography.fernet import Fernet


def encrypt_data(data):
    """Encrypts the provided data using the defined encryption scheme."""
    fernet = Fernet(ENCRYPTION_KEY)
    return fernet.encrypt(data.encode()).decode()


def decrypt_data(data):
    """Decrypts the provided data using the defined encryption scheme."""
    fernet = Fernet(ENCRYPTION_KEY)
    return fernet.decrypt(data.encode()).decode()
