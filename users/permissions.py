from typing import override

from rest_framework.permissions import BasePermission


class IsRoleAdmin(BasePermission):
    @override
    def has_permission(self, request, view) -> bool:
        return request.user.is_admin()
