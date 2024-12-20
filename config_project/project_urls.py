# project_urls.py
"""Project-level URL configuration.

Maps top-level URLs to appropriate views and includes.
Defines admin, API, and other high-level URL patterns.
Central routing configuration for the entire project.
"""

from django.contrib import admin
from django.urls import URLResolver, include, path

# Type annotations for the urlpatterns variable, ensuring it passes mypy's checks

urlpatterns: list[URLResolver] = [
    path("admin/", admin.site.urls),  # Admin interface
    path("api/v1/", include("api.api_urls")),  # Include API v1 URLs
]
