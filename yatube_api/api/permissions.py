from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Позволяет только владельцу объекта выполнять операции."""

    def has_object_permission(self, request, view, user_data):
        return (
            request.method in permissions.SAFE_METHODS
            or user_data.author == request.user
        )
