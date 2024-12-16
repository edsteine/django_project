from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .user_serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create", "login"]:
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def create_user(self, request):
        """Create a new user"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    def read_user(self, request, pk=None):
        """Get a user by ID"""
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=["PUT"], permission_classes=[IsAuthenticated])
    def update_user(self, request, pk=None):
        """Update user data"""
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["DELETE"], permission_classes=[IsAuthenticated])
    def delete_user(self, request, pk=None):
        """Delete a user"""
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def search_users(self, request):
        """Search users by name"""
        query = request.query_params.get("name", "")
        users = User.objects.filter(first_name__icontains=query) | User.objects.filter(last_name__icontains=query)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def list_users(self, request):
        """List all users with optional pagination"""
        page = request.query_params.get("page", 1)
        limit = request.query_params.get("limit", 10)
        users = User.objects.all()[(int(page) - 1) * int(limit) : int(page) * int(limit)]
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def filter_users(self, request):
        """Filter users by role and status"""
        role = request.query_params.get("role")
        status = request.query_params.get("status")
        users = User.objects.filter(role=role, is_active=status)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"], permission_classes=[IsAuthenticated])
    def bulk_create(self, request):
        """Bulk create users"""
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["PUT"], permission_classes=[IsAuthenticated])
    def bulk_update(self, request):
        """Bulk update users"""
        for user_data in request.data:
            user = User.objects.get(id=user_data["id"])
            serializer = self.get_serializer(user, data=user_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response({"message": "Bulk update successful"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["DELETE"], permission_classes=[IsAuthenticated])
    def bulk_delete(self, request):
        """Bulk delete users"""
        ids = request.data.get("ids", [])
        User.objects.filter(id__in=ids).delete()
        return Response({"message": "Bulk delete successful"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def login(self, request):
        """Login user"""
        # Implement JWT or other login mechanism
        pass

    @action(detail=False, methods=["POST"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Logout user"""
        # Handle logout logic
        pass

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def verify(self, request):
        """Verify user email"""
        # Implement email verification logic
        pass

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def forgot_password(self, request):
        """Send password reset link"""
        # Send reset link to email
        pass

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def reset_password(self, request):
        """Reset user password"""
        # Reset password logic
        pass

    @action(detail=True, methods=["PUT"], permission_classes=[IsAuthenticated])
    def update_profile(self, request, pk=None):
        """Update user profile data"""
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["PATCH"], permission_classes=[IsAuthenticated])
    def change_status(self, request, pk=None):
        """Change user status"""
        status = request.data.get("status")
        user = self.get_object()
        user.is_active = status == "active"
        user.save()
        return Response({"status": "Status updated successfully"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def assign_role(self, request, pk=None):
        """Assign role to user"""
        role = request.data.get("role")
        user = self.get_object()
        user.role = role
        user.save()
        return Response({"role": "Role assigned successfully"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["DELETE"], permission_classes=[IsAuthenticated])
    def remove_role(self, request, pk=None):
        """Remove role from user"""
        user = self.get_object()
        user.role = ""
        user.save()
        return Response({"role": "Role removed successfully"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], permission_classes=[IsAuthenticated])
    def enable_account(self, request, pk=None):
        """Enable user account"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({"message": "Account enabled"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], permission_classes=[IsAuthenticated])
    def disable_account(self, request, pk=None):
        """Disable user account"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({"message": "Account disabled"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"], permission_classes=[IsAuthenticated])
    def live_status(self, request, pk=None):
        """Check live status of a user"""
        user = self.get_object()
        status = "active" if user.is_active else "inactive"
        return Response({"status": status}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], permission_classes=[IsAuthenticated])
    def deactivate_account(self, request, pk=None):
        """Deactivate user account"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({"message": "Account deactivated"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], permission_classes=[IsAuthenticated])
    def reactivate_account(self, request, pk=None):
        """Reactivate user account"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({"message": "Account reactivated"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"], permission_classes=[IsAuthenticated])
    def update_role(self, request, pk=None):
        """Update user role"""
        user = self.get_object()
        role = request.data.get("role")
        user.role = role
        user.save()
        return Response({"role": "Role updated successfully"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PUT"], permission_classes=[IsAuthenticated])
    def update_password(self, request, pk=None):
        """Update user password"""
        user = self.get_object()
        password = request.data.get("password")
        user.set_password(password)
        user.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def upload_image(self, request, pk=None):
        """Upload or update user profile image"""
        user = self.get_object()
        image = request.data.get("image")
        user.image = image
        user.save()
        return Response({"message": "Image uploaded successfully"}, status=status.HTTP_200_OK)
