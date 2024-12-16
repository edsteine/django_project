# api/core/utils/core_validators.py
"""Core validators.

Implements general validation logic for commonly used validation patterns
like email, phone numbers, etc., to ensure data integrity across the app.
"""

import re


def validate_email(email: str) -> bool:
    """Validates email format."""
    email_regex = r"(^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$)"
    return re.match(email_regex, email) is not None
