from django.db import models
from accounts.models import CustomUser
from django.utils.text import slugify
import string
import random
import uuid
from pet.constants import MAX_RAND_STR_LENGTH


class WeightMeasurement(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.name}"


class PetType(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        verbose_name="Pettype ID",
        default=uuid.uuid4,
        unique=True,
    )
    pet_type = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.pet_type)
        super(PetType, self).save()

    def __str__(self):
        return self.pet_type


class PetBreed(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Breed ID",
        unique=True,
    )
    pet_breed = models.CharField(max_length=255, null=True, blank=True)
    pet_type = models.ForeignKey(
        PetType, on_delete=models.CASCADE, related_name="pettype"
    )
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.pet_breed)
        super(PetBreed, self).save()

    def __str__(self):
        return self.pet_breed


class PetGenderChoices(models.TextChoices):
    MALE = "male", "MALE"
    FEMALE = "female", "FEMALE"


class PetProfile(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="pet ID",
        unique=True,
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_name"
    )
    pet_type = models.ForeignKey(
        PetType,
        null=True,
        on_delete=models.CASCADE,
        related_name="breedtype",
        blank=True,
    )
    primary_breed = models.ForeignKey(
        PetBreed,
        null=True,
        on_delete=models.CASCADE,
        related_name="primary",
        blank=True,
    )
    secondary_breed = models.ForeignKey(
        PetBreed,
        null=True,
        on_delete=models.CASCADE,
        related_name="secondary",
        blank=True,
    )
    pet_name = models.CharField(max_length=250)
    pet_dob = models.DateField(null=True, blank=True)
    pet_gender = models.CharField(
        max_length=250, null=True, blank=True, choices=PetGenderChoices.choices
    )
    weight_measurement = models.ForeignKey(
        WeightMeasurement, blank=True, null=True, on_delete=models.SET_NULL
    )
    weight = models.FloatField(max_length=250, null=True, blank=True)
    special_comments = models.TextField(max_length=450, null=True, blank=True)
    number_of_nails = models.IntegerField(blank=True, default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        super(PetProfile, self).save()
        if not self.slug:
            str_range = MAX_RAND_STR_LENGTH
            res = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=str_range)
            )
            self.slug = slugify(self.pet_name) + "-" + str(res)
            super(PetProfile, self).save()

    def __str__(self):
        return self.pet_name


class PetMediaFile(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name="File ID",
        unique=True,
    )
    pet_id = models.ForeignKey(
        PetProfile,
        on_delete=models.CASCADE,
        related_name="media_files",
        blank=True,
        null=True,
    )
    file = models.FileField(
        upload_to="pet_media/", max_length=254, null=True, blank=True
    )
    featured = models.BooleanField(default=False)
