from rest_framework import viewsets

from api.models import Camion
from api.permissions import IsAdministradorRefineria
from api.serializers import CamionSerializer


class CamionViewSet(viewsets.ModelViewSet):
    queryset = Camion.objects.all()
    serializer_class = CamionSerializer
    permission_classes = [
        IsAdministradorRefineria
    ]
