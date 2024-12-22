"""
File: api/core/encryption/encryption_handlers.py
Date updated: 2024-12-21
Author: Adil AJDAA
Email: a.ajdaa@outlook.com
Project: Ed Project
Description: Encryption handling logic.
    Manages encryption operations for data, including encrypting and decrypting
    data using the defined encryption scheme.
Used Libraries: cryptography.fernet
"""

from api.core.encryption.encryption_config import ENCRYPTION_KEY
from cryptography.fernet import Fernet


def encrypt_data(data: str) -> str:
    """Encrypts plain text data using Fernet."""
    fernet: Fernet = Fernet(ENCRYPTION_KEY)
    return fernet.encrypt(data.encode()).decode()


def decrypt_data(data: str) -> str:
    """Decrypts encrypted data using Fernet."""
    fernet: Fernet = Fernet(ENCRYPTION_KEY)
    return fernet.decrypt(data.encode()).decode()


# from api.core.encryption.encryption_handlers import encrypt_data, decrypt_data

# # Encrypting data before sending it to an external service or storing it
# encrypted_data = encrypt_data("sensitive_data")

# # Decrypting data when retrieving it
# decrypted_data = decrypt_data(encrypted_data)
