from django.contrib import admin

from parametros.models.alergia import Alergia
from parametros.models.ciudad import Ciudad
from parametros.models.concepto import Concepto
from parametros.models.dificultad import Dificultad
from parametros.models.enfermedad_cronica import EnfermedadCronica
from parametros.models.enfermedad_infancia import EnfermedadInfancia
from parametros.models.escuela import Escuela
from parametros.models.espacio import Espacio
from parametros.models.estado import Estado
from parametros.models.genero import Genero
from parametros.models.grupo_sanguineo import GrupoSanguineo
from parametros.models.institucion import Institucion
from parametros.models.medicacion import Medicacion
from parametros.models.tipo_archivo import TipoArchivo
from parametros.models.tipo_documento import TipoDocumento
from parametros.models.tipo_evento import TipoEvento
from parametros.models.tipo_intervencion import TipoIntervencion
from parametros.models.tipo_personal import TipoPersonal
from parametros.models.tipo_socio import TipoSocio
from parametros.models.vacuna import Vacuna

class CiudadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo_postal']  # Muestra más campos en la lista
    search_fields = ['nombre']  # Permite búsqueda por nombre
    ordering = ['nombre']  # Ordena por nombre

class GeneroAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

class EstadoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']
    
"""     exclude = ['club']
    
    def save_model(self, request, obj, form, change):
        obj.club = request.user.club
        super().save_model(request, obj, form, change) """

class EnfermedadCronicaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']  # Muestra también la descripción
    search_fields = ['nombre']

class EnfermedadInfanciaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

class VacunaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

class DificultadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

class AlergiaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

class MedicacionAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

class GrupoSanguineoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

class TipoIntervencionAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

class EscuelaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


class TipoEventoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']  # Muestra también la descripción
    search_fields = ['nombre']


class InstitucionAdmin(admin.ModelAdmin):
    list_display = ['tipo_institucion', 'nombre_institucion', 'direccion', 'telefono'] # Muestra más campos
    search_fields = ['tipo_institucion', 'nombre_institucion', 'ciudad__nombre']  # Búsqueda por nombre de institución y ciudad
    ordering = ['tipo_institucion', 'nombre_institucion']

    exclude = ['club']
    
    def save_model(self, request, obj, form, change):
        obj.club = request.user.club
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        # Si el usuario es un superusuario, mostramos tod
        if request.user.is_superuser:
            return queryset
        
        # Si el usuario no es superusuario, mostramos asociados a la disciplina
        try:
            mi_club = request.user.club  
            if mi_club:
                queryset = queryset.filter(club=mi_club)
                return queryset
        except AttributeError:
            # Si no se encuentra la disciplina en el usuario, no se muestra nada
            queryset = queryset.none()
        
        return queryset


class EspacioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'apto_deporte'] # Muestra más detalles
    search_fields = ['nombre']
    
    exclude = ['club']
    
    def save_model(self, request, obj, form, change):
        obj.club = request.user.club
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        # Si el usuario es un superusuario, mostramos tod
        if request.user.is_superuser:
            return queryset
        
        # Si el usuario no es superusuario, mostramos asociados a la disciplina
        try:
            mi_club = request.user.club  
            if mi_club:
                queryset = queryset.filter(club=mi_club)
                return queryset
        except AttributeError:
            # Si no se encuentra la disciplina en el usuario, no se muestra nada
            queryset = queryset.none()
        
        return queryset


class TipoPersonalAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


class TipoSocioAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

class TipoArchivoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']


class ConceptoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

    exclude = ['club']
    
    def save_model(self, request, obj, form, change):
        obj.club = request.user.club
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        # Si el usuario es un superusuario, mostramos tod
        if request.user.is_superuser:
            return queryset
        
        # Si el usuario no es superusuario, mostramos asociados a la disciplina
        try:
            mi_club = request.user.club  
            if mi_club:
                queryset = queryset.filter(club=mi_club)
                return queryset
        except AttributeError:
            # Si no se encuentra la disciplina en el usuario, no se muestra nada
            queryset = queryset.none()
        
        return queryset


# Registrar los modelos en el admin
admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(Genero, GeneroAdmin)
admin.site.register(Estado, EstadoAdmin)
admin.site.register(EnfermedadCronica, EnfermedadCronicaAdmin)
admin.site.register(EnfermedadInfancia, EnfermedadInfanciaAdmin)
admin.site.register(Vacuna, VacunaAdmin)
admin.site.register(Dificultad, DificultadAdmin)
admin.site.register(Alergia, AlergiaAdmin)
admin.site.register(Medicacion, MedicacionAdmin)
admin.site.register(GrupoSanguineo, GrupoSanguineoAdmin)
admin.site.register(TipoIntervencion, TipoIntervencionAdmin)
admin.site.register(Escuela, EscuelaAdmin)
admin.site.register(TipoEvento, TipoEventoAdmin)
admin.site.register(Institucion, InstitucionAdmin)
admin.site.register(Espacio, EspacioAdmin)
admin.site.register(TipoPersonal, TipoPersonalAdmin)
admin.site.register(TipoSocio, TipoSocioAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(TipoArchivo, TipoArchivoAdmin)
admin.site.register(Concepto, ConceptoAdmin)
