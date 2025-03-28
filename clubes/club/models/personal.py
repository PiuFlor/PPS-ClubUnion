from django.db import models
from club.models.club import Club
from parametros.models.ciudad import Ciudad
from parametros.models.genero import Genero
from parametros.models.tipo_documento import TipoDocumento
from parametros.models.tipo_personal import TipoPersonal
from clubes.validators import validar_cuit

class Personal(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    nro_documento = models.CharField(max_length=20, unique= True)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    CUIL = models.CharField(max_length=11, unique=True, validators=[validar_cuit])
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=100)
    nro_telefono = models.CharField(max_length=30)
    email = models.EmailField(max_length=255, unique= True)
    estado = models.BooleanField(verbose_name="Activo")
    fecha_ingreso = models.DateField()
    fecha_egreso = models.DateField(blank= True, null= True)
    tipo_personal = models.ForeignKey(TipoPersonal, on_delete=models.CASCADE)
    descripcion_tareas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Personal"
        verbose_name = "Personal"