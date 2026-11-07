
from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    message = "Admin permission is required."

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_admin
        )
