# Generated by Django 4.1.6 on 2023-08-16 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PetBreed",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="Breed ID",
                    ),
                ),
                ("pet_breed", models.CharField(blank=True, max_length=255, null=True)),
                ("slug", models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="PetType",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="Pettype ID",
                    ),
                ),
                ("pet_type", models.CharField(blank=True, max_length=255, null=True)),
                ("slug", models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="PetProfile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="pet ID",
                    ),
                ),
                ("pet_name", models.CharField(max_length=250)),
                ("pet_age", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "pet_gender",
                    models.CharField(
                        blank=True,
                        choices=[("male", "MALE"), ("female", "FEMALE")],
                        max_length=250,
                        null=True,
                    ),
                ),
                ("height", models.CharField(blank=True, max_length=250, null=True)),
                ("weight", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "special_comments",
                    models.TextField(blank=True, max_length=450, null=True),
                ),
                ("slug", models.SlugField(unique=True)),
                (
                    "pet_breed",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="breedname",
                        to="pet.petbreed",
                    ),
                ),
                (
                    "pet_type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="breedtype",
                        to="pet.pettype",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_name",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PetImage",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="Image ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, max_length=254, null=True, upload_to="images/"
                    ),
                ),
                (
                    "pet_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pet_images",
                        to="pet.petprofile",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="petbreed",
            name="pet_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pettype",
                to="pet.pettype",
            ),
        ),
    ]
