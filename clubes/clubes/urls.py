"""
URL configuration for clubes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.shortcuts import redirect

from clubes.views.indumentaria import indumentaria
from clubes.views.disciplina_indumentaria import disciplinaIndumentaria
from clubes.views.tipo_indumentaria import tipoIndumentaria
from clubes.views import asociarme
from clubes.views.contacto import contacto
from clubes.views.disciplina import disciplina
from clubes.views.historia import historia
from clubes.views.home import home
from cuotas.views import generacion_cuotas
urlpatterns = [

    path('', home, name="home"),
    path('historia', historia, name="historia"),
    path('indumentaria', indumentaria, name="indumentaria"),
    path('contacto', contacto, name="contacto"),
    path('disciplina/<int:id>/', disciplina, name="disciplina"),
    path('indumentaria/tipo/<int:id>/', tipoIndumentaria, name="tipoIndumentaria"),
    path('indumentaria/disciplina/<int:id>/', disciplinaIndumentaria, name="disciplinaIndumentaria"),
    path('asociarme', asociarme.asociarme, name="asociarme"),
    path('submitForm/', asociarme.submitForm, name='submitForm'),
    path('verificar_cuil/<str:cuil>/', asociarme.verificar_cuil, name='verificar_cuil'),
    path('verificar_dni/<str:dni>/', asociarme.verificar_dni, name='verificar_dni'),
    path('verificar_email/<str:email>/', asociarme.verificar_email, name='verificar_email'),
    path('generacion_cuotas/', generacion_cuotas, name="generacion_cuotas"),
    path('admin/', admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path('ckeditor/', include('ckeditor_uploader.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)