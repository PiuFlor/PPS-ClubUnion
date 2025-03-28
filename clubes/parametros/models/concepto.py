from django.db import models
from club.models.club import Club

class Concepto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, blank=True)
   
 
    # Definir que nombre mostrar para el registro
    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        # Definir que nombre mostrar para referencias al registro individual
        verbose_name = "Concepto"
        # Definir que nombre mostrar para referencias de lista de registros
        verbose_name_plural = "Conceptos"
        # Definir ordenamiento
        ordering = ["nombre"]