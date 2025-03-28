from django.db import models

class TipoEvento(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=200, null=True)
 
    # Definir que nombre mostrar para el registro
    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        # Definir que nombre mostrar para referencias al registro individual
        verbose_name = "Tipo de evento"
        # Definir que nombre mostrar para referencias de lista de registros
        verbose_name_plural = "Tipos de eventos"
        # Definir ordenamiento
        ordering = ["nombre"]
        ordering = ["descripcion"]