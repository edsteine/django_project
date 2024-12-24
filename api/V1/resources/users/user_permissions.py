"""
File: permissions.py
Date updated: 2024-12-23
Author: Adil AJDAA
Email: a.ajdaa@outlook.com
Project: Ed Project
Description: Custom permissions to control access based on user roles and object ownership.
Used Libraries: django, rest_framework
"""

from api.V1.resources.users.models import User

# from django.contrib.auth.models import User
from django.views import View
from rest_framework import permissions
from rest_framework.request import Request


class IsAdminUser(permissions.BasePermission):
    """
    Allows only admin users (staff) to perform actions.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_authenticated and request.user.is_staff


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Grants access to an object if the user is the owner or an admin.
    """

    def has_object_permission(self, request: Request, view: View, obj: User | object) -> bool:
        return obj == request.user or request.user.is_staff


class IsAuthenticated(permissions.BasePermission):
    """
    Grants access only to authenticated users.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_authenticated


class IsOwner(permissions.BasePermission):
    """
    Allows access only to the owner of the object.
    """

    def has_object_permission(self, request: Request, view: View, obj: User) -> bool:
        return request.user.is_authenticated and obj == request.user


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Allows read-only access for unauthenticated users, but requires authentication for other methods.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated


class IsSuperuser(permissions.BasePermission):
    """
    Grants access only to superusers (admin with full privileges).
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_superuser
