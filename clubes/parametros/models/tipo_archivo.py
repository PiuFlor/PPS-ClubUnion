from django.db import models

class TipoArchivo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
   
 
    # Definir que nombre mostrar para el registro
    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        # Definir que nombre mostrar para referencias al registro individual
        verbose_name = "Tipo de Archivo"
        # Definir que nombre mostrar para referencias de lista de registros
        verbose_name_plural = "Tipos de Archivos"
        # Definir ordenamiento
        ordering = ["nombre"]