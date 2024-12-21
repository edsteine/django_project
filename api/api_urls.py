from django.urls import include, path
from django.urls.resolvers import URLPattern, URLResolver
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.V1.resources.users.user_views import UserViewSet

router: DefaultRouter = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")


urlpatterns: list[URLPattern | URLResolver] = [
    path("", include(router.urls)),  # User-related endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Token obtain endpoint
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Token refresh endpoint
]
