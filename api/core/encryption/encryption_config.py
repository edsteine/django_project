"""api/core/encryption/encryption_config.py
Encryption configuration.

Defines encryption settings, schemes, and behavior, including the
encryption key and the algorithm used.
"""

import environ  # type: ignore

# Initialize environment variables
env = environ.Env()

# Read .env file
environ.Env.read_env()

# Type annotations for known types
ENCRYPTION_KEY: str = env("ENCRYPTION_KEY")  # Type hinting the encryption key as a string
ENCRYPTION_ALGORITHM: str = env("ENCRYPTION_ALGORITHM")  # Type hinting the algorithm as a string
