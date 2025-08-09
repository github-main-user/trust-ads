from typing import override

from rest_framework.permissions import BasePermission


class IsReviewAuthor(BasePermission):
    """Validates if current user is author of the review."""

    @override
    def has_object_permission(self, request, view, review) -> bool:
        return review.author == request.user
