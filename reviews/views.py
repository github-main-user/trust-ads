from typing import override

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ads.models import Ad
from users.permissions import IsRoleAdmin

from .models import Review
from .permissions import IsReviewAuthor
from .serializers import ReviewSerializer


@extend_schema(tags=["reviews"])
@extend_schema_view(
    list=extend_schema(
        summary="List all reviews", description="Retrieves a list of all reviews."
    ),
    retrieve=extend_schema(
        summary="Retrieve a review",
        description="Retrieves the details of a specific review.",
    ),
    create=extend_schema(
        summary="Create a new review", description="Creates a new review."
    ),
    update=extend_schema(
        summary="Update a review", description="Updates an existing review."
    ),
    partial_update=extend_schema(
        summary="Partially update a review",
        description="Partially updates an existing review.",
    ),
    destroy=extend_schema(summary="Delete a review", description="Deletes a review."),
)
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
