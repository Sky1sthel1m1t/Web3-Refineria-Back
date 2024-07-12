from django.db import models


class Camion(models.Model):
    placa = models.CharField(max_length=10)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    chofer = models.IntegerField()
