# api/core/utils/core_exceptions.py
"""Custom exceptions.

Defines exceptions for specific error cases, enabling better error
handling and debugging across the application.
"""


class CustomExceptionError(Exception):
    """Custom exception for specific error cases.

    This exception can be raised to handle specific error conditions that
    require more detailed or customized error messages. It extends the base
    `Exception` class, adding a `message` attribute for additional context.

    Attributes:
        message (str): The error message associated with the exception.

    """

    def __init__(self, message):
        """Initializes the exception with a custom message.

        Args:
            message (str): The error message to be attached to the exception.

        """
        self.message = message
        super().__init__(self.message)
