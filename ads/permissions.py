from typing import override

from rest_framework.permissions import BasePermission


class IsAdAuthor(BasePermission):
    @override
    def has_object_permission(self, request, view, ad) -> bool:
        return ad.author == request.user
