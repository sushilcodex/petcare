from django.urls import path, include
from .views import (
    PetProfileMediaViews,
    PetProfileViews,
    FavouritePetView,
    FavouritePetListing,
    LikePetView,
    LikedPetListing,
    PetTypeListing,
    PetBreedListing,
)
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(
    r"petprofile",
    PetProfileViews,
)
router.register(
    f"petmedia",
    PetProfileMediaViews,
)

urlpatterns = [
    path(
        "favourite-pet/<uuid:uuid>",
        FavouritePetView.as_view(),
        name="user_favourite_pet",
    ),
    path("favourite-listing/", FavouritePetListing.as_view(), name="favourite_listing"),
    path("like-pet/<uuid:uuid>", LikePetView.as_view(), name="user_like_pet"),
    path("like-listing/", LikedPetListing.as_view(), name="like_listing"),
    path("type-listing/", PetTypeListing.as_view(), name="type_listing"),
    path("breed-listing/<uuid:uuid>", PetBreedListing.as_view(), name="breed_listing"),
    path(r"", include(router.urls)),
]
