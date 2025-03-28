from django.db import models
from socios.models import Socio

from parametros.models.tipo_evento import TipoEvento
from parametros.models.estado import Estado
from parametros.models.ciudad import Ciudad
from parametros.models.institucion import Institucion

from disciplinas.models import Disciplina, Categoria
from club.models.club import Club
from club.models.personal import Personal
from django.forms import ValidationError

class Evento(models.Model):
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE, verbose_name="Tipo_evento")
    nombre = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    lugar = models.CharField(max_length=200)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, verbose_name="Ciudad")
    disciplinas = models.ManyToManyField(Disciplina, blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, null=True, blank=True)
    categorias = models.ManyToManyField(Categoria, blank=True)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name="Estado")
    club = models.ForeignKey(Club, models.CASCADE, blank=False, null=False)
    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ["tipo_evento", "nombre"]
    
    def clean(self):
        if self.fecha_inicio and self.fecha_fin and self.fecha_inicio > self.fecha_fin:
            raise ValidationError({'fecha_inicio': 'La fecha de inicio no puede ser posterior a la fecha de finalización'})

class ParticipantesEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    socios = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name='socio_participantes')

    def __str__(self):
        return f"{self.evento}"

    class Meta:
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"
        ordering = ["evento"]

class ResponsableEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='evento_personal')
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='evento_responsable_personal')

    def __str__(self):
        return f"{self.personal}"

    class Meta:
        verbose_name_plural = "Responsables Institucionales"
        verbose_name = "Responsable Institucional"

class ResponsableDeportivoEvento(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='evento_deportivo')
    profesor = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='responsable_deportivo_evento')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE) 

    def __str__(self):
        return f"{self.profesor}"

    class Meta:
        verbose_name_plural = "Responsables Deportivos"
        verbose_name = "Responsable Deportivo"
