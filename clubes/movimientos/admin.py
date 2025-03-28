from django.contrib import admin
from .models import Ingreso, Egreso  # Asegúrate de que están correctamente importados
from django import forms
from django.utils.timezone import now

# Register your models here.
class IngresoAdmin(admin.ModelAdmin):
    # Personaliza los campos que se muestran en la lista
    list_display = ('fecha', 'concepto', 'monto')

    # Filtrar por ciertos campos
    list_filter = ('concepto', 'responsable', 'disciplina', 'fecha')

    exclude = ["club"]
    
    # Cambiar el orden de los campos en el formulario de creación
    ordering = ['fecha']
    
    def save_model(self, request, obj, form, change):
        obj.club = request.user.club
        super().save_model(request, obj, form, change)


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        # Si el usuario es un superusuario, mostramos todo
        if request.user.is_superuser:
            return queryset
        
        # Si el usuario no es superusuario, mostramos eventos asociados a la disciplina
        try:
            mi_disciplina = request.user.disciplina  
            if mi_disciplina:
                queryset = queryset.filter(disciplina=mi_disciplina)
            mi_club = request.user.club  
            if mi_club:
                queryset = queryset.filter(club=mi_club)
        except AttributeError:
            # Si no se encuentra la disciplina en el usuario, no se muestra nada
            queryset = queryset.none()
        
        return queryset

# Registra el modelo en el admin
admin.site.register(Ingreso, IngresoAdmin)

class EgresoAdmin(admin.ModelAdmin):

    # Personaliza los campos que se muestran en la lista
    list_display = ('fecha', 'concepto', 'monto')

    # Filtrar por ciertos campos
    list_filter = ('concepto', 'responsable', 'disciplina', 'fecha')

    exclude = ["club"]
    
    # Cambiar el orden de los campos en el formulario de creación
    ordering = ['fecha']
    
    def save_model(self, request, obj, form, change):
        obj.club = request.user.club
        super().save_model(request, obj, form, change)


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        # Si el usuario es un superusuario, mostramos todo
        if request.user.is_superuser:
            return queryset
        
        # Si el usuario no es superusuario, mostramos eventos asociados a la disciplina
        try:
            mi_disciplina = request.user.disciplina  
            if mi_disciplina:
                queryset = queryset.filter(disciplina=mi_disciplina)
            mi_club = request.user.club  
            if mi_club:
                queryset = queryset.filter(club=mi_club)
        except AttributeError:
            # Si no se encuentra la disciplina en el usuario, no se muestra nada
            queryset = queryset.none()
        
        return queryset

# Registra el modelo en el admin
admin.site.register(Egreso, EgresoAdmin)
