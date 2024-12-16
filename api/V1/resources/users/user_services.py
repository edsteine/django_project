from api.V1.resources.users.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


class UserService:
    @classmethod
    def search_users(cls, query, role=None):
        """Advanced user search with optional role filtering"""
        search_query = Q(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query) | Q(username__icontains=query),
        )

        if role:
            search_query &= Q(role=role)

        return User.objects.filter(search_query)

    @classmethod
    def get_user_details(cls, user_id):
        """Retrieve detailed user information"""
        try:
            return User.objects.select_related("hair", "address", "bank", "company", "crypto").get(id=user_id)
        except User.DoesNotExist as err:
            raise ObjectDoesNotExist(f"User with id {user_id} not found.") from err
