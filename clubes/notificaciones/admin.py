from django.contrib import admin
from django.contrib import admin, messages
from clubes.enviarNotificacion import enviar
from .models import Mensaje


@admin.action(description="Enviar mensajes")
def enviar_mensajes(modeladmin, request, queryset):
    for obj in queryset:
        res = enviar(obj)

        if res == 'OK':
            messages.success(request, f"El mensaje '{obj.referencia}' ha sido enviado correctamente.")
        else:
            messages.error(request, res)

class MensajeAdmin(admin.ModelAdmin):
    list_display = ['referencia', 'fecha', 'estado']
    list_filter = ['estado', 'disciplina', 'categoria']
    search_fields = ['referencia', 'texto']
    actions = [enviar_mensajes]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        mi_club = request.user.club
        if (mi_club):
            queryset = queryset.filter(club=mi_club)
        return queryset

admin.site.register(Mensaje, MensajeAdmin)
