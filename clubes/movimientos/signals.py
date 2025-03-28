from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
from .models import Egreso, Ingreso

# Señales para Ingresos
@receiver(pre_save, sender=Ingreso)
def actualizar_monto_ingreso(sender, instance, **kwargs):
    if instance.pk:  # Si es una modificación
        ingreso_anterior = Ingreso.objects.get(pk=instance.pk)
        monto_anterior = float(ingreso_anterior.monto)
        monto_nuevo = float(instance.monto)
        diferencia = monto_nuevo - monto_anterior
        instance.disciplina.monto = float(instance.disciplina.monto) + diferencia
        instance.disciplina.save()
    else:  # Si es nuevo
        instance.disciplina.monto = float(instance.disciplina.monto) + float(instance.monto)
        instance.disciplina.save()

@receiver(pre_delete, sender=Ingreso)
def restar_monto_ingreso(sender, instance, **kwargs):
    instance.disciplina.monto = float(instance.disciplina.monto) - float(instance.monto)
    instance.disciplina.save()

# Señales para Egresos
@receiver(pre_save, sender=Egreso)
def actualizar_monto_egreso(sender, instance, **kwargs):
    if instance.pk:  # Si es una modificación
        egreso_anterior = Egreso.objects.get(pk=instance.pk)
        monto_anterior = float(egreso_anterior.monto)
        monto_nuevo = float(instance.monto)
        diferencia = monto_nuevo - monto_anterior
        instance.disciplina.monto = float(instance.disciplina.monto) - diferencia
        instance.disciplina.save()
    else:  # Si es nuevo
        instance.disciplina.monto = float(instance.disciplina.monto) - float(instance.monto)
        instance.disciplina.save()

@receiver(pre_delete, sender=Egreso)
def sumar_monto_egreso(sender, instance, **kwargs):
    instance.disciplina.monto = float(instance.disciplina.monto) + float(instance.monto)
    instance.disciplina.save()