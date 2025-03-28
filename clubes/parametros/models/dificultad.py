from django.db import models

class Dificultad(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(null=True, blank=True)
 
   # Definir que nombre mostrar para el registro
    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        # Definir que nombre mostrar para referencias al registro individual
        verbose_name = "Dificultad"
        # Definir que nombre mostrar para referencias de lista de registros
        verbose_name_plural = "Dificultades"
        # Definir ordenamiento
        ordering = ["nombre"]