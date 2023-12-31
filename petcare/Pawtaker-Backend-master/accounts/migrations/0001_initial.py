# Generated by Django 4.1.6 on 2023-08-16 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="User ID",
                    ),
                ),
                ("parent_name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, null=True, region=None
                    ),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("address", models.CharField(blank=True, max_length=250, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
                (
                    "image",
                    models.ImageField(
                        blank=True, max_length=254, null=True, upload_to="images/"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ResetPasswordLink",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="id",
                    ),
                ),
                ("created_at", models.DateTimeField()),
                ("expired_at", models.DateTimeField()),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reset_password_link",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "reset_password_link",
            },
        ),
    ]
