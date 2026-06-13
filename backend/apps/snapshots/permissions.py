from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return getattr(obj, 'user', None) == request.user
