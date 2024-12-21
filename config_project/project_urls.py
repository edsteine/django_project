# project_urls.py
"""Project-level URL configuration.

Maps top-level URLs to appropriate views and includes.
Defines admin, API, and other high-level URL patterns.
Central routing configuration for the entire project.
"""

from django.contrib import admin
from django.urls import URLResolver, include, path
from drf_yasg import openapi  # type: ignore[import-untyped]
from drf_yasg.views import get_schema_view  # type: ignore[import-untyped]
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Ed Project Api",
        default_version="v1",
        description="""ED Project is a comprehensive Django REST API framework designed for robust,
          secure, and scalable web applications. Built with modern Python development practices,
            this project provides a solid foundation for building enterprise-grade web services.",
        terms_of_service="https://www.google.com/policies/terms/""",
        contact=openapi.Contact(email="a.ajdaa@outlook.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns: list[URLResolver] = [
    path("admin/", admin.site.urls),  # Admin interface
    path("api/v1/", include("api.api_urls")),  # Include API v1 URLs
    path("__debug__/", include("debug_toolbar.urls")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-docs"),
    path("accounts/", include("django.contrib.auth.urls")),
]
