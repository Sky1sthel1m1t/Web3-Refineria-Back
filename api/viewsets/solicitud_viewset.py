from rest_framework import viewsets

from api.models.solicitud import Solicitud
from api.permissions.permissions import IsAdministradorSurtidor
from api.serializers import SolicitudSerializer


class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    permission_classes = [
        IsAdministradorSurtidor
    ]