from typing import Any

from api.V1.resources.users.models import User
from api.V1.resources.users.user_serializers import UserSerializer
from django.db.models import QuerySet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken


class UserPagination(PageNumberPagination):
    page_size: int = 10  # Adjust according to your needs


class UserViewSet(viewsets.ModelViewSet[User]):
    queryset: QuerySet[User] = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # noqa: RUF012
    pagination_class = UserPagination

    def get_permissions(self) -> list[Any]:
        """Override permissions based on action."""
        if self.action in ["create", "login"]:
            return [AllowAny()]
        return list(super().get_permissions())

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def create_user(self, request: Request) -> Response:
        """Create a new user"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, content_type="application/json")

    @action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    def read_user(self, request: Request, pk: int) -> Response:
        """Get a user by ID"""
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data, content_type="application/json")

    @action(detail=True, methods=["PUT"], permission_classes=[IsAuthenticated])
    def update_user(self, request: Request, pk: int) -> Response:
        """Update user data"""
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, content_type="application/json")

    @action(detail=True, methods=["DELETE"], permission_classes=[IsAuthenticated])
    def delete_user(self, request: Request, pk: int) -> Response:
        """Delete a user"""
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, content_type="application/json")

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def search_users(self, request: Request) -> Response:
        """Search users by name"""
        query = request.query_params.get("name", "")
        users = User.objects.filter(first_name__icontains=query) | User.objects.filter(last_name__icontains=query)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, content_type="application/json")

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def list_users(self, request: Request) -> Response:
        """List all users with optional pagination"""
        page = int(request.query_params.get("page", 1))
        limit = int(request.query_params.get("limit", 10))
        users = User.objects.all()[(page - 1) * limit : page * limit]
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, content_type="application/json")

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def filter_users(self, request: Request) -> Response:
        """Filter users by role and status"""
        role = request.query_params.get("role", "")
        user_status = request.query_params.get("status", "inactive")  # Default value
        users = User.objects.filter(role=role, is_active=(user_status == "active"))
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, content_type="application/json")

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def login(self, request: Request) -> Response:
        """Login user and return JWT token"""
        # Extract username and password from request data
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = User.objects.filter(username=username).first()
        if not isinstance(password, str) or user is None or not user.check_password(password):
            raise AuthenticationFailed("Invalid credentials")

        # Create JWT tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.token

        return Response(
            {
                "access": str(access),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
            content_type="application/json",
        )

    @action(detail=False, methods=["POST"], permission_classes=[IsAuthenticated])
    def logout(self, request: Request) -> Response:
        """Logout user by removing their refresh token from the client side"""
        try:
            # Optionally, blacklist the refresh token if using a token store
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                # Optionally, you can blacklist the refresh token here
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklisting the token (requires additional setup)

            # Optionally handle client-side logic (clear cookies, local storage, etc.)
            return Response(
                {"message": "Logout successful, token invalidated."}, status=status.HTTP_200_OK, content_type="application/json"
            )
        except InvalidToken:
            return Response({"message": "Invalid token provided."}, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def verify(self, request: Request) -> Response:
        """Verify user email"""
        # Implement email verification logic
        return Response(
            {"message": "Verification method not implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED, content_type="application/json"
        )

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def forgot_password(self, request: Request) -> Response:
        """Send password reset link"""
        # Send reset link to email
        return Response(
            {"message": "Forgot password method not implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED, content_type="application/json"
        )

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def reset_password(self, request: Request) -> Response:
        """Reset user password"""
        # Reset password logic
        return Response(
            {"message": "Reset password method not implemented"}, status=status.HTTP_501_NOT_IMPLEMENTED, content_type="application/json"
        )

    @action(detail=True, methods=["PUT"], permission_classes=[IsAuthenticated])
    def update_profile(self, request: Request, pk: int) -> Response:
        """Update user profile data"""
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, content_type="application/json")

    @action(detail=True, methods=["PATCH"], permission_classes=[IsAuthenticated])
    def change_status(self, request: Request, pk: int) -> Response:
        """Change user status"""
        status_param = request.data.get("status", "inactive")
        user = self.get_object()
        user.is_active = status_param == "active"
        user.save()
        return Response({"status": "Status updated successfully"}, status=status.HTTP_200_OK, content_type="application/json")

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def assign_role(self, request: Request, pk: int) -> Response:
        """Assign role to user"""
        role = request.data.get("role", "")
        user = self.get_object()
        user.role = role
        user.save()
        return Response({"role": "Role assigned successfully"}, status=status.HTTP_200_OK, content_type="application/json")

    @action(detail=True, methods=["DELETE"], permission_classes=[IsAuthenticated])
    def remove_role(self, request: Request, pk: int) -> Response:
        """Remove role from user"""
        user = self.get_object()
        user.role = ""
        user.save()
        return Response({"role": "Role removed successfully"}, status=status.HTTP_200_OK, content_type="application/json")

    @action(detail=True, methods=["PATCH"], permission_classes=[IsAuthenticated])
    def enable_account(self, request: Request, pk: int) -> Response:
        """Enable user account"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({"message": "Account enabled"}, status=status.HTTP_200_OK, content_type="application/json")

    @action(detail=True, methods=["PATCH"], permission_classes=[IsAuthenticated])
    def disable_account(self, request: Request, pk: int) -> Response:
        """Disable user account"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({"message": "Account disabled"}, status=status.HTTP_200_OK, content_type="application/json")

    @action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    def live_status(self, request: Request, pk: int) -> Response:
        """Check live status of a user"""
        user = self.get_object()
        user_status = "active" if user.is_active else "inactive"
        return Response({"status": user_status}, status=status.HTTP_200_OK, content_type="application/json")

    @action(detail=True, methods=["PATCH"], permission_classes=[IsAuthenticated])
    def deactivate_account(self, request: Request, pk: int) -> Response:
        """Deactivate user account"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({"message": "Account deactivated"}, status=status.HTTP_200_OK, content_type="application/json")

    @action(detail=True, methods=["PATCH"], permission_classes=[IsAuthenticated])
    def reactivate_account(self, request: Request, pk: int) -> Response:
        """Reactivate user account"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({"message": "Account reactivated"}, status=status.HTTP_200_OK, content_type="application/json")

    @action(detail=True, methods=["PATCH"], permission_classes=[IsAuthenticated])
    def update_role(self, request: Request, pk: int) -> Response:
        """Update user role"""
        user = self.get_object()
        role = request.data.get("role", "")
        user.role = role
        user.save()
        return Response({"role": "Role updated successfully"}, status=status.HTTP_200_OK, content_type="application/json")

    # @action(detail=True, methods=["PATCH"], permission_classes=[IsAuthenticated])
    # def update_permissions(self, request: Request, pk: int) -> Response:
    #     """Update user permissions"""
    #     try:
    #         user = self.get_object()
    #         permissions = request.data.get("permissions", [])

    #         if not permissions:
    #             return Response({"error": "No permissions provided"}, status=status.HTTP_400_BAD_REQUEST)

    #         # Use `user_permissions` instead of `permissions`
    #         user.user_permissions.set(permissions)
    #         user.save()

    #      return Response({"permissions": "Permissions updated successfully"}, status=status.HTTP_200_OK, content_type="application/json")

    #     except Exception as e:
    #         # Catch unexpected errors (e.g., database errors)
    #         return Response({"error": "An unexpected error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
