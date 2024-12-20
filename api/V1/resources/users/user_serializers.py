from typing import Any, ClassVar

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):  # type: ignore
    pass

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs: ClassVar[dict[str, dict[str, bool | str]]] = {
            "password": {"write_only": True},
            "username": {"required": False},  # Make username optional
        }

    def create(self, validated_data: dict[str, Any]) -> User:
        """Create a user, generating a unique username if not provided.

        Args:
            validated_data (dict[str, Any]): The validated data for creating the user.

        Returns:
            User: The created user instance.

        """
        # Ensure username is set
        if "username" not in validated_data or not validated_data["username"]:
            # Generate username from email if not provided
            email = validated_data.get("email", "")
            username = email.split("@")[0]
            validated_data["username"] = self._generate_unique_username(username)

        # Create user
        user = User.objects.create_user(**validated_data)

        return user

    def _generate_unique_username(self, base_username: str) -> str:
        """Generate a unique username by checking if it already exists.

        Args:
            base_username (str): The base username to check.

        Returns:
            str: The unique username.

        """
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        return username
