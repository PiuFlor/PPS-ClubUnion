from django.db import models

from clubes.validators import validar_cuit
from parametros.models.ciudad import Ciudad

class Club(models.Model):
    razon_social = models.CharField(max_length=255, unique=True)
    CUIT = models.CharField(max_length=11, unique=True, validators=[validar_cuit])
    direccion = models.CharField(max_length=100)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
    grupo_telegram = models.CharField(max_length=30, null=True, blank=True)
    secuencia_socio = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.razon_social}"
    
    class Meta:
        ordering = ["razon_social"]
        verbose_name_plural = "Clubes"
        verbose_name = "Club"