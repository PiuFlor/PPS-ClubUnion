from django.contrib import admin

from .forms import TipoArticuloForm
from .models import Articulo, DetalleEntrega, DetalleRecepcion, Entrega, Recepcion, TipoArticulo

# Register your models here.


class TipoArticuloAdmin(admin.ModelAdmin):
    form = TipoArticuloForm
        
    def save_model(self, request, obj, form, change):
        obj.club = request.user.club
        super().save_model(request, obj, form, change)

admin.site.register(TipoArticulo, TipoArticuloAdmin)


class ArticuloAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipoArticulo', 'stock']
    list_filter = ['tipoArticulo']
    readonly_fields = ['stock']
    exclude=['club']

        
    def save_model(self, request, obj, form, change):
        obj.club = request.user.club
        super().save_model(request, obj, form, change)

admin.site.register(Articulo, ArticuloAdmin)


@admin.action(description="Completar Recepción de Artículos")
def completar_recepcion(modeladmin, request, queryset):
    queryset.update(estado="C")
    for obj in queryset:
        prods = DetalleRecepcion.objects.filter(recepcion=obj)
        for prod in prods:
            prod.articulo.stock += prod.cantidad
            prod.articulo.save()

@admin.action(description="Completar Entrega de Artículos")
def completar_entrega(modeladmin, request, queryset):
    queryset.update(estado="C")
    for obj in queryset:
        prods = DetalleEntrega.objects.filter(entrega=obj)
        for prod in prods:
            prod.articulo.stock -= prod.cantidad
            prod.articulo.save()


class DetalleEntregaInline(admin.TabularInline):
    model = DetalleEntrega
    fields = ('articulo', 'cantidad')
    exclude=['club']

class EntregaAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'estado', 'referencia']
    list_filter = ['estado']
    actions = [completar_entrega]
    inlines = [DetalleEntregaInline]
    readonly_fields = ['estado']
    exclude=['club']

        
    def save_model(self, request, obj, form, change):
        obj.club = request.user.club
        super().save_model(request, obj, form, change)

admin.site.register(Entrega, EntregaAdmin)



class DetalleRecepcionInline(admin.TabularInline):
    model = DetalleRecepcion
    fields = ('articulo', 'cantidad')
    exclude=['club']


class RecepcionAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'estado', 'referencia']
    list_filter = ['estado']
    actions = [completar_recepcion]
    inlines = [DetalleRecepcionInline]
    readonly_fields = ['estado']
    exclude=['club']
        
    def save_model(self, request, obj, form, change):
        obj.club = request.user.club
        super().save_model(request, obj, form, change)


admin.site.register(Recepcion, RecepcionAdmin)
