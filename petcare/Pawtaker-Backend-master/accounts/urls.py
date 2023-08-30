from django.urls import path
from .views import (
    UserRegistrationView,
    SendPasswordEmailView,
    UserPasswordRestView,
    ChangePasswordViews,
    UserProfileUpdateView,
    UserDetails,
)


urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path(
        "send-password-reset-link/",
        SendPasswordEmailView.as_view(),
        name="password-reset-email.html",
    ),
    path(
        "reset/change-password/<uuid:uid>/",
        UserPasswordRestView.as_view(),
        name="password-reset",
    ),
    path("change-password/", ChangePasswordViews.as_view(), name="change_password"),
    path(
        "user-profile-update/",
        UserProfileUpdateView.as_view(),
        name="user_profile_setting",
    ),
    path("user-details/", UserDetails.as_view(), name="user-details"),
    # path("pet-post/<uuid:uuid>",PetPostDetails.as_view(),name='PetPostDetails')
]
