from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Permite acceso de lectura a todos los usuarios,
    pero solo permite escritura a usuarios staff.
    """

    def has_permission(self, request, view):
        # Permitir solicitudes de lectura (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permitir escritura solo a usuarios staff
        return request.user and request.user.is_staff
