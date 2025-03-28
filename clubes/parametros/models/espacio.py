from django.db import models

from club.models.club import Club

class Espacio(models.Model):
    nombre = models.CharField(unique=True, max_length=50)
    descripcion = models.TextField(null=True,blank=True)
    apto_deporte = models.BooleanField(default=True, verbose_name="¿Uso deportivo?")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre}"