from api.V1.resources.users.models import User
from django.db.models import Q, QuerySet


class UserService:
    @classmethod
    def search_users(cls, query: str, role: str | None = None) -> QuerySet[User]:
        """Advanced user search with optional role filtering.

        Args:
            query (str): The search query to match against user fields.
            role (Optional[str]): An optional role to filter the users by.

        Returns:
            QuerySet[User]: A QuerySet of users that match the search criteria.
        """
        search_query = Q(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query) | Q(username__icontains=query),
        )

        if role:
            search_query &= Q(role=role)

        return User.objects.filter(search_query)  # Using the model's objects manager

    @classmethod
    def get_user_details(cls, user_id: int) -> User | None:
        """Retrieve detailed user information.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            Optional[User]: The user instance with detailed information or None if not found.

        Raises:
            ObjectDoesNotExist: If the user with the given ID is not found.

        """
        return User.objects.select_related("hair", "address", "bank", "company", "crypto").filter(id=user_id).first()
