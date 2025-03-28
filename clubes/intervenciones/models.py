from django.db import models
from parametros.models.tipo_intervencion import TipoIntervencion
from parametros.models.estado import Estado
from disciplinas.models import Disciplina
from club.models.club import Club
from club.models.personal import Personal
from disciplinas.models import Disciplina
from socios.models import Socio

# Create your models here.

class Intervencion(models.Model):
    ''' Modelo para representar intervenciones'''
    tipo_intervencion = models.ForeignKey(TipoIntervencion, on_delete=models.CASCADE)
    referentes = models.ManyToManyField(Personal)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Disciplina")
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateField(verbose_name="Fecha")
    notas = models.TextField(null=True, blank=True)
    estado = models.ForeignKey(Estado, models.CASCADE, verbose_name="Estado")
    club = models.ForeignKey(Club, models.CASCADE, blank=False, null=False)
    def __str__(self):
        return f"{self.tipo_intervencion}"
    
    class Meta:
        # Definir que nombre mostrar para referencias al registro individual
        verbose_name = "Intervención"
        # Definir que nombre mostrar para referencias de lista de registros
        verbose_name_plural = "Intervenciones"
        # Definir ordenamiento
        ordering = ["tipo_intervencion"]
