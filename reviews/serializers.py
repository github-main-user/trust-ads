from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id", "text", "author", "ad", "created_at")
        read_only_fields = ("author", "ad", "created_at")
