from typing import override

from rest_framework.permissions import BasePermission


class IsReviewAuthor(BasePermission):
    @override
    def has_object_permission(self, request, view, review) -> bool:
        return review.author == request.user
