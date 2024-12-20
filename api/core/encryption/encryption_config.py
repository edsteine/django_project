"""api/core/encryption/encryption_config.py
Encryption configuration.

Defines encryption settings, schemes, and behavior, including the
encryption key and the algorithm used.
"""

from environ import Env

# from environ import Env  # type: ignore[import-untyped]

# Initialize environment variables using environ
env_variables = Env()
Env.read_env(".env")


# Type annotations for known types
ENCRYPTION_KEY: str = env_variables("ENCRYPTION_KEY")
ENCRYPTION_ALGORITHM: str = env_variables("ENCRYPTION_ALGORITHM")
