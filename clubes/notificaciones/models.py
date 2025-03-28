from django.db import models

from club.models.club import Club
from disciplinas.models import Categoria, Disciplina

# Create your models here.

MEDIO_ENVIO = [
    ('T', 'Telegram'),
    ('E', 'Email'),
    ('A', 'Ambos'),
]

ESTADOS_ENVIO = [
    ('P', 'Pendiente'),
    ('E', 'Enviado'),
    ('C', 'Cancelado'),
]

class Mensaje(models.Model):
    referencia = models.CharField(max_length=200, unique=True)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    socios_activos = models.BooleanField(default=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Disciplina")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Categoria")
    fecha = models.DateField(null=True, blank=True)
    texto = models.TextField()
    medio = models.CharField(max_length=1, choices=MEDIO_ENVIO, default='E')
    estado = models.CharField(max_length=1, choices=ESTADOS_ENVIO, default='P', verbose_name="Estado")
    archivo = models.FileField(upload_to='upload/', null=True, blank=True)

    def __str__(self):
        return f"{self.referencia} - {self.fecha}"
    
    class Meta:
        ordering = ['fecha']
        verbose_name_plural = "Mensajes"
        verbose_name = "Mensaje"