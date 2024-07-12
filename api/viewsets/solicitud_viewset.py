from rest_framework import viewsets

from api.models.solicitud import Solicitud
from api.permissions.permissions import IsAdministradorSurtidor, IsAdministradorRefineria
from api.serializers import SolicitudSerializer


class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    permission_classes = [
        IsAdministradorRefineria
    ]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdministradorSurtidor]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]