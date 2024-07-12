from rest_framework.permissions import BasePermission


class IsChofer(BasePermission):
    message = 'No tienes permisos para hacer esto'

    def has_permission(self, request, view):
        token = request.auth
        role_id = token['role']
        return role_id == 5


class IsAdministradorRefineria(BasePermission):
    message = 'No tienes permisos para hacer esto'

    def has_permission(self, request, view):
        token = request.auth
        role_id = token['role']
        return role_id == 2


class IsAdministradorSurtidor(BasePermission):
    message = 'No tienes permisos para hacer esto'

    def has_permission(self, request, view):
        token = request.auth
        role_id = token['role']
        return role_id == 1
