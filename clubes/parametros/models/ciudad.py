from django.db import models

# Create your models here.
class Ciudad(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    codigo_postal = models.IntegerField(blank=True, null=True)

    # Definir que nombre mostrar para el registro
    def __str__(self):
        return f"{self.nombre}"
    
    class Meta:
        # Definir que nombre mostrar para referencias al registro individual
        verbose_name = "Ciudad"
        # Definir que nombre mostrar para referencias de lista de registros
        verbose_name_plural = "Ciudades"
        # Definir ordenamiento
        ordering = ["nombre"]
