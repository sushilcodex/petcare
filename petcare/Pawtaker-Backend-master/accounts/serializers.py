import re
from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model

from pet.models import *
from rest_framework import status
from django.utils import timezone
from accounts.models import *
import json
import io
from datetime import datetime
from pet.models import PetProfile
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.hashers import check_password
from pet.serializers import PetPostSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=15, write_only=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        max_length=15, write_only=True, style={"input_type": "password"}
    )
    parent_name = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = (
            "parent_name",
            "email",
            "country_code",
            "phone_number",
            "password",
            "password2",
            "image",
            "date_of_birth",
            "address",
        )

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        phone_number = attrs.get("phone_number")
        parent_name = attrs.get("parent_name")
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pattern = re.compile(reg)
        pattern_phone_number = re.compile(r"^\d{10}$")

        if password != password2:
            raise serializers.ValidationError("Password doesn't match")
        elif not re.search(pattern, password):
            raise serializers.ValidationError(
                "Password is invalid. Password should be more than 8 characters and must"
                " contain one Uppercase, Lowercase and Alphanumeric value"
            )

        if re.search(r'[0-9!@#$%^&*(),.?":{}|<>]', parent_name):
            raise serializers.ValidationError(
                "Parent Name cannot contain special characters or numbers."
            )

        if not pattern_phone_number.match(phone_number):
            raise serializers.ValidationError("Phone Number is invalid")

        return attrs

    def create(self, validated_data):
        password = validated_data["password"]
        password = validated_data.pop("password2")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ResetPasswordLinkSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = ResetPasswordLink
        fields = [
            "email",
        ]

    def validate_email(self, email):
        if email:
            check_user = CustomUser.objects.filter(email=email).exists()
            if not check_user:
                raise serializers.ValidationError(
                    "No user exists with provided email id."
                )
        else:
            raise serializers.ValidationError("Please provide email id")
        return email

    def create(self, validated_data):
        user_obj = CustomUser.objects.get(email=validated_data.get("email"))
        current_datetime = timezone.now()
        if ResetPasswordLink.objects.filter(user=user_obj).exists():
            reset_password_link = user_obj.reset_password_link
        else:
            reset_password_link = ResetPasswordLink()
            reset_password_link.user = user_obj
        reset_password_link.created_at = current_datetime
        reset_password_link.expired_at = (
            current_datetime + settings.RESET_PASSWORD_EXPIRY
        )
        reset_password_link.save()
        return reset_password_link


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=15, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=15, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        id = self.context.get("uid")
        reset_password_link_obj = ResetPasswordLink.objects.filter(
            id=id, expired_at__gte=timezone.now()
        ).first()
        if reset_password_link_obj:
            if password != password2:
                raise serializers.ValidationError("Password are not same")
            elif not len(password) >= 8:
                raise serializers.ValidationError(
                    "Password length should be more than 8"
                )
            elif not re.findall("[A-Z]", password):
                raise serializers.ValidationError(
                    "The password must contain at least 1 uppercase letter, A-Z."
                )
            elif not re.findall("[a-z]", password):
                raise serializers.ValidationError(
                    "The password must contain at least 1 lowercase letter, a-z."
                )
        else:
            raise serializers.ValidationError("Link expired")
        return attrs

    def create(self, data):
        new_password = data.get("password")
        id = self.context.get("uid")
        reset_password_link_obj = ResetPasswordLink.objects.get(
            id=id, expired_at__gte=timezone.now()
        )
        user = CustomUser.objects.get(email=reset_password_link_obj.user.email)
        if user:
            user.set_password(new_password)
            user.save()
            reset_password_link_obj.delete()
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    class Meta:
        fields = ["old_password", "new_password", "confirm_new_password"]

    def validate(self, attrs):
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_new_password")
        email = self.context["request"].user
        user = CustomUser.objects.get(email=email)
        if user:
            if user.check_password(old_password):
                if old_password == new_password:
                    raise serializers.ValidationError(
                        "Password already has been used by you previous time please enter new "
                        "password."
                    )
            else:
                raise serializers.ValidationError(
                    "old password you entered is incorrect."
                )
        else:
            raise serializers.ValidationError("invalid credentials.")
        if new_password != confirm_password:
            raise serializers.ValidationError(
                "New password do not match with confirm password."
            )
        elif not len(new_password) >= 8:
            raise serializers.ValidationError("Password length should be more than 8")
        elif not re.findall("[A-Z]", new_password):
            raise serializers.ValidationError(
                "The password must contain at least 1 uppercase letter, A-Z."
            )
        elif not re.findall("[a-z]", new_password):
            raise serializers.ValidationError(
                "The password must contain at least 1 lowercase letter, a-z."
            )
        return attrs

    def create(self, data):
        new_password = data.get("new_password")
        email = self.context["request"].user
        user = CustomUser.objects.get(email=email)

        if user:
            user.set_password(new_password)
            user.save()
        return data


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField("get_image_url")
    old_password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=False)
    confirm_new_password = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "parent_name",
            "country_code",
            "phone_number",
            "date_of_birth",
            "address",
            "image_url",
            "image",
            "old_password",
            "new_password",
            "confirm_new_password",
        )
        extra_kwargs = {
            "parent_name": {"required": True},
            "phone_number": {"required": True},
            "date_of_birth": {"required": False},
            "address": {"required": True},
            "email": {"required": True},
            "country_code": {"required": True},
        }

    def validate_email(self, value):
        if self.instance.email != value:
            raise serializers.ValidationError(
                "You don't have permission to change your email."
            )
        return value

    def validate_new_password(self, value):
        data = self.get_initial()
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        pattern = re.compile(reg)

        if value == data.get("old_password"):
            raise serializers.ValidationError(
                "New password cannot be same as old password."
            )

        if not re.search(pattern, value):
            raise serializers.ValidationError(
                "Password is invalid. Password should be more than 8 characters and must"
                " contain one Uppercase, Lowercase and Alphanumeric value"
            )
        return value

    def validate_confirm_new_password(self, value):
        data = self.get_initial()
        if value != data.get("new_password"):
            raise serializers.ValidationError(
                "Confirm Password is not same as New Password."
            )
        return value

    def get_image_url(self, obj) -> str:
        request = self.context.get("request")
        image_obj = CustomUser.objects.get(id=obj.id)
        if hasattr(image_obj, "image") and image_obj.image:
            image_obj = image_obj.image.url
            image_obj = request.build_absolute_uri(image_obj)
        else:
            image_obj = ""
        date_of_birth = (
            obj.date_of_birth.strftime("%Y-%m-%d") if obj.date_of_birth else None
        )
        return image_obj


class UserDetailsSerializer(serializers.ModelSerializer):
    pet = serializers.SerializerMethodField("get_pet")
    image_url = serializers.SerializerMethodField("get_image_url")

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "parent_name",
            "phone_number",
            # "image",
            "image_url",
            "pet",
            "date_of_birth",
            "address",
        )

    def get_pet(self, obj) -> str:
        mydict = []
        pet_obj = PetProfile.objects.filter(user=obj)
        for pet in pet_obj:
            temp = {}

            image = PetMediaFile.objects.filter(pet_id=pet).first()
            if image:
                image = image.file.url
                temp["image"] = image
            temp["pet_name"] = pet.pet_name
            temp["pet_dob"] = pet.pet_dob

            mydict.append(temp)
        return mydict

    def get_image_url(self, obj) -> str:
        request = self.context.get("request")
        image_obj = CustomUser.objects.get(id=obj.id)
        if getattr(image_obj, "image"):
            image_obj = image_obj.image.url
            image_obj = request.build_absolute_uri(image_obj)
        else:
            image_obj = ""
        return image_obj


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def validate(self, attrs):
        data = {}
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = get_user_model().objects.get(email__iexact=email)
        except get_user_model().DoesNotExist:
            raise AuthenticationFailed("Username not found.")

        if not re.match(self.email_pattern, email):
            raise AuthenticationFailed(
                "Username format is invalid. Only alphanumeric characters and underscores are allowed."
            )

        if not re.match(r"^(?=.*\d)(?=.*[a-zA-Z]).{8,}$", password):
            raise AuthenticationFailed("Password format is invalid.")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password.")

        refresh = self.get_token(user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
