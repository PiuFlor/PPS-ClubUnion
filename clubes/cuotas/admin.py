from datetime import datetime
from django.contrib import admin, messages

from .models import  Pago, Cuota, EsquemaCuotaDeportiva, EsquemaCuotaSocial
from disciplinas.models import Disciplina, Categoria
from socios.models import Socio

@admin.action(description="Confirmar Pago")
def confirmar_pago(modeladmin, request, queryset):
    pagos_confirmados = queryset.filter(estado='confirmado')
    
    if pagos_confirmados.exists():
        messages.error(request, "En la selección existen pagos ya confirmados. Revise la selección e intente nuevamente.")
        return  

    try:
        queryset.update(estado='confirmado')
        for pago in queryset:
            cuotas = Cuota.objects.filter(pago=pago.id)
            cuotas.update(pagada=True)
        messages.success(request, "Pago/s confirmado/s exitosamente")

    except Exception as e:
        messages.error(request, f"Error al confirmar el pago: {str(e)}")
    

@admin.action(description="Pagar cuotas")
def pagar_cuotas(modeladmin, request, queryset):
    cuotas_pagadas = queryset.filter(pagada=True)
    if cuotas_pagadas.exists():
        messages.error(
            request, 
            "Se han seleccionado cuotas que ya están pagas. Por favor, revise la selección e intente nuevamente."
        )
        return
    monto = 0
    for cuota in queryset:
        monto += cuota.monto_neto
    try:
        pago = Pago(
            fecha = datetime.now(),
            monto = monto,
            estado = 'confirmado'
        )
        pago.save()
        queryset.update(pago=pago)
        queryset.update(pagada=True)
        messages.success(request, f"Pago registrado exitosamente por un monto de {monto:.2f}.")
    except Exception as e:
        messages.error(request, f"Error al registrar el pago: {str(e)}")
    
class CuotaInline(admin.TabularInline):
    model = Cuota
    max_num=0 
    fields = ('mes', 'anio', 'monto_base', 'monto_neto', 'socio', 'pagada')    
    readonly_fields =('mes', 'anio', 'fecha_vencimiento', 'monto_base', 'monto_neto', 'socio', 'pagada')    
    can_delete = True
    show_change_link = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PagoAdmin(admin.ModelAdmin):
    list_display= ['fecha', 'modalidad', 'estado', 'monto']
    inlines = [CuotaInline]
    """ actions = [confirmar_pago] """

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
class EsquemaCuotaDeportivaAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'categoria', 'monto', 'descuento_x_2', 'descuento_x_3', 'descuento_x_4')
    list_filter = ['categoria', 'disciplina']
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "disciplina":
            kwargs["queryset"] = Disciplina.objects.filter(estado=True)
        elif db_field.name == "categoria":
            kwargs["queryset"] = Categoria.objects.filter(estado=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class EsquemaCuotaSocialAdmin(admin.ModelAdmin):
    list_display = ('tipo_socio', 'monto', 'descuento_x_2', 'descuento_x_3', 'descuento_x_4')
    list_filter = ['tipo_socio']

class EstadoCuotaFilter(admin.SimpleListFilter):
    title = 'Estado' 
    parameter_name = 'estado'

    def lookups(self, request, model_admin):
      
        return (
            ('True', 'Pagada'),
            ('False', 'Impaga'),
        )

    def queryset(self, request, queryset):
  
        if self.value() == 'True':
            return queryset.filter(pagada=True)
        if self.value() == 'False':
            return queryset.filter(pagada=False)
        return queryset
    

class TipoCuotaFilter(admin.SimpleListFilter):
    title = 'Tipo de Cuota'
    parameter_name = 'tipo_cuota'

    def lookups(self, request, model_admin):
        return [
            ('deportiva', 'Deportiva'),
            ('social', 'Social'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'deportiva':
            return queryset.filter(disciplina__isnull=False)
        elif self.value() == 'social':
            return queryset.filter(tipo_socio__isnull=False)
        return queryset


class SocioFilter(admin.SimpleListFilter):
    title = 'socio'
    parameter_name = 'socio' 

    def lookups(self, request, model_admin):
        
        from socios.models import Socio  
        return [(s.id, str(s)) for s in Socio.objects.all()]

    def queryset(self, request, queryset):
       
        if self.value():
            return queryset.filter(socio_id=self.value())
        return queryset
class CuotaAdmin(admin.ModelAdmin):
    list_display = ["mes", "anio", "socio", "monto_base", "monto_neto", "fecha_vencimiento", "pagada"]
    list_filter = [TipoCuotaFilter, 'mes', 'anio', EstadoCuotaFilter, SocioFilter, 'socio__grupo_familiar']
    actions = [pagar_cuotas]   
    # search_fields = ['socio__nombre', 'disciplina__nombre', 'tipo_socio__nombre']
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "disciplina":
            kwargs["queryset"] = Disciplina.objects.filter(estado=True)
        elif db_field.name == "socio":
            kwargs["queryset"] = Socio.objects.filter(activo=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
 
admin.site.register(Cuota, CuotaAdmin)
admin.site.register(EsquemaCuotaDeportiva, EsquemaCuotaDeportivaAdmin)
admin.site.register(EsquemaCuotaSocial, EsquemaCuotaSocialAdmin)
admin.site.register(Pago, PagoAdmin)