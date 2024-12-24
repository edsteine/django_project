from api.V1.resources.users.user_views import UserViewSet
from django.urls import include, path
from django.urls.resolvers import URLPattern, URLResolver
from rest_framework.routers import DefaultRouter

router: DefaultRouter = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")


urlpatterns: list[URLPattern | URLResolver] = [
    path("", include(router.urls)),  # User-related endpoints
]
