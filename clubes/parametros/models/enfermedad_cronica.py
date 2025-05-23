from django.db import models

class EnfermedadCronica(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    
   
    # Definir que nombre mostrar para el registro
    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        # Definir que nombre mostrar para referencias al registro individual
        verbose_name = "Enfermedad crónica"
        # Definir que nombre mostrar para referencias de lista de registros
        verbose_name_plural = "Enfermedades crónicas"
        # Definir ordenamiento
        ordering = ["nombre"]