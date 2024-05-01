from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Позволяет только владельцу объекта выполнять операции."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
