from datetime import date, datetime
import re
from django.db import models
from django.forms import ValidationError
from club.models.club import Club
from club.models.personal import Personal
from parametros.models.espacio import Espacio
from socios.models import Socio

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField



OPCIONES_DIAS = [
    ('LU', 'Lunes'),
    ('MA', 'Martes'),
    ('MI', 'Miércoles'),
    ('JU', 'Jueves'),
    ('VI', 'Viernes'),
    ('SA', 'Sábado'),
    ('DO', 'Domingo'),
]

COLORES = [
    ('#288313', 'Verde'),
    ('#ff5733', 'Naranja'),
    ('#67e1e3', 'Celeste'),
    ('#f23727', 'Rojo'),
    ('#000000', 'Negro'),
    ('#e8ea39', 'Amarillo'),
    ('#d83fd4', 'Violeta'),
]

class Disciplina (models.Model):
    nombre = models.CharField(max_length=50, unique=True, blank=False, null=False, verbose_name="Disciplina")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=False, null=False) 
    estado = models.BooleanField(default=True, verbose_name="¿Está activo?") 
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Caja")
    color = models.CharField(max_length=7, choices=COLORES, default="#288313")
    imagen = models.ImageField(blank=False, null=False, default="logo.png", verbose_name="Ícono")
    info = RichTextUploadingField(null=True, blank=True)
    imagenContenido1 = models.ImageField(blank=False, null=False, default="logo.png", verbose_name="Imagen de contenido 1")
    imagenContenido2 = models.ImageField(blank=False, null=False, default="logo.png", verbose_name="Imagen de contenido 2")
    imagenContenido3 = models.ImageField(blank=False, null=False, default="logo.png", verbose_name="Imagen de contenido 3")
    def __str__(self):
            return f"{self.nombre}"

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Disciplinas"
        verbose_name = "Disciplina"
    
    def getCategorias(self):
        all_cat = Categoria.objects.filter(disciplina=self)
        return all_cat

    def getSocios(self):
        all_cat = Categoria.objects.filter(disciplina=self)

        for cat in all_cat:

            all_soc = SocioCategoria.objects.filter(categoria=cat)

            return all_soc


class Categoria(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False, verbose_name="Categoría")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, verbose_name="Disciplina")
    anio = models.IntegerField(default=date.today().year, verbose_name="Año")
    estado = models.BooleanField(default=True, verbose_name="¿Está activo?")
    edad_desde = models.PositiveIntegerField()
    edad_hasta = models.PositiveIntegerField()
    grupo_telegram = models.CharField(max_length=30, null=True, blank=True)
    club = models.ForeignKey(Club, models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.anio} - {self.disciplina.nombre}"
     
    def clean(self):
        super().clean()
        current_year = date.today().year
        if not (current_year <= self.anio <= current_year + 1):
            raise ValidationError({'anio': f"El año debe ser {current_year} o {current_year + 1}."})

    def getSocios(self):
        all_soc = SocioCategoria.objects.filter(categoria=self)
        return all_soc
    
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = "Categorias"
        verbose_name = "Categoria"
        constraints = [
            models.UniqueConstraint(fields=['nombre', 'disciplina', 'anio'], 
                name='unique_categoria_disciplina_anio')
        ]

class Horario(models.Model):
    cancha = models.ForeignKey(Espacio, on_delete=models.CASCADE, limit_choices_to={'apto_deporte': True}, verbose_name='Espacio')
    dia_semana = models.CharField(max_length=255, blank=True, null=True, choices=OPCIONES_DIAS, verbose_name='Día de la Semana')
    inicio = models.TimeField(help_text="Formato requerido: HH:MM (ejemplo: 17:30)")
    fin = models.TimeField(help_text="Formato requerido: HH:MM (ejemplo: 18:30)")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoria')
    club = models.ForeignKey(Club, models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.categoria.nombre} / {self.categoria.anio} - {self.cancha}"

    def clean(self):
        super().clean()
        
        formato_hora = re.compile(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
        
        if not self.inicio or not self.fin:
            raise ValidationError("Los campos de inicio y fin son obligatorios - El formato de hora debe ser HH:MM")
        
        if self.inicio and not formato_hora.match(str(self.inicio.strftime('%H:%M'))):
            raise ValidationError({'inicio': "El formato de hora debe ser HH:MM (ejemplo: 17:30)"})
        
        if self.fin and not formato_hora.match(str(self.fin.strftime('%H:%M'))):
            raise ValidationError({'fin': "El formato de hora debe ser HH:MM (ejemplo: 17:30)"})

        if self.inicio and self.fin and self.inicio >= self.fin:
            raise ValidationError({'fin': "La hora de fin debe ser mayor a la hora de inicio."})

        if self.inicio and self.fin and self.dia_semana and self.cancha:
            
            solapamientos = Horario.objects.filter(
                cancha=self.cancha,
                dia_semana=self.dia_semana
            ).exclude(pk=self.pk)

            for horario in solapamientos:
                if (
                    (self.inicio >= horario.inicio and self.inicio < horario.fin) or
                    (self.fin > horario.inicio and self.fin <= horario.fin) or
                    (self.inicio <= horario.inicio and self.fin >= horario.fin)
                ):
                    raise ValidationError(
                        f"Este horario se solapa con otro existente: {horario.inicio.strftime('%H:%M')} - {horario.fin.strftime('%H:%M')}"
                    )

    class Meta:
        ordering = ['dia_semana', 'inicio']
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"


class ProfesorCategoria(models.Model):
    profesor = models.ForeignKey(Personal, on_delete=models.CASCADE, default=1, related_name="Profesor")#limitar q solo sea personal de tipo profesor
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="Categoria_profesor")
    estado = models.BooleanField(default=True, verbose_name="¿Está activo?")
    club = models.ForeignKey(Club, models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.profesor.apellido}  {self.profesor.nombre} - {self.categoria} - {self.categoria.disciplina}" 
    
    class Meta:
        verbose_name_plural = "Profesores Categoria"
        verbose_name = "Profesor Categoria" 
    def clean(self):
        super().clean()
        if ProfesorCategoria.objects.filter(categoria=self.categoria, profesor=self.profesor).exclude(id=self.id).exists():
            raise ValidationError('El profesor ya tiene asignada esa categoría')


class SocioCategoria(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, default=1, related_name="socio")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="Categoria_socio")
    estado = models.BooleanField(default=True, verbose_name="¿Está activo?")
    club = models.ForeignKey(Club, models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.socio}-{self.categoria}-{self.socio.fecha_ingreso}"
    class Meta:
        verbose_name_plural = "Socios Categoria"
        verbose_name = "Socio Categoria" 
        unique_together = ('socio', 'categoria') 
    
"""     def clean(self):
        super().clean()
        if SocioCategoria.objects.filter(categoria=self.categoria, socio=self.socio).exclude(id=self.id).exists():
            raise ValidationError('El socio ya tiene asignada esa categoría')
 """

