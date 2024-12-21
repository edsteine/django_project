"""api/core/encryption/encryption_config.py
Encryption configuration.

Defines encryption settings, schemes, and behavior, including the
encryption key and the algorithm used.
"""

# Import the Env class from the `environ` library to manage environment variables.
# from environ import Env

# Uncommented import, with type ignore (used to bypass type checking if required)
from environ import Env  # type: ignore[import-untyped]

# Initialize the Env object to load and parse environment variables.
env_variables = Env()

# Load environment variables from a `.env` file. Ensure `.env` exists in the project root.
# Env.read_env(".env")
Env.read_env()

# Type annotations ensure type safety for variables.
# Fetch the encryption key from the environment variables.
ENCRYPTION_KEY: str = env_variables("ENCRYPTION_KEY")

# Fetch the encryption algorithm from the environment variables.
ENCRYPTION_ALGORITHM: str = env_variables("ENCRYPTION_ALGORITHM")
