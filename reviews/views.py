from typing import override

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ads.models import Ad
from users.permissions import IsRoleAdmin

from .models import Review
from .permissions import IsReviewAuthor
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_ad(self) -> Ad:
        if not hasattr(self, "_ad"):
            self._ad = get_object_or_404(Ad, pk=self.kwargs.get("ad_pk"))
        return self._ad

    @override
    def get_queryset(self):
        return super().get_queryset().filter(ad=self.get_ad())

    @override
    def get_permissions(self):
        permissions = [IsAuthenticated]
        if self.action in ["update", "partial_update", "destroy"]:
            permissions += [IsReviewAuthor | IsRoleAdmin]

        return [permission() for permission in permissions]

    @override
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, ad=self.get_ad())
