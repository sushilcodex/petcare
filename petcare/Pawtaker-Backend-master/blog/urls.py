from rest_framework import routers
from django.urls import path, include
from .views import BlogListingView

router = routers.DefaultRouter()

router.register(
    f"blogs",
    BlogListingView,
)


urlpatterns = [
    path("", include(router.urls)),
]
