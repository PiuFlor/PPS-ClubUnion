from django.db import models

from parametros.models.ciudad import Ciudad
from club.models.club import Club

class Institucion(models.Model):
    nombre_institucion = models.CharField(max_length=200, unique=True)
    direccion = models.CharField(max_length=200)
    ciudad = models.ForeignKey(Ciudad, models.CASCADE)
    tipo_institucion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
 
    # Definir que nombre mostrar para el registro
    def __str__(self):
        return f"{self.nombre_institucion}"
    
    class Meta:
        # Definir que nombre mostrar para referencias al registro individual
        verbose_name = "Institución"
        # Definir que nombre mostrar para referencias de lista de registros
        verbose_name_plural = "Instituciones"
        # Definir ordenamiento
        ordering = ["nombre_institucion"]
        ordering = ["tipo_institucion"]