# project_urls.py
"""Project-level URL configuration.

Maps top-level URLs to appropriate views and includes.
Defines admin, API, and other high-level URL patterns.
Central routing configuration for the entire project.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin interface
    path("api/v1/", include("api.api_urls")),  # Include API v1 URLs
]
