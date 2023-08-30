from django.contrib import admin
from pet.models import PetProfile, PetBreed, PetType, PetMediaFile, WeightMeasurement


class PetMediaFileInlineAdmin(admin.TabularInline):
    model = PetMediaFile


class PetProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pet_name",
        "pet_dob",
        "pet_gender",
        "primary_breed",
        "secondary_breed",
        "pet_type",
        "special_comments",
        "weight_measurement",
        "slug",
    )
    inlines = [PetMediaFileInlineAdmin]
    prepopulated_fields = {"slug": ("pet_name",)}

    def pet_type(self, obj):
        return obj.pettype.pet_type

    def pet_breed(self, obj):
        return obj.breed.pet_breed


class PetBreedAdmin(admin.TabularInline):
    model = PetBreed
    prepopulated_fields = {"slug": ("pet_breed",)}


class PetTypeAdmin(admin.ModelAdmin):
    inlines = [PetBreedAdmin]
    list_display = ("id", "pet_type", "slug")
    prepopulated_fields = {"slug": ("pet_type",)}


class PetMediaFileAdmin(admin.ModelAdmin):
    list_display = ("id", "pet_id", "file")


class PetWeightMeasurementAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")


admin.site.register(WeightMeasurement, PetWeightMeasurementAdmin)
admin.site.register(PetMediaFile, PetMediaFileAdmin)
admin.site.register(PetProfile, PetProfileAdmin)
admin.site.register(PetType, PetTypeAdmin)
