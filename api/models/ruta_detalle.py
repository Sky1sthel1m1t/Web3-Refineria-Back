from django.db import models


class RutaDetalle(models.Model):
    ruta = models.ForeignKey(
        'Ruta',
        on_delete=models.CASCADE,
        related_name='ruta_detalle_ruta'
    )
    surtidor = models.IntegerField()
    orden = models.IntegerField()
    litros = models.IntegerField()
    entregado = models.BooleanField(default=False)