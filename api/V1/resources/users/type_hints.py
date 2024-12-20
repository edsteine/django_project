from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    pass


class UserProtocol(Protocol):
    """Protocol defining the expected methods and attributes of a User model."""

    email: str
    username: str
    is_staff: bool
    is_superuser: bool
    is_active: bool

    def set_password(self, raw_password: str) -> None: ...
    def save(
        self,
        using: str | None = None,
        force_insert: bool = False,
        force_update: bool = False,
        **kwargs: dict[str, Any],  # Type annotation for **kwargs
    ) -> None: ...
