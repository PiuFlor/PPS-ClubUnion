from django.contrib import admin
from .models import Intervencion
from parametros.models.tipo_intervencion import TipoIntervencion
from disciplinas.models import Disciplina, Categoria


class IntervencionAdmin(admin.ModelAdmin):
    # Personaliza los campos que se muestran en la lista
    list_display = ('tipo_intervencion', 'disciplina', 'socio', 'fecha', 'estado')
    
    # Hacer que los campos se puedan buscar
    search_fields = ('referentes', 'socio', 'tipo_intervencion__nombre', 'disciplina__nombre')
    
    # Filtrar por ciertos campos
    list_filter = ('tipo_intervencion', 'estado', 'disciplina', 'fecha')
    
    # Agregar un campo de edición rápido
    list_editable = ('estado',)
    exclude = ["club"]

    # Personalizar la vista de detalle del registro
    fieldsets = (
        (None, {
            'fields': ('tipo_intervencion', 'referentes', 'disciplina', 'socio', 'fecha', 'estado')
        }),
        ('Notas', {
            'fields': ('notas',)
        }),
    )
    
    # Cambiar el orden de los campos en el formulario de creación
    ordering = ('tipo_intervencion', 'fecha')
    
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
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        club = request.user.club
        if db_field.name == "disciplina":
            if request.user.is_superuser:
            # Los superusuarios pueden ver todas las disciplinas activas
                kwargs["queryset"] = Disciplina.objects.filter(estado=True)
            else:
                # Filtrar por la disciplina asociada al usuario
                try:
                    mi_disciplina = request.user.disciplina
                    if mi_disciplina:
                        kwargs["queryset"] = Disciplina.objects.filter(pk=mi_disciplina.pk, estado=True)
                    else:
                        kwargs["queryset"] = Disciplina.objects.filter(club=club, estado=True)
                except AttributeError:
                # Si el usuario no tiene una disciplina asociada
                    kwargs["queryset"] = Disciplina.objects.none()

        elif db_field.name == "categoria":
            if request.user.is_superuser:
                # Los superusuarios pueden ver todas las categorías activas
                kwargs["queryset"] = Categoria.objects.filter(estado=True)
            else:
                # Filtrar categorías según la disciplina del usuario
                try:
                    mi_disciplina = request.user.disciplina
                    disciplinas_club = Disciplina.objects.filter(club=club, estado=True)
                    if mi_disciplina:
                        kwargs["queryset"] = Categoria.objects.filter(disciplina=mi_disciplina, estado=True)
                    else:
                        kwargs["queryset"] = Categoria.objects.none()
                except AttributeError:
                    kwargs["queryset"] = Categoria.objects.filter(disciplina__in=disciplinas_club, estado=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Registra el modelo en el admin
admin.site.register(Intervencion, IntervencionAdmin)