from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
)
from django.db import models
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _
from petcare_project import settings


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, password2=None):
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="User ID",
        unique=True,
    )
    parent_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    country_code = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=250, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)
    favourite_pet = models.ManyToManyField(
        "pet.PetProfile", related_name="favourite_pet"
    )
    image = models.ImageField(
        upload_to="images/", max_length=254, null=True, blank=True
    )

    like = models.ManyToManyField("pet.PetProfile", related_name="like")

    USERNAME_FIELD = "email"
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class ResetPasswordLink(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="id",
        unique=True,
    )
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="reset_password_link"
    )
    created_at = models.DateTimeField(auto_now_add=False)
    expired_at = models.DateTimeField(auto_now_add=False)

    class Meta:
        db_table = "reset_password_link"
