from typing import override

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.permissions import IsRoleAdmin

from .models import Ad
from .pagination import AdPagination
from .permissions import IsAdAuthor
from .serializers import AdSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination

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
