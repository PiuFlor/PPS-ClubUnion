from django.db import models

from club.models.club import Club
from club.models.personal import Personal
from disciplinas.models import Disciplina
from socios.models import Socio

# Create your models here.

ESTADOS_MOV = [
    ('P','Pendiente'),
    ('C','Procesada'),
    ]

class TipoArticulo(models.Model):
    ''' Modelo para representar los tipos de artículos'''

    nombre = models.CharField(max_length=200)
    imagen = models.ImageField()
    club = models.ForeignKey(Club, models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Tipos de Artículos"

class Articulo(models.Model):
    ''' Modelo para representar los artículos'''

    nombre = models.CharField(max_length=200)
    tipoArticulo = models.ForeignKey(TipoArticulo, models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, models.CASCADE, null=True, blank=True)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField()
    club = models.ForeignKey(Club, models.CASCADE, null=True, blank=True)
    precio = models.FloatField(default=0)
    costo = models.FloatField(default=0)
    destacado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name_plural = "Artículos"

class Entrega(models.Model):
    ''' Modelo para representar la entrega de articulos '''

    fecha = models.DateField(verbose_name='Fecha de Entrega')
    referencia = models.CharField(max_length=100, blank=True, null=True)
    personal = models.ForeignKey(Personal, models.CASCADE, related_name="fk_alm_per")
    socio = models.ForeignKey(Socio, models.CASCADE, related_name="fk_alm_soc", blank=True, null=True)
    estado = models.CharField(max_length=1, choices=ESTADOS_MOV, default='P')
    club = models.ForeignKey(Club, models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.fecha} - {self.personal} - {self.estado}"

    class Meta:
        verbose_name_plural = "Entregas de Artículos"

class DetalleEntrega(models.Model):
    ''' Modelo para representar los items de la entrega de los artículos '''
    entrega = models.ForeignKey(Entrega, models.CASCADE, related_name="fk_det_ent")
    articulo = models.ForeignKey(Articulo, models.CASCADE, related_name="fk_det_ent_art")
    cantidad = models.IntegerField()
    club = models.ForeignKey(Club, models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.articulo} - {self.cantidad}"

    class Meta:
        verbose_name_plural = "Detalle de Entregas de Artículos"

class Recepcion(models.Model):
    ''' Modelo para representar la recepcion de articulos '''

    fecha = models.DateField()
    referencia = models.CharField(max_length=100, blank=True, null=True)
    personal = models.ForeignKey(Personal, models.CASCADE, related_name="fk_rec_alm_per")
    estado = models.CharField('Estado', max_length=1, choices=ESTADOS_MOV, default='P')
    club = models.ForeignKey(Club, models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.fecha} - {self.personal} - {self.estado}"

    class Meta:
        verbose_name_plural = "Recepcion de Artículos"

class DetalleRecepcion(models.Model):
    ''' Modelo para representar los items de la recepcion de los artículos '''
    recepcion = models.ForeignKey(Recepcion, models.CASCADE, related_name="fk_det_rec")
    articulo = models.ForeignKey(Articulo, models.CASCADE, related_name="fk_det_rec_art")
    cantidad = models.IntegerField()
    club = models.ForeignKey(Club, models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.articulo} - {self.cantidad}"

    class Meta:
        verbose_name_plural = "Detalle de Recepcion de Artículos"

