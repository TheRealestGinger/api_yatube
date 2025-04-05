from rest_framework import permissions


class IsAuthenticatedOrOwner(permissions.BasePermission):
    """
    Позволяет редактировать объект только его владельцу.
    Остальным пользователям доступ только на чтение.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
