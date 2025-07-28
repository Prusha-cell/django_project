from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешение, позволяющее редактировать объект только владельцу.
    Чтение разрешено всем (если IsAuthenticatedOrReadOnly), а изменение — только owner.
    """

    def has_object_permission(self, request, view, obj):
        # Если метод безопасный (GET, HEAD, OPTIONS) — разрешаем
        if request.method in SAFE_METHODS:
            return True
        # Иначе — разрешено только если пользователь является владельцем
        return obj.owner == request.user
