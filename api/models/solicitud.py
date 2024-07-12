from django.db import models


class Solicitud(models.Model):
    surtidor = models.IntegerField()
    gasolina = models.IntegerField()
