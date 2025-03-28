from django.contrib import admin
from .models import Evento, ParticipantesEvento, ResponsableDeportivoEvento, ResponsableEvento
from club.models.personal import Personal
from disciplinas.models import Disciplina, Categoria

# Inline para ParticipantesEvento
class ParticipantesEventoInline(admin.TabularInline):
    model = ParticipantesEvento
    extra = 1  

# Inline para ResponsableEvento
class ResponsableEventoInline(admin.TabularInline):
    model = ResponsableEvento
    extra = 1  # Número de filas adicionales vacías para agregar responsables generales

# Inline para ResponsableDeportivoEvento
class ResponsableDeportivoEventoInline(admin.TabularInline):
    model = ResponsableDeportivoEvento
    extra = 1  # Número de filas adicionales vacías para agregar responsables deportivos

# Personalización del modelo Evento en el admin
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    inlines = [
        ParticipantesEventoInline,
        ResponsableEventoInline,  # Responsables generales
        ResponsableDeportivoEventoInline  # Responsables deportivos
    ]
    list_display = ("tipo_evento", "nombre", "fecha_inicio", "fecha_fin", "lugar")
    search_fields = ("nombre", "tipo_evento__nombre", "lugar")
    list_filter = ("tipo_evento", "ciudad", "estado")
    exclude = ["club"]

   # Personalización de los campos que se ven en el formulario de detalle
    fieldsets = (
        (None, {
            'fields': ('tipo_evento', 'nombre', 'fecha_inicio', 'fecha_fin', 'lugar', 'ciudad', 'estado')
        }),
        ('Disciplinas y Categorías', {
            'fields': ('disciplinas', 'categorias')
        }),
        ('Descripción', {
            'fields': ('descripcion',)
        }),
        ('Institución', {
            'fields': ('institucion',)
        }),
    )
        
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
                queryset = queryset.filter(disciplinas__nombre=mi_disciplina.nombre)
            mi_club = request.user.club  
            if mi_club:
                queryset = queryset.filter(club=mi_club)
        except AttributeError:
            # Si no se encuentra la disciplina en el usuario, no se muestra nada
            queryset = queryset.none()
        
        return queryset

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        club = request.user.club
        if db_field.name == "disciplinas":
            if request.user.is_superuser:
                # Los superusuarios ven todas las disciplinas activas
                kwargs["queryset"] = Disciplina.objects.filter(estado=True)
            else:
                # Los usuarios normales ven solo su disciplina o todas las del club
                mi_disciplina = getattr(request.user, 'disciplina', None)
                if mi_disciplina:
                    kwargs["queryset"] = Disciplina.objects.filter(pk=mi_disciplina.pk, estado=True)
                else:
                    kwargs["queryset"] = Disciplina.objects.filter(club=club, estado=True)
        elif db_field.name == "categorias":
            if request.user.is_superuser:
                # Los superusuarios ven todas las categorías activas
                kwargs["queryset"] = Categoria.objects.filter(estado=True)
            else:
                # Los usuarios normales ven categorías relacionadas con su disciplina
                mi_disciplina = getattr(request.user, 'disciplina', None)
                disciplinas_club = Disciplina.objects.filter(club=club, estado=True)
                if mi_disciplina:
                    kwargs["queryset"] = Categoria.objects.filter(disciplina=mi_disciplina, estado=True)
                else:
                    kwargs["queryset"] = Categoria.objects.filter(disciplina__in=disciplinas_club, estado=True)

        
        return super().formfield_for_manytomany(db_field, request, **kwargs)
      


# Personalización del modelo ResponsableEvento
@admin.register(ResponsableEvento)
class ResponsableEventoAdmin(admin.ModelAdmin):
    list_display = ('evento', 'personal')
    search_fields = ('evento__nombre', 'personal__nombre', 'personal__apellido')
    list_filter = ('evento',)

    # Filtro para limitar la selección de personal que no son profesores
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "personal":
            # Filtrar los empleados que no son profesores 
            kwargs["queryset"] = Personal.objects.exclude(tipo_personal__nombre="Profesor")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Personalización del modelo ResponsableDeportivoEvento
@admin.register(ResponsableDeportivoEvento)
class ResponsableDeportivoEventoAdmin(admin.ModelAdmin):
    list_display = ('evento', 'profesor', )
    search_fields = ('evento__nombre', 'profesor__nombre', 'profesor__apellido')
    list_filter = ('evento', )

    # Filtro para limitar la selección de personal solo a los profesores
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "profesor":
            # Filtra para que solo se muestre los empleados que son profesores
            kwargs["queryset"] = Personal.objects.filter(tipo_personal__nombre="Profesor")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
