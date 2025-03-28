from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.forms import ValidationError
from parametros.models.tipo_socio import TipoSocio
from clubes.validators import validate_valor_desde_hasta, validate_valor_negativo


METODOS_PAGOS = [
    ('efectivo', 'Efectivo'),
    ('transferencia', 'Transferencia'),
    ('otros', 'Otros'),
]
ESTADOS_DE_PAGO = [
    ('pendiente', 'Pendiente'),
    ('confirmado', 'Confirmado'),
]
TIPO_CUOTA = [
    ('dep', 'Deportiva'),
    ('soc', 'Social')
]

MESES = [
    ('01', 'Enero'),
    ('02', 'Febrero'),
    ('03', 'Marzo'),
    ('04', 'Abril'),
    ('05', 'Mayo'),
    ('06', 'Junio'),
    ('07', 'Julio'),
    ('08', 'Agosto'),
    ('09', 'Septiembre'),
    ('10', 'Octubre'),
    ('11', 'Noviembre'),
    ('12', 'Diciembre')
]


class EsquemaCuotaSocial (models.Model):
    tipo_socio = models.ForeignKey(TipoSocio, on_delete=models.CASCADE)
    dias_vencimiento = models.IntegerField(validators=[validate_valor_negativo], null=True, blank=True)
    cobra_mora = models.BooleanField(default=False, null=True, blank=True)
    monto_penalizacion = models.IntegerField(validators=[validate_valor_desde_hasta], help_text="Porcentaje, ingrese un valor entre 0 y 100", null=True, blank=True)
    monto =  models.FloatField(validators=[validate_valor_negativo], help_text="Ingrese un valor mayor a 0")
    descuento_x_2 = models.IntegerField(validators=[validate_valor_desde_hasta], help_text="Ingrese un valor entre 0 y 100")
    descuento_x_3 = models.IntegerField(validators=[validate_valor_desde_hasta], help_text="Ingrese un valor entre 0 y 100")
    descuento_x_4 = models.IntegerField(validators=[validate_valor_desde_hasta], help_text="Ingrese un valor entre 0 y 100")

    def __str__(self):
        return f"{self.monto}"
    
    class Meta:
        ordering = ['monto']
        verbose_name_plural = "Cuotas Sociales"
        verbose_name = "Cuota Social" 

    def clean(self):
        super().clean()
        if EsquemaCuotaSocial.objects.filter( tipo_socio=self.tipo_socio).exclude(id=self.id).exists():
            raise ValidationError('Ya existe un esquema de cuota social para este tipo de socio.')


class EsquemaCuotaDeportiva (models.Model):
    from disciplinas.models import Disciplina, Categoria
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    monto =  models.FloatField(validators=[validate_valor_negativo], help_text="Ingrese un valor mayor a 0")
    dias_vencimiento = models.IntegerField(validators=[validate_valor_negativo], null=True, blank=True)
    cobra_mora = models.BooleanField(default=False, null=True, blank=True)
    monto_penalizacion = models.IntegerField(validators=[validate_valor_desde_hasta], help_text="Porcentaje, ingrese un valor entre 0 y 100", null=True, blank=True)
    descuento_x_2 = models.IntegerField(validators=[validate_valor_desde_hasta], help_text="Ingrese un valor entre 0 y 100") # verificar q sea entre 0 y 100
    descuento_x_3 = models.IntegerField(validators=[validate_valor_desde_hasta], help_text="Ingrese un valor entre 0 y 100")
    descuento_x_4 = models.IntegerField(validators=[validate_valor_desde_hasta], help_text="Ingrese un valor entre 0 y 100")
      
    def __str__(self):
        return f"{self.monto}"
    
    class Meta:
        ordering = ['monto']
        verbose_name_plural = "Cuotas Deportivas"
        verbose_name = "Cuota Deportiva" 
    def clean(self):
        super().clean()
        if EsquemaCuotaDeportiva.objects.filter(disciplina=self.disciplina, categoria=self.categoria).exclude(id=self.id).exists():
            raise ValidationError('Ya existe un esquema de cuota deportiva para esta disciplina y categoría.')

class Pago (models.Model):
    fecha = models.DateField()
    # socio =  models.ForeignKey()
    modalidad= models.CharField(max_length=20, choices= METODOS_PAGOS, default='efectivo')
    referencia = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS_DE_PAGO, default='pendiente')
    monto= models.CharField(max_length=20, )
    detalles = models.TextField(null=True, blank=True)


    def __str__(self):
        return f"{self.fecha} - {self.monto}"
    
    class Meta:
        ordering = ['fecha', 'monto']
        verbose_name_plural = "Pagos"
        verbose_name = "Pago" 

    def recalcular_monto(self):
        """Actualiza el monto basado en las cuotas relacionadas."""
        total_monto = self.cuota_set.aggregate(total=models.Sum('monto_neto'))['total'] or 0
        self.monto = total_monto
        self.save()
    
class Cuota (models.Model):
    from socios.models import Socio
    from disciplinas.models import Disciplina
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, null=True, blank=True, help_text="Seleccionar disciplina sólo en caso de crear cuota deportiva")
    tipo_socio = models.ForeignKey(TipoSocio, on_delete=models.CASCADE, null=True, blank=True, help_text="Seleccionar tipo de socio sólo en caso de crear cuota social, debe coincidir con el del Socio elegido")
    mes = models.CharField(max_length=2, choices=MESES, verbose_name="Mes")
    anio = models.CharField(max_length=4, verbose_name="Año")
    fecha_vencimiento = models.DateField(null=True, blank=True)
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    monto_base = models.DecimalField(max_digits=9, decimal_places=2, validators=[validate_valor_negativo], help_text="Ingrese un valor mayor a 0")
    monto_neto = models.DecimalField(max_digits=9, decimal_places=2, validators=[validate_valor_negativo], help_text="Ingrese un valor mayor a 0")
    pagada= models.BooleanField()
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE, null=True, blank=True)
    

    def clean(self):
        if not self.disciplina and not self.tipo_socio:
            raise ValidationError(
                "No has seleccionado disciplina ni tipo de socio. Para crear una cuota deportiva debes seleccionar una disciplina. Para crear una cuota social debes seleccionar el tipo de socio. No elegir ambos al mismo tiempo"
            )
        if self.disciplina and self.tipo_socio:
            raise ValidationError(
                "No puedes tener asignados una disciplina y un tipo de socio al mismo tiempo. Elige disciplina si es una cuota deportiva o tipo de socio si se trata de una cuota social"
            )
        if self.socio and self.tipo_socio:
            if self.socio.tipo_socio != self.tipo_socio:
                raise ValidationError(
                    f"El Socio {self.socio} posee un tipo de socio {self.socio.tipo_socio}. No coincide con el que has seleccionado."
                )
        
        if self.disciplina:
            cuota_existente = Cuota.objects.filter(
                socio=self.socio,
                mes=self.mes,
                anio=self.anio,
                disciplina=self.disciplina
            ).exclude(pk=self.pk).exists()

            if cuota_existente:
                raise ValidationError(
                    f"Ya existe una cuota deportiva registrada para {self.socio}, para el período {self.mes}-{self.anio} de la disciplina {self.disciplina}."
                )
        if self.tipo_socio:
            cuota_existente = Cuota.objects.filter(
                socio=self.socio,
                mes=self.mes,
                anio=self.anio,
                tipo_socio = self.tipo_socio
            ).exists()

            if cuota_existente:
                raise ValidationError(
                    f"Ya existe una cuota social registrada para {self.socio}, tipo de socio {self.tipo_socio} para el período {self.mes}-{self.anio}"
                )
            
        if self.disciplina:
            # Verificar si el socio tiene alguna categoría asociada a la disciplina seleccionada
            categorias_del_socio = self.socio.socio.all()
            disciplinas_asociadas = categorias_del_socio.filter(categoria__disciplina=self.disciplina)

            if not disciplinas_asociadas.exists():
                raise ValidationError(
                    f"El socio seleccionado no tiene asignada la disciplina '{self.disciplina.nombre}' en sus categorías."
                )
        

    def __str__(self):
        return f"{self.mes} - {self.anio} - {self.socio}"
    class Meta:
        ordering = ['mes', 'anio']
        verbose_name_plural = "Cuotas"
        verbose_name = "Cuota" 
    @property
    def es_deportiva(self):
        return self.disciplina is not None

    @property
    def es_social(self):
        return self.tipo_socio is not None



@receiver(post_delete, sender=Cuota)
def actualizar_pago_post_delete(sender, instance, **kwargs):
    """Recalcula el monto del pago al eliminar una cuota."""
    if instance.pago_id: 
            try:
                pago = Pago.objects.get(id=instance.pago_id)
                pago.recalcular_monto()
            except Pago.DoesNotExist:
                pass # si no hay pago no recalcula