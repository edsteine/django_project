"""
File: project_urls.py
Date updated: 2024-12-23
Author: Adil AJDAA
Email: a.ajdaa@outlook.com
Project: Ed Project
Description: Project-level URL configuration.

Maps top-level URLs to appropriate views and includes.
Defines admin, API, and other high-level URL patterns.
Central routing configuration for the entire project.
Used Libraries: django, drf_yasg, rest_framework
"""

from api import views
from api.core.utils.core_constants import API_VERSION, CONTACT, DESCRIPTION, LICENSE, TITLE
from api.V1.resources.users.user_permissions import IsAdminOrSuperUser
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
)
from django.urls import URLPattern, URLResolver, include, path
from drf_yasg import openapi  # type: ignore[import-untyped]
from drf_yasg.views import get_schema_view  # type: ignore[import-untyped]
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title=TITLE,
        default_version=API_VERSION,
        description=DESCRIPTION,
        contact=openapi.Contact(email=CONTACT),
        license=openapi.License(name=LICENSE),
    ),
    public=False,
    permission_classes=[IsAdminOrSuperUser],
)


urlpatterns: list[URLPattern | URLResolver] = [
    path("", views.home, name="home"),  # Homepage with links
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),  # Admin interface
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/", include("api.api_urls")),
    path("swagger/", login_required(schema_view.with_ui("swagger", cache_timeout=0)), name="swagger-docs"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("__debug__/", include("debug_toolbar.urls")),
    path("login/", LoginView.as_view(), name="login"),
    # path("logout/", LogoutView.as_view(), name="logout"),
    # path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    # path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
# https://127.0.0.1:8000/admin/
# https://127.0.0.1:8000/admin/login
# https://127.0.0.1:8000/admin/logout
# https://127.0.0.1:8000/admin/password_change
# https://127.0.0.1:8000/admin/password_change/done/
# https://127.0.0.1:8000/admin/autocomplete
# https://127.0.0.1:8000/admin/jsi18n
# https://127.0.0.1:8000/accounts/
# https://127.0.0.1:8000/accounts/login
# https://127.0.0.1:8000/accounts/logout
# https://127.0.0.1:8000/accounts/password_change
# https://127.0.0.1:8000/accounts/password_change/done/
# https://127.0.0.1:8000/accounts/password_reset
# https://127.0.0.1:8000/accounts/password_reset/done/
# https://127.0.0.1:8000/accounts/reset/done/
# https://127.0.0.1:8000/logout/
# https://127.0.0.1:8000/password_change/
# https://127.0.0.1:8000/password_reset/
# https://127.0.0.1:8000/accounts/password_reset/done/
# https://127.0.0.1:8000/api-auth/logout/
# https://127.0.0.1:8000/api-auth/login/
# https://127.0.0.1:8000/login/

handler404 = views.custom_404
