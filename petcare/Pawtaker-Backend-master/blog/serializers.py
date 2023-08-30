# serializers.py
from rest_framework import serializers
from .models import Blog


class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "excerpt",
            "description",
            "category",
            "image",
            "is_draft",
            "published_date",
            "publisher_name",
        ]
