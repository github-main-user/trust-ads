from rest_framework import serializers

from .models import Ad


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ("id", "title", "price", "description", "author", "created_at")
        read_only_fields = ("author", "created_at")
