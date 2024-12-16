# api/V1/resources/users/user_permissions.py
from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Custom permission to only allow admin users to perform certain actions"""

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(permissions.BasePermission):
    """Custom permission to only allow owners of an object or admins to edit it"""

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff
