from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from pet.serializers import *
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from pet.models import *
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework import generics
from accounts.models import CustomUser


@extend_schema(tags=["Pet Media APIs"])
class PetProfileMediaViews(viewsets.ModelViewSet):
    serializer_class = PetProfileMediaCreateSerializer
    queryset = PetMediaFile.objects.all()
    http_method_names = ["post", "delete"]
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        files = serializer.validated_data.get("file")
        media_objs = []
        for file in files:
            pet_obj = PetMediaFile()
            pet_obj.file = file
            pet_obj.featured = False
            media_objs.append(pet_obj)
        objs = PetMediaFile.objects.bulk_create(media_objs)
        list_serializer_obj = PetProfileMediaListSerializer(
            objs, many=True, context={"request": request}
        )
        headers = self.get_success_headers(list_serializer_obj.data)
        return Response(
            list_serializer_obj.data, status=status.HTTP_201_CREATED, headers=headers
        )


@extend_schema(tags=["Pet Profile Apis"])
class PetProfileViews(viewsets.ModelViewSet):
    serializer_class = PetProfileCreateUpdateSerializer
    list_serializer_class = PetProfileListSerializer
    detail_serializer_class = PetProfileDetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["post", "delete", "get", "patch"]
    lookup_field = "id"
    queryset = PetProfile.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return self.list_serializer_class
        elif self.action == "retrieve":
            return self.detail_serializer_class
        else:
            return self.serializer_class

    def get_queryset(self):
        user = self.request.user
        return PetProfile.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        context["request"] = self.request
        return context

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Pet profile deleted successfully"}, status=status.HTTP_200_OK
        )


@extend_schema(tags=["Other Pet Related Api's"])
class FavouritePetView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FavouritePetSerializer
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        uuid = request.user.id
        user_obj = CustomUser.objects
        try:
            pet_obj = PetProfile.objects.get(id=kwargs["uuid"])
        except:
            return Response(
                {"message": "Pet id is not valid "},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = CustomUser.favourite_pet.through.objects.get(
                petprofile_id=pet_obj.id, customuser_id__id=uuid
            )
            if user:
                user.delete()
                return Response(
                    {"message": "Pet marked as unfavourite"},
                    status=status.HTTP_200_OK,
                )

        except:
            user = user_obj.get(id=uuid)
            if user:
                user.favourite_pet.add(pet_obj.id)
                user.save()
                return Response(
                    {"message": "Pet marked as favourite"},
                    status=status.HTTP_200_OK,
                )


@extend_schema(tags=["Other Pet Related Api's"])
class FavouritePetListing(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FavouritePetSerializer
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        uuid = request.user.id
        pet_id = CustomUser.favourite_pet.through.objects.filter(
            customuser_id__id=uuid
        ).values_list("petprofile_id", flat=True)
        pet_obj = PetProfile.objects.filter(id__in=pet_id)
        serializer_data = FavouritePetSerializer(pet_obj, many=True).data
        return Response(data=serializer_data, status=status.HTTP_200_OK)


@extend_schema(tags=["Other Pet Related Api's"])
class LikePetView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LikePetSerializer

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        uuid = request.user.id
        user_obj = CustomUser.objects
        try:
            pet_obj = PetProfile.objects.get(id=kwargs["uuid"])
        except:
            return Response(
                {"message": "Pet id is not valid "},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = CustomUser.like.through.objects.get(
                petprofile_id=pet_obj.id, customuser_id__id=uuid
            )
            if user:
                user.delete()
                return Response(
                    {"message": "Un-liked"},
                    status=status.HTTP_200_OK,
                )

        except:
            user = user_obj.get(userId=uuid)
            if user:
                user.like.add(pet_obj.id)
                user.save()
                return Response(
                    {"message": "Liked"},
                    status=status.HTTP_200_OK,
                )


@extend_schema(tags=["Other Pet Related Api's"])
class LikedPetListing(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = LikePetSerializer
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        uuid = request.user.id
        pet_id = CustomUser.like.through.objects.filter(
            customuser_id__id=uuid
        ).values_list("petprofile_id", flat=True)
        pet_obj = PetProfile.objects.filter(id__in=pet_id)
        serializer_data = LikePetSerializer(pet_obj, many=True).data
        return Response(data=serializer_data, status=status.HTTP_200_OK)


@extend_schema(tags=["Other Pet Related Api's"])
class PetTypeListing(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PetTypeListingSerializer
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        pet_types = PetType.objects.all()
        weight_measurements = WeightMeasurement.objects.all()

        pet_type_serializer = self.serializer_class(pet_types, many=True)
        weight_measurement_serializer = WeightMeasurementSerializer(
            weight_measurements, many=True
        )

        response_data = {
            "pet_types": pet_type_serializer.data,
            "weight_measurements": weight_measurement_serializer.data,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)


@extend_schema(tags=["Other Pet Related Api's"])
class PetBreedListing(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PetBreedListingSerializer
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        pettype = str(kwargs["uuid"])
        type_breeds = PetBreed.objects.filter(pet_type__id=pettype)
        serializers_data = PetBreedListingSerializer(type_breeds, many=True).data
        return Response(data=serializers_data, status=status.HTTP_200_OK)
