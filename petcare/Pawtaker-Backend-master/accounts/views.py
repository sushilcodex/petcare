from drf_spectacular.utils import extend_schema
from rest_framework import generics
from django.template.loader import render_to_string
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .serializers import *
from pet.models import *
from rest_framework import permissions
from accounts.utils import send_email
from accounts.constants import WELCOME_EMAIL_SUBJECT, RESET_PASSWORD_EMAIL_SUBJECT
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


@extend_schema(tags=["User-Account-Registeration Api's"])
class UserRegistrationView(generics.CreateAPIView):
    """
    User Registration API.
    """

    parser_classes = (MultiPartParser, FormParser)

    serializer_class = UserSerializer
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user_register_obj = serializer.save()
        recipient_list = str(user_register_obj)
        context = {
            "request": request._request,
            "name": user_register_obj.parent_name,
        }
        body_text_content = render_to_string("emails/text/welcome-page.txt")
        subject = WELCOME_EMAIL_SUBJECT
        html_content = render_to_string("emails/html/welcome-page.html", context)
        send_email(subject, body_text_content, [recipient_list], html_content)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["User-Account-Registeration Api's"])
class SendPasswordEmailView(generics.CreateAPIView):
    """
    Sending email to user for resetting the password.
    """

    serializer_class = ResetPasswordLinkSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_password_obj = serializer.save()
        context = {
            "link": f"{settings.FRONT_END_CHANGE_PASSWORD_URL}{reset_password_obj.id}",
            "reset_password_obj": reset_password_obj,
            "request": request._request,  # WSGI Request object
            "name": reset_password_obj.user.parent_name,
        }
        body_text_content = render_to_string("emails/text/password-reset-email.txt")
        subject = RESET_PASSWORD_EMAIL_SUBJECT
        html_content = render_to_string(
            "emails/html/password-reset-email.html", context
        )
        send_email(
            subject, body_text_content, [reset_password_obj.user.email], html_content
        )
        return Response(
            "Password Reset link send. Please check your email",
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["User-Account-Registeration Api's"])
class ChangePasswordViews(generics.CreateAPIView):
    """
    This function help user to change the password
    after login.
    Validating user old password.

    """

    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Password updated successfully"}, status=status.HTTP_200_OK
        )


@extend_schema(tags=["User-Account-Registeration Api's"])
class UserPasswordRestView(generics.CreateAPIView):
    """
    User reset password function when reset request
    received by email.
    """

    serializer_class = UserPasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserPasswordResetSerializer(data=request.data, context=kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Password Reset Successfully"}, status=status.HTTP_200_OK
        )


@extend_schema(tags=["User-Account-Registeration Api's"])
class UserProfileUpdateView(generics.UpdateAPIView):
    """
    User Profile update
    """

    parser_classes = (MultiPartParser, FormParser)

    serializer_class = UserProfileUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["patch"]

    @extend_schema(
        summary="User Profile Update Api",
        description="User can update all the fields except the email. "
        "Parent Name, Phone Number, Country Code, Address "
        "and Email are required fields.",
    )
    def patch(self, request, *args, **kwargs):
        uuid = request.user.id
        instance = CustomUser.objects.get(id=uuid)
        serializer = self.serializer_class(
            instance, data=request.data, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data.get("new_password")
        if new_password:
            instance.set_password(new_password)
            instance.save()

        serializer.save()
        return Response(
            {"data": serializer.data, "message": "Profile updated successfully"},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["User-Account-Registeration Api's"])
class UserDetails(generics.RetrieveAPIView):
    """
    User details
    """

    serializer_class = UserDetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        uuid = request.user.id
        instance = CustomUser.objects.get(id=uuid)
        serializers = self.serializer_class(instance, context={"request": request})
        return Response(serializers.data, status=status.HTTP_200_OK)


def page_not_found_view(request, exception):
    return render(request, "404.html", status=404)


def Bad_Gateway(request, exception):
    return render(request, "502.html", status=404)


@extend_schema(tags=["Authentication Api's"])
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(tags=["Authentication APIs"])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token_data = serializer.validated_data

            return Response(token_data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


@extend_schema(tags=["Authentication Api's"])
class CustomTokenRefreshView(TokenRefreshView):
    pass
