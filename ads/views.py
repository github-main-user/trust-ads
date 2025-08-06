from typing import override

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.permissions import IsRoleAdmin

from .models import Ad
from .pagination import AdPagination
from .permissions import IsAdAuthor
from .serializers import AdSerializer


@extend_schema(tags=["ads"])
@extend_schema_view(
    list=extend_schema(
        summary="List all ads",
        description="Retrieves a list of all ads. Supports search by title.",
    ),
    retrieve=extend_schema(
        summary="Retrieve an ad", description="Retrieves the details of a specific ad."
    ),
    create=extend_schema(summary="Create a new ad", description="Creates a new ad."),
    update=extend_schema(summary="Update an ad", description="Updates an existing ad."),
    partial_update=extend_schema(
        summary="Partially update an ad",
        description="Partially updates an existing ad.",
    ),
    destroy=extend_schema(summary="Delete an ad", description="Deletes an ad."),
)
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination

    filter_backends = (filters.SearchFilter,)
    search_fields = ("title",)

    @override
    def get_permissions(self):
        match self.action:
            case "list":
                permissions = [AllowAny]
            case "create" | "retrieve":
                permissions = [IsAuthenticated]
            case "update" | "partial_update" | "destroy":
                permissions = [IsAuthenticated, IsAdAuthor | IsRoleAdmin]
            case _:
                permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    @override
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
