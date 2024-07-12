import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.constants import Constants
from api.models import Ruta, RutaDetalle
from api.models.solicitud import Solicitud
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
        ruta = ruta_detalle.ruta
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': request.headers.get('Authorization')
            }
            body = {
                'litros': ruta_detalle.litros,
                'surtidor': ruta_detalle.surtidor,
                'combustible': ruta_detalle.ruta.tipo_gasolina,
                'precio': ruta_detalle.ruta.precio_litro,
            }
            response = requests.post(
                Constants.SURTIDORES_URL + '/tanques' + '/cargar/',
                headers=headers,
                json=body
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return e.response.json()
        solicitud = Solicitud.objects.get(
            surtidor=ruta_detalle.surtidor,
            combustible=ruta_detalle.ruta.tipo_gasolina
        )
        solicitud.delete()
        higher_order = RutaDetalle.objects.filter(ruta=ruta.id).order_by('-orden').first()
        if higher_order.entregado:
            ruta.estado = False
            ruta.save()
            ruta.camion.estado = True
            ruta.camion.save()
        return Response({'detail': 'Entregado'}, status=status.HTTP_200_OK)