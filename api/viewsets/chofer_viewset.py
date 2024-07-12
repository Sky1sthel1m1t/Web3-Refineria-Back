from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Ruta, RutaDetalle
from api.permissions import IsChofer
from api.serializers import RutaWithDetalleSerializer


class ChoferViewSet(viewsets.GenericViewSet):
    permission_classes = [
        IsChofer
    ]

    @action(detail=False, methods=['get'], url_path='ruta')
    def get_ruta_by_chofer(self, request):
        chofer = request.user
        queryset = Ruta.objects.filter(
            camion__chofer=chofer,
            estado=True
        ).first()
        if queryset is None:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        serializer = RutaWithDetalleSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='entregar')
    def entregar(self, request):
        ruta_detalle_id = request.data.get('id')
        ruta_detalle = RutaDetalle.objects.get(pk=ruta_detalle_id)
        ruta_detalle.entregado = True
        ruta_detalle.save()
        ruta_id = ruta_detalle.ruta.id
        higher_order = RutaDetalle.objects.filter(ruta=ruta_id).order_by('-orden').first()
        if higher_order.entregado:
            ruta = Ruta.objects.get(pk=ruta_id)
            ruta.estado = False
            ruta.save()
            camion = ruta.camion
            camion.estado = True
            camion.save()
        return Response({'detail': 'Entregado'}, status=status.HTTP_200_OK)