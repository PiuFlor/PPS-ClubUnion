from django.contrib import admin
from django.contrib import messages

from club.models.club import Club
from club.models.documento_vinculado import DocumentoVinculado
from club.models.personal import Personal


class EstadoPersonalFilter(admin.SimpleListFilter):
    title = 'Estado' 
    parameter_name = 'estado'

    def lookups(self, request, model_admin):
      
        return (
            ('True', 'Activo'),
            ('False', 'Inactivo'),
        )

    def queryset(self, request, queryset):
  
        if self.value() == 'True':
            return queryset.filter(estado=True)
        if self.value() == 'False':
            return queryset.filter(estado=False)
        return queryset

class PersonalAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'estado', 'tipo_personal', 'fecha_ingreso']
    list_filter = ['tipo_personal', EstadoPersonalFilter, 'genero']
    exclude = ['club']
    fieldsets = (
        ('Datos Personales', {
            'fields': ('nombre', 'apellido', 'fecha_nacimiento', 'tipo_documento', 'nro_documento', 'genero', 'CUIL'),
        }), 
        ('Datos de Contacto', {
            'fields': ('direccion', 'ciudad', 'nro_telefono', 'email'),
        }),
        ('Información Laboral', {
            'fields': ('tipo_personal', 'estado', 'fecha_ingreso', 'fecha_egreso', 'descripcion_tareas'),
        }),
    )

    def save_model(self, request, obj, form, change):
        # Asigna por defecto el club del usuario logueado
        obj.club = request.user.club
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        # Obtener el organismo del usuario actual
        queryset = super().get_queryset(request)
        mi_club = request.user.club
        if (mi_club):
            queryset = queryset.filter(club=mi_club)
        return queryset
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filtrar el campo 'club' según el club del usuario
        if db_field.name == 'club':
            mi_club = getattr(request.user, 'club', None)
            if mi_club:
                kwargs['queryset'] = Club.objects.filter(id=mi_club.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
 
class DocumentoVinculadoInline(admin.TabularInline):    
    model = DocumentoVinculado
    max_num=0 
    can_delete = False
    fields = ('tipo_documento', 'detalle','archivo') 
    readonly_fields = ('tipo_documento', 'detalle','archivo') 

class ClubAdmin(admin.ModelAdmin):
    list_display = ['razon_social', 'ciudad', 'direccion', 'telefono', 'email']
    list_filter = ['razon_social',]
    search_fields = ['ciudad__nombre', 'razon_social'] #ver si se puede poner x q campo buscas
    inlines = [DocumentoVinculadoInline]
    readonly_fields = ['secuencia_socio']
    
    def get_queryset(self, request):
        # Obtener el organismo del usuario actual
        queryset = super().get_queryset(request)
        mi_club = request.user.club
        if (mi_club):
            queryset = queryset.filter(CUIT=mi_club.CUIT)
        return queryset
        
class DocumentoVinculadoAdmin(admin.ModelAdmin):
    list_display = ['tipo_documento', 'detalle', 'archivo']
    exclude = ['club']
    
    def get_queryset(self, request):
        # Obtener el organismo del usuario actual
        queryset = super().get_queryset(request)
        mi_club = request.user.club
        if (mi_club):
            queryset = queryset.filter(club=mi_club)
        return queryset
    
    # Permitir agregar un nuevo 'tipo_documento' desde el admin
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'tipo_documento':
            kwargs["widget"] = admin.widgets.RelatedFieldWidgetWrapper(
                db_field.formfield().widget,
                db_field.remote_field,
                admin.site,
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Filtra el campo 'club' según el club del usuario
        if db_field.name == 'club':
            mi_club = getattr(request.user, 'club', None)
            if mi_club:
                kwargs['queryset'] = Club.objects.filter(id=mi_club.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        # Asigna por defecto el club del usuario logueado
        obj.club = request.user.club
        super().save_model(request, obj, form, change)

admin.site.register(Club, ClubAdmin)
admin.site.register(DocumentoVinculado, DocumentoVinculadoAdmin)
admin.site.register(Personal, PersonalAdmin)
# admin.site.register(ProfesorDisciplina, ProfesorDisciplinaAdmin)
