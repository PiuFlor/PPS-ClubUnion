from django.db import models
from parametros.models.genero import Genero
from parametros.models.ciudad import Ciudad
from parametros.models.tipo_socio import TipoSocio
from parametros.models.estado import Estado
from parametros.models.grupo_sanguineo import GrupoSanguineo
from parametros.models.enfermedad_cronica import EnfermedadCronica
from parametros.models.enfermedad_infancia import EnfermedadInfancia
from parametros.models.vacuna import Vacuna
from parametros.models.dificultad import Dificultad
from parametros.models.alergia import Alergia
from parametros.models.medicacion import Medicacion
from parametros.models.escuela import Escuela
from parametros.models.tipo_documento import TipoDocumento

from club.models.club import Club
from clubes.validators import validar_cuit
from django.core.exceptions import ValidationError

from datetime import date

# Create your models here.

class Socio(models.Model):
   
    nro_socio = models.IntegerField(default=0, null=True, blank=True)
    nro_inscripcion = models.IntegerField(default=0, null=True, blank=True)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    nro_documento = models.CharField(max_length=15,unique=True)
    genero = models.ForeignKey(Genero,models.CASCADE)
    club = models.ForeignKey(Club,on_delete=models.CASCADE, default=1)
    grupo_familiar = models.CharField(max_length=20, null=True, blank=True)
    CUIL = models.CharField(max_length=11, unique=True, validators=[validar_cuit])
    ciudad = models.ForeignKey(Ciudad,models.CASCADE)
    direccion = models.CharField(max_length=250)
    nro_telefono = models.CharField(max_length=15)
    grupo_telegram = models.CharField(max_length=30, null=True, blank=True)
    email_socio = models.EmailField (max_length=254, unique=True, null=True, blank=True)
    usa_email = models.BooleanField(verbose_name="Usa email?")
    activo = models.BooleanField(default=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    fecha_egreso = models.DateField(null=True, blank=True)
    responsable = models.CharField(max_length=250,null=True, blank=True)
    tel_responsable = models.CharField(max_length=15,null=True, blank=True)
    email_responsable = models.EmailField (max_length=254,null=True, blank=True)
    tipo_socio = models.ForeignKey(TipoSocio, on_delete=models.CASCADE, null=True, blank=True)
    #datos salud
    cobertura = models.CharField(max_length=250, null=True, blank=True)
    nro_cobertura = models.CharField(max_length=20, null=True, blank=True)
    medico = models.CharField(max_length=250,null=True,blank=True)
    grupo_sanguineo = models.ForeignKey(GrupoSanguineo, models.CASCADE)
    peso = models.FloatField(verbose_name="Peso (Kg)")
    altura = models.FloatField(verbose_name= "Altura (Metros)")
    enfermedades_cronicas = models.ManyToManyField(EnfermedadCronica, blank=True)
    enfermedades_infancia = models.ManyToManyField(EnfermedadInfancia, blank=True)
    enfermedades_huesos = models.BooleanField(default=False)
    enfermedades_nerviosas = models.BooleanField(default=False)
    enfermedades_digestivas = models.BooleanField(default=False)
    vacunas = models.ManyToManyField(Vacuna, null=True, blank=True)
    dificultades = models.ManyToManyField(Dificultad, null=True, blank=True)
    alergias = models.ManyToManyField(Alergia, null=True, blank=True)
    medicaciones = models.ManyToManyField(Medicacion, null=True, blank=True)
     #datos educacion
    escuela = models.ForeignKey(Escuela,models.CASCADE,null=True, blank=True)
    año_escolar = models.IntegerField(null=True, blank=True)
    turno_escolar = models.CharField(max_length=10, null=True, blank=True)
    tipo_contacto_escolar = models.CharField(max_length=15, null=True, blank=True)
    nombre_contacto_escolar = models.CharField(max_length=20, null=True, blank=True)
    telefono_contacto_escolar = models.CharField(max_length=20, null=True, blank=True)
    email_contacto_escolar = models.EmailField (max_length=254, null=True,blank=True)

    @property
    def edad(self):
        """Calcula la edad basada en la fecha de nacimiento."""
        hoy = date.today()
        return (
            hoy.year - self.fecha_nacimiento.year - 
            ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        )
    
    def clean(self):
        # Verificar que la fecha de egreso no sea anterior a la de ingreso
        if self.fecha_egreso and self.fecha_egreso < self.fecha_ingreso:
            raise ValidationError({
                'fecha_egreso': 'La fecha de egreso no puede ser anterior a la fecha de ingreso.'
            })
    def __str__(self):
        return f"{self.apellido} {self.nombre}"
    
    class Meta:
        # Definir que nombre mostrar para referencias al registro individual
        verbose_name = "Socio"
        # Definir que nombre mostrar para referencias de lista de registros
        verbose_name_plural = "Socios"
        # Definir ordenamiento
        ordering = ["fecha_ingreso"]
