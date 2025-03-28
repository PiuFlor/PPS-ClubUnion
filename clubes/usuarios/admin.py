from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import UsuarioExtendido

class UsuarioExtendidoAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Si el campo de la contraseña ha cambiado, usamos el método set_password
        if obj.password:
            obj.password = make_password(obj.password)  # Hasheamos la contraseña antes de guardarla
        obj.save()

admin.site.register(UsuarioExtendido, UsuarioExtendidoAdmin)
