"""
File: api/api_apps.py
Date updated: 2024-12-21
Author: Adil AJDAA
Email: a.ajdaa@outlook.com
Project: Ed Project
Description: Registers the API app as a Django application, defining app-specific configurations,
including settings and any initialization logic that runs when the app is ready.
Used Libraries: django.apps.AppConfig, cache, redis
"""

import logging

import redis

from django.apps import AppConfig
from django.core.cache import cache

logging.basicConfig()
logger = logging.getLogger(__name__)


class ApiConfig(AppConfig):
    """Configuration class for the 'api' application."""

    name: str = "api"
    verbose_name: str = "API"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        """App-specific initialization when the app is ready."""
        try:
            # Test Redis connection
            r = redis.Redis()
            r.ping()  # Check if Redis is available
            logger.info("Successfully connected to Redis")

            # Example of using cache
            cache.set("api_status", "active", timeout=60 * 5)  # Cache for 5 minutes
            status = cache.get("api_status")
            logger.info("Cache status: %s", status)

        except redis.ConnectionError as e:
            logger.error("Redis connection error: %s", e)
            raise
        # from api.V1.resources.users import models  # if you have signals
