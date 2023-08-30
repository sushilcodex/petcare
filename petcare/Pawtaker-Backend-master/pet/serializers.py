import uuid
from rest_framework import serializers
from pet.models import PetProfile, PetType, PetBreed, PetMediaFile, WeightMeasurement


class PetProfileMediaCreateSerializer(serializers.Serializer):
    file = serializers.ListField(
        child=serializers.FileField(
            max_length=100000, allow_empty_file=False, use_url=False
        )
    )


class PetProfileMediaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetMediaFile
        fields = ["id", "featured", "file"]
        extra_kwargs = {"id": {"read_only": False}, "file": {"read_only": True}}


class PetProfileCreateUpdateSerializer(serializers.ModelSerializer):
    images = PetProfileMediaListSerializer(many=True, write_only=True)

    class Meta:
        model = PetProfile
        fields = (
            "id",
            "pet_name",
            "pet_dob",
            "pet_gender",
            "primary_breed",
            "secondary_breed",
            "pet_type",
            "weight_measurement",
            "weight",
            "special_comments",
            "images",
        )

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        internal_value.update(
            {
                "user": self.context.get("user"),
            }
        )
        return internal_value

    def create(self, validated_data):
        images = validated_data.pop("images")
        obj = self.Meta.model.objects.create(**validated_data)
        for image_data in images:
            pet_media = PetMediaFile.objects.get(id=image_data.get("id"))
            pet_media.pet_id = obj
            pet_media.featured = image_data.get("featured")
            pet_media.save()
        return obj

    def update(self, instance, validated_data):
        images = validated_data.pop("images")
        instance = super().update(instance, validated_data)
        for image_data in images:
            pet_media = PetMediaFile.objects.get(id=image_data.get("id"))
            pet_media.pet_id = instance
            pet_media.featured = image_data.get("featured")
            pet_media.save()
        return instance


class PetProfileDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PetProfile
        fields = (
            "id",
            "pet_name",
            "weight",
            "pet_gender",
            "primary_breed",
            "secondary_breed",
            "weight_measurement",
            "pet_type",
            "media_files",
            "pet_dob",
            "special_comments",
        )
        depth = 1


class PetProfileListSerializer(serializers.ModelSerializer):
    media_url = serializers.SerializerMethodField("get_media_url")
    pet_gender = serializers.SerializerMethodField("get_pet_gender")

    class Meta:
        model = PetProfile
        fields = (
            "id",
            "pet_name",
            "pet_gender",
            "primary_breed",
            "secondary_breed",
            "pet_type",
            "media_url",
        )
        depth = 1

    def get_media_url(self, obj) -> str:
        request = self.context.get("request")
        media_querset = PetMediaFile.objects.filter(pet_id=obj.id, featured=True)
        for media in media_querset:
            media_obj = media.file.url
            media_obj = request.build_absolute_uri(media_obj)
            return media_obj

    def get_pet_gender(self, obj) -> str:
        try:
            return obj.pet_gender.upper()
        except:
            return None


class FavouritePetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetProfile
        fields = "__all__"


class LikePetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetProfile
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetMediaFile
        fields = "__all__"


class PetPostSerializer(serializers.ModelSerializer):
    petprofile = ImageSerializer(many=True)

    class Meta:
        model = PetProfile
        fields = ("pet_name", "pet_breed", "petprofile")


class UpdatePetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetProfile
        fields = (
            "pet_name",
            "pet_dob",
            "pet_gender",
            "pet_type",
            "primary_breed",
            "secondary_breed",
            "special_comments",
        )


class PetTypeListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetType
        fields = ("id", "pet_type")


class WeightMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightMeasurement
        fields = ("id", "name")


class PetBreedListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetBreed
        fields = ("id", "pet_breed")


class PetMediaDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.CharField())
