from django.db import models


class Ruta(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    camion = models.ForeignKey(
        'Camion',
        on_delete=models.CASCADE,
        related_name='ruta_camion'
    )
    estado = models.BooleanField(default=True)
    litros = models.IntegerField()
    TIPO_GASOLINA = 0
    TIPO_DIESEL = 1
    TIPO_GAS = 2
    TIPO_CHOICES = [
        (TIPO_GASOLINA, 'Gasolina'),
        (TIPO_DIESEL, 'Diesel'),
        (TIPO_GAS, 'Gas'),
    ]
    tipo_gasolina = models.IntegerField(choices=TIPO_CHOICES)
    precio_litro = models.FloatField()
