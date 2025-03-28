from django.db import models
from club.models.club import Club

class Estado(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    club = models.ForeignKey(Club, models.CASCADE)
   
    # Definir que nombre mostrar para el registro
    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        # Definir que nombre mostrar para referencias al registro individual
        verbose_name = "Estado"
        # Definir que nombre mostrar para referencias de lista de registros
        verbose_name_plural = "Estados"
        # Definir ordenamiento
        ordering = ["nombre"]