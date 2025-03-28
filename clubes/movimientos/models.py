from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from club.models.club import Club
from club.models.personal import Personal
from parametros.models.concepto import Concepto
from disciplinas.models import Disciplina
from eventos.models import Evento

# Create your models here.
class Ingreso(models.Model):
    fecha = models.DateField()
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    responsable = models.ForeignKey(Personal, on_delete=models.CASCADE, null = True, blank= True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True, blank=True, related_name='evento_ingresos')
    detalles = models.TextField(null = True, blank= True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, models.CASCADE, blank=False, null=False)

    def clean(self):
        # Validar que el monto sea positivo
        if self.monto <= 0:
            raise ValidationError("El monto del ingreso debe ser mayor a 0.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.concepto} - {self.fecha}"


    class Meta:
        verbose_name_plural = "Ingresos de caja"
        verbose_name = "Ingreso de caja" 


class Egreso(models.Model):
    fecha = models.DateField()
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    responsable = models.ForeignKey(Personal, on_delete=models.CASCADE, null = True, blank= True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True, blank=True, related_name='evento_egresos')
    detalles = models.TextField(null = True, blank= True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, models.CASCADE, blank=False, null=False)

    def clean(self):
         # Validar que la fecha no sea nula antes de compararla
        if self.fecha:
            if self.fecha > now().date():
                raise ValidationError("La fecha del egreso no puede ser posterior a hoy.")
        # Validar que el monto sea positivo
        if self.monto <= 0:
            raise ValidationError("El monto del egreso debe ser mayor a 0.")
        

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    
    
    def __str__(self):
        return f"{self.concepto} - {self.fecha}"
    
    class Meta:
        verbose_name_plural = "Egresos de caja"
        verbose_name = "Egreso de caja" 

