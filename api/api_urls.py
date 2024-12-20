from django.urls import include, path
from django.urls.resolvers import URLPattern, URLResolver
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.V1.resources.users.user_views import UserViewSet

router: DefaultRouter = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")


urlpatterns: list[URLPattern | URLResolver] = [
    path("", include(router.urls)),  # User-related endpoints
    path("", include(router.urls)),  # User-related endpoints
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Token refresh endpoint
    # Custom User URLs
    path(
        "users/create/",
        UserViewSet.as_view({"post": "create_user"}),
        name="create_user",
    ),
    path("users/<int:pk>/", UserViewSet.as_view({"get": "read_user"}), name="read_user"),
    path(
        "users/<int:pk>/update/",
        UserViewSet.as_view({"put": "update_user"}),
        name="update_user",
    ),
    path(
        "users/<int:pk>/delete/",
        UserViewSet.as_view({"delete": "delete_user"}),
        name="delete_user",
    ),
    path(
        "users/search/",
        UserViewSet.as_view({"get": "search_users"}),
        name="search_users",
    ),
    path("users/list/", UserViewSet.as_view({"get": "list_users"}), name="list_users"),
    path(
        "users/filter/",
        UserViewSet.as_view({"get": "filter_users"}),
        name="filter_users",
    ),
    path("users/login/", UserViewSet.as_view({"post": "login"}), name="login_user"),
    path("users/logout/", UserViewSet.as_view({"post": "logout"}), name="logout_user"),
    path("users/verify/", UserViewSet.as_view({"post": "verify"}), name="verify_user"),
    path(
        "users/forgot-password/",
        UserViewSet.as_view({"post": "forgot_password"}),
        name="forgot_password",
    ),
    path(
        "users/reset-password/",
        UserViewSet.as_view({"post": "reset_password"}),
        name="reset_password",
    ),
    path(
        "users/<int:pk>/profile/",
        UserViewSet.as_view({"put": "update_profile"}),
        name="update_profile",
    ),
    path(
        "users/<int:pk>/status/",
        UserViewSet.as_view({"patch": "change_status"}),
        name="change_status",
    ),
    path(
        "users/<int:pk>/assign-role/",
        UserViewSet.as_view({"post": "assign_role"}),
        name="assign_role",
    ),
    path(
        "users/<int:pk>/remove-role/",
        UserViewSet.as_view({"delete": "remove_role"}),
        name="remove_role",
    ),
    path(
        "users/<int:pk>/enable/",
        UserViewSet.as_view({"patch": "enable_account"}),
        name="enable_account",
    ),
    path(
        "users/<int:pk>/disable/",
        UserViewSet.as_view({"patch": "disable_account"}),
        name="disable_account",
    ),
    path(
        "users/<int:pk>/status/",
        UserViewSet.as_view({"get": "live_status"}),
        name="live_status",
    ),
    path(
        "users/<int:pk>/deactivate/",
        UserViewSet.as_view({"patch": "deactivate_account"}),
        name="deactivate_account",
    ),
    path(
        "users/<int:pk>/reactivate/",
        UserViewSet.as_view({"patch": "reactivate_account"}),
        name="reactivate_account",
    ),
    path(
        "users/<int:pk>/role/",
        UserViewSet.as_view({"patch": "update_role"}),
        name="update_role",
    ),
    path(
        "users/<int:pk>/password/",
        UserViewSet.as_view({"put": "update_password"}),
        name="update_password",
    ),
    path(
        "users/<int:pk>/image/",
        UserViewSet.as_view({"post": "upload_image"}),
        name="upload_image",
    ),
]
