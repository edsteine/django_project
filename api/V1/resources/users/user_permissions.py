from django.contrib.auth.models import User
from django.views import View
from rest_framework import permissions
from rest_framework.request import Request


class IsAdminUser(permissions.BasePermission):
    """Custom permission to only allow admin users to perform certain actions"""

    def has_permission(self, request: Request, view: View) -> bool:
        """Check if the user has permission to perform the action.

        Args:
            request (Request): The incoming request.
            view (View): The view that the permission is being checked for.

        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        return request.user.is_authenticated and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """Custom permission to only allow owners of an object or admins to edit it"""

    def has_object_permission(self, request: Request, view: View, obj: User | object) -> bool:
        """Check if the user has permission to access or modify the object.

        Args:
            request (Request): The incoming request.
            view (View): The view that the permission is being checked for.
            obj (Union[User, object]): The object the permission is being checked for (could be a User or other model instance).

        Returns:
            bool: True if the user is the owner or an admin, False otherwise.

        """
        return obj == request.user or request.user.is_staff
