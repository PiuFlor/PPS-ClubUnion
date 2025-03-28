from django.db import models

from club.models.club import Club
from parametros.models.tipo_archivo import TipoArchivo


class DocumentoVinculado(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    tipo_documento = models.ForeignKey(TipoArchivo, on_delete=models.CASCADE)
    detalle = models.TextField(null=True, blank=True)
    archivo = models.FileField(upload_to='upload/')

    def __str__(self):
        return f"{self.tipo_documento}"
    
    class Meta:
        ordering = ['tipo_documento']
        verbose_name_plural = "Documentos"
        verbose_name = "Documento"