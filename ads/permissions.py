from typing import override

from rest_framework.permissions import BasePermission


class IsAdAuthor(BasePermission):
    """Validates if current user the author of the ad."""

    @override
    def has_object_permission(self, request, view, ad) -> bool:
        return ad.author == request.user
