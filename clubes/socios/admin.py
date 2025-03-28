from django.contrib import admin, messages
from cuotas.models import Cuota
from .models import Socio
from disciplinas.models import SocioCategoria

class CuotaInline(admin.TabularInline):    
    model = Cuota
    max_num=0 
    can_delete = False
    fields = ('mes', 'anio','monto_base', 'monto_neto', 'fecha_vencimiento', 'pagada') 
    readonly_fields = ('mes', 'anio','monto_base', 'monto_neto', 'fecha_vencimiento', 'pagada') 

class CategoriaInline(admin.TabularInline):    
    model = SocioCategoria
    max_num=0 
    can_delete = False
    verbose_name = "Categoría inscrita"
    verbose_name_plural = "Categorías inscriptas"
    fields = ('categoria',) 
    readonly_fields = ('categoria',) 

class EstadoSocioFilter(admin.SimpleListFilter):
    title = 'Estado' 
    parameter_name = 'estado'

    def lookups(self, request, model_admin):
      
        return (
            ('True', 'Activo'),
            ('False', 'Inactivo'),
        )

    def queryset(self, request, queryset):
  
        if self.value() == 'True':
            return queryset.filter(activo=True)
        if self.value() == 'False':
            return queryset.filter(activo=False)
        return queryset

@admin.action(description="Aprobar ingreso")
def aprobar_ingreso(modeladmin, request, queryset):
    try:
        pendientes = queryset.filter(nro_socio=0)
        club = request.user.club
        nro = club.secuencia_socio
        for socio in pendientes:
            socio.nro_socio = nro + 1
            nro += 1
            socio.save()
        club.secuencia_socio = nro
        club.save()
        messages.success(request, "Socio/s aprobados exitosamente")
    
    except Exception as e:
        messages.error(request, f"Error en la aprobación de socio/s: {str(e)}")
    
    
class SocioAdmin(admin.ModelAdmin):
    list_display = ("apellido", "nombre", "nro_socio", "activo", "fecha_ingreso", "grupo_familiar", "tipo_socio")
    search_fields = ("nombre", "apellido", "nro_socio", "nro_inscripcion")
    list_filter = ("genero", EstadoSocioFilter, "club", "usa_email", "grupo_familiar")
    inlines = [CuotaInline, CategoriaInline]
    actions = [aprobar_ingreso]
    fieldsets = [
        ("Información Personal", {
            'fields': [
                "nombre", "apellido", 
                "fecha_nacimiento", 
                "tipo_documento",
                "nro_documento", 
                "CUIL",
                "genero",
                "grupo_familiar"
            ]
        }),
        ("Información de Contacto", {
            'fields': [
                "ciudad", 
                "direccion", 
                "nro_telefono", 
                "email_socio",
                "usa_email",
            ],
        }),
        ("Datos del Club", {
            'fields': [
                "nro_socio",
                "activo", 
                "tipo_socio",
                "fecha_ingreso", 
                "fecha_egreso"
            ],
        }),
        ("Datos del Responsable", {
            'fields': [
                "responsable", 
                "tel_responsable", 
                "email_responsable"
            ],
        }),
        ("Información de Salud", {
            'fields': [
                "cobertura", "nro_cobertura", "medico", 
                "grupo_sanguineo", 
                "peso", "altura", 
                "enfermedades_cronicas", 
                "enfermedades_infancia", 
                "enfermedades_huesos",
                "enfermedades_nerviosas",
                "enfermedades_digestivas",
                "vacunas", 
                "dificultades", 
                "alergias", 
                "medicaciones"
            ],
        }),
        ("Datos Escolares", {
            'fields': [
                "escuela", 
                "año_escolar", 
                "turno_escolar", 
                "tipo_contacto_escolar",
                "nombre_contacto_escolar",
                "telefono_contacto_escolar",
                "email_contacto_escolar"
            ],
        }),
    ]
    def save_model(self, request, obj, form, change):
        # Asigna por defecto el club del usuario logueado
        obj.club = request.user.club
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
    
        # Si el usuario es un superusuario, mostramos todo
        if request.user.is_superuser:
            return queryset
    
         # Si el usuario no es superusuario, mostramos asociados al club
        try:
            mi_club = request.user.club  
            if mi_club:
                queryset = queryset.filter(club=mi_club)
        except AttributeError:
            # Si no se encuentra el club en el usuario, no se muestra nada
            queryset = queryset.none()
    
        return queryset

    def save_model(self, request, obj, form, change):
        obj.full_clean()  # Llama al método `clean` del modelo para realizar validaciones
        super().save_model(request, obj, form, change)

admin.site.register(Socio, SocioAdmin)
