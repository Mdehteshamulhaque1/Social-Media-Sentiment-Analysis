from __future__ import annotations

from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    allowed_roles: tuple[str, ...] = ()

    def has_permission(self, request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if not self.allowed_roles:
            return True
        return getattr(request.user, 'role', None) in self.allowed_roles
