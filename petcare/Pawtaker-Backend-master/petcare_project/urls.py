from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from accounts.views import CustomTokenObtainPairView, CustomTokenRefreshView


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/login/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/pet/", include("pet.urls")),
    path("api/v1/blog/", include("blog.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = "accounts.views.page_not_found_view"
handler502 = "accounts.views.Bad_Gateway"
