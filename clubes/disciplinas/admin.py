from datetime import date
from django.contrib import messages  # Importación correcta

import re
from django.contrib import admin
from django.db import models
from django.forms import TimeInput, ValidationError
from django.forms.widgets import TimeInput
from django.db.models import Q
from django.db import transaction

from club.models.club import Club
from club.models.personal import Personal
from parametros.models.espacio import Espacio

from .forms import DisciplinaForm
from socios.models import Socio
from .models import Categoria, Disciplina, Horario, ProfesorCategoria, SocioCategoria


@admin.action(description="Copiar Categoría")
def copiar_categoria(modeladmin, request, queryset):
    with transaction.atomic():  
        contadores_disciplina = {}
        
        for categoria in queryset:
            disciplina_id = categoria.disciplina_id
            if disciplina_id not in contadores_disciplina:
                max_copia = 0
                nombre_base = re.sub(r'\s*\(Copia\s*\d*\)\s*$', '', categoria.nombre)
                existentes = categoria.__class__.objects.filter(
                    disciplina_id=disciplina_id,
                    nombre__regex=fr"^{re.escape(nombre_base)}\s*\(Copia(\s*\d*)?\)"
                )
                for existente in existentes:
                    match = re.search(r'\(Copia\s*(\d+)?\)', existente.nombre)
                    if match:
                        num = match.group(1)
                        if num:
                            max_copia = max(max_copia, int(num))
                        else:
                            max_copia = max(max_copia, 1)
                contadores_disciplina[disciplina_id] = max_copia

        for categoria in queryset:
            horarios = Horario.objects.filter(categoria=categoria)
            profesores_categoria = ProfesorCategoria.objects.filter(categoria=categoria)
            socios_categoria = SocioCategoria.objects.filter(categoria=categoria)
            
            if categoria.estado:
                categoria.estado = False
                categoria.save()

            nueva_categoria = categoria
            nueva_categoria.pk = None
            
            nombre_base = re.sub(r'\s*\(Copia\s*\d*\)\s*$', '', categoria.nombre)
            disciplina_id = categoria.disciplina_id

            contadores_disciplina[disciplina_id] += 1
            contador = contadores_disciplina[disciplina_id]

            nuevo_nombre = f"{nombre_base} (Copia{' ' + str(contador) if contador > 1 else ''})"

            nueva_categoria.nombre = nuevo_nombre
            nueva_categoria.anio += 1
            nueva_categoria.estado = True
            nueva_categoria.save()

            for horario in horarios:
                horario.pk = None
                horario.categoria = nueva_categoria
                horario.save()
                
            for profesor_categoria in profesores_categoria:
                profesor_categoria.pk = None
                profesor_categoria.categoria = nueva_categoria
                profesor_categoria.save()
                
            for socio_categoria in socios_categoria:
                socio_categoria.pk = None
                socio_categoria.categoria = nueva_categoria
                socio_categoria.save()

class HorarioAdmin(admin.ModelAdmin):
    list_display = ('cancha', 'dia_semana', 'inicio', 'fin', 'categoria')
    exclude = ['club']
    
    formfield_overrides = {
        models.TimeField: {'widget': TimeInput(format='%H:%M')}
    }
    
    list_filter = ['cancha', 'dia_semana', 'categoria']  

    def inicio(self, obj):
        return obj.inicio.strftime('%H:%M')  

    def fin(self, obj):
        return obj.fin.strftime('%H:%M')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "cancha":
            mi_club = request.user.club
            kwargs["queryset"] = Espacio.objects.filter(club=mi_club).filter(apto_deporte=True)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        
            """ if db_field.name == "categoria":
            mi_disciplina = request.user.disciplina
            kwargs["queryset"] = Categoria.objects.filter(categoria__disciplina=mi_disciplina).filter(activo=True)
            return super().formfield_for_foreignkey(db_field, request, **kwargs) """

    def save_model(self, request, obj, form, change):
        # Asigna por defecto el club del usuario logueado
        obj.club = request.user.club
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        # Si el usuario es un superusuario, mostramos tod
        if request.user.is_superuser:
            return queryset
        
        # Si el usuario no es superusuario, mostramos asociados a la disciplina
        try:
            mi_disciplina = request.user.disciplina  
            if mi_disciplina:
                queryset = queryset.filter(categoria__disciplina=mi_disciplina)
                return queryset
            mi_club = request.user.club  
            if mi_club:
                queryset = queryset.filter(club=mi_club)
                return queryset
        except AttributeError:
            # Si no se encuentra la disciplina en el usuario, no se muestra nada
            queryset = queryset.none()
        
        return queryset

class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 0
    fields = ('cancha', 'dia_semana', 'inicio', 'fin')

    formfield_overrides = {
        models.TimeField: {'widget': TimeInput(format='%H:%M')}
    }

    def inicio(self, obj):
        return obj.inicio.strftime('%H:%M')  

    def fin(self, obj):
        return obj.fin.strftime('%H:%M')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False




class ProfesorCategoriaInline(admin.TabularInline):
    model = ProfesorCategoria
    extra = 0
    fields = ('categoria','profesor','estado')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
   
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "profesor":
            kwargs["queryset"] = Personal.objects.filter(estado=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
class DisciplinaAdmin(admin.ModelAdmin):
    list_filter = ['estado']
    list_display = ['nombre', 'estado', 'monto']
    readonly_fields = ['monto']
    form = DisciplinaForm

    def save_model(self, request, obj, form, change):
        # Asigna por defecto el club del usuario logueado
        obj.club = request.user.club
        super().save_model(request, obj, form, change)


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Si el usuario es un superusuario, mostramos tod
        if request.user.is_superuser:
            return queryset
        # Si el usuario no es superusuario, mostramos asociados a la disciplina
        try:
            mi_disciplina = request.user.disciplina  
            if mi_disciplina:
                queryset = queryset.filter(id=mi_disciplina.id)
            mi_club = request.user.club  
            if mi_club:
                queryset = queryset.filter(club=mi_club)
        except AttributeError:
            # Si no se encuentra la disciplina en el usuario, no se muestra nada
            queryset = queryset.none()
        
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filtrar el campo 'club' según el club del usuario
        if db_field.name == 'club':
            mi_club = getattr(request.user, 'club', None)
            if mi_club:
                kwargs['queryset'] = Club.objects.filter(id=mi_club.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

#Validar la edad del socio
def validate_socio_age(socio, categoria, request):
    fecha_nacimiento = socio.fecha_nacimiento

    if fecha_nacimiento:
        today = date.today()
        age = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        edad_desde = categoria.edad_desde
        edad_hasta = categoria.edad_hasta

        if age < edad_desde or age > edad_hasta:
            messages.warning(
                request,
                f"Advertencia: El socio '{socio}' tiene {age} años, que está fuera de la edad permitida ({edad_desde}-{edad_hasta}) para la categoría '{categoria}'."
            )
            return False
    return True

class SocioCategoriaInline(admin.TabularInline):
    model = SocioCategoria
    fields = ('socio', 'estado')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CategoriaAdmin(admin.ModelAdmin):
    inlines = [HorarioInline, SocioCategoriaInline, ProfesorCategoriaInline]
    exclude = ['club']
    actions = [copiar_categoria]
    
    list_filter = ['nombre', 'disciplina', 'anio', 'estado']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'disciplina':
            # Si el usuario es superusuario, no se aplica filtro
            if request.user.is_superuser:
                kwargs['queryset'] = Disciplina.objects.filter(estado=True)
            else:
                # Obtener la disciplina asociada al usuario
                mi_disciplina = getattr(request.user, 'disciplina', None)
                if mi_disciplina:
                    # Filtrar solo por la disciplina del usuario
                    kwargs['queryset'] = Disciplina.objects.filter(id=mi_disciplina.id, estado=True)
                else:
                    # Si el usuario no tiene disciplina, no mostrar opciones
                    kwargs['queryset'] = Disciplina.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_inlines(self, request, obj=None):
        if obj:  
            return [HorarioInline, SocioCategoriaInline, ProfesorCategoriaInline]
        else:  
            return []

    def save_model(self, request, obj, form, change):
        # Asigna por defecto el club del usuario logueado
        obj.club = request.user.club
        super().save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        if formset.model == SocioCategoria:
            instances = formset.save(commit=False) 
            for instance in instances:
                
                if instance.socio and instance.categoria:
                    validate_socio_age(instance.socio, instance.categoria, request)  
                instance.save() 
            formset.save_m2m()  
        else:
            formset.save()


    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        # Si el usuario es un superusuario, mostramos tod
        if request.user.is_superuser:
            return queryset
        
        # Si el usuario no es superusuario, mostramos asociados a la disciplina
        try:
            mi_disciplina = request.user.disciplina  
            if mi_disciplina:
                queryset = queryset.filter(disciplina=mi_disciplina)
                return queryset
            mi_club = request.user.club  
            if mi_club:
                queryset = queryset.filter(club=mi_club)
                return queryset
        except AttributeError:
            # Si no se encuentra la disciplina en el usuario, no se muestra nada
            queryset = queryset.none()
        
        return queryset

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filtrar el campo 'club' según el club del usuario
        if db_field.name == 'club':
            mi_club = getattr(request.user, 'club', None)
            if mi_club:
                kwargs['queryset'] = Club.objects.filter(id=mi_club.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SocioCategoriaAdmin(admin.ModelAdmin):
    list_display = ['socio', 'categoria']
    exclude = ['club']

    def save_model(self, request, obj, form, change):
        # Asigna por defecto el club del usuario logueado
        obj.club = request.user.club
        if(validate_socio_age(obj.socio, obj.categoria, request)):
            if SocioCategoria.objects.filter(categoria=obj.categoria, socio=obj.socio).exclude(id=obj.id).exists():
                raise ValidationError('El socio ya tiene asignada esa categoría')
            super().save_model(request, obj, form, change)
        else:
            return False
        

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "socio":
            kwargs["queryset"] = Socio.objects.filter(activo=True)
        if db_field.name == "categoria":
            kwargs["queryset"] = Categoria.objects.filter(estado=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        # Si el usuario es un superusuario, mostramos tod
        if request.user.is_superuser:
            return queryset
        
        # Si el usuario no es superusuario, mostramos asociados a la disciplina
        try:
            mi_disciplina = request.user.disciplina  
            if mi_disciplina:
                queryset = queryset.filter(categoria__disciplina=mi_disciplina)
                return queryset
            mi_club = request.user.club  
            if mi_club:
                queryset = queryset.filter(club=mi_club)
                return queryset
        except AttributeError:
            # Si no se encuentra la disciplina en el usuario, no se muestra nada
            queryset = queryset.none()
        
        return queryset

class ProfesorCategoriaAdmin(admin.ModelAdmin):
    list_filter = ['categoria']
    exclude = ['club']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "profesor":
            kwargs["queryset"] = Personal.objects.filter(estado=True, tipo_personal__nombre = 'Profesor/a')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        # Asigna por defecto el club del usuario logueado
        obj.club = request.user.club
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        
        # Si el usuario es un superusuario, mostramos tod
        if request.user.is_superuser:
            return queryset
        
        # Si el usuario no es superusuario, mostramos asociados a la disciplina
        try:
            mi_disciplina = request.user.disciplina  
            if mi_disciplina:
                queryset = queryset.filter(categoria__disciplina=mi_disciplina)
                return queryset
            mi_club = request.user.club  
            if mi_club:
                queryset = queryset.filter(club=mi_club)
                return queryset
        except AttributeError:
            # Si no se encuentra la disciplina en el usuario, no se muestra nada
            queryset = queryset.none()
        
        return queryset

# Register your models here.
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(Horario, HorarioAdmin)
admin.site.register(ProfesorCategoria, ProfesorCategoriaAdmin)
admin.site.register(SocioCategoria, SocioCategoriaAdmin)