from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Ruta, RutaDetalle
from api.permissions import IsAdministradorRefineria, IsChofer
from api.serializers import RutaSerializer, RutaWithDetalleSerializer, RutaDetalleSerializer


class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
    permission_classes = [
        IsAdministradorRefineria
    ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = RutaWithDetalleSerializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()
        serializer.instance.camion.estado = False
        serializer.instance.camion.save()

    @action(detail=True, methods=['post'], url_path='detalle')
    def add_detalle(self, request, pk=None):
        ruta = self.get_object()
        orden = request.data.get('orden')
        litros = request.data.get('litros')
        surtidor = request.data.get('surtidor')

        ruta_detalle = {
            'orden': orden,
            'litros': litros,
            'surtidor': surtidor,
            'ruta_id': ruta.id
        }
        ruta_detalle_serializer = RutaDetalleSerializer(
            data=ruta_detalle
        )
        ruta_detalle_serializer.is_valid(raise_exception=True)
        ruta_detalle_serializer.save()
        return Response(ruta_detalle_serializer.data, status=status.HTTP_201_CREATED)
