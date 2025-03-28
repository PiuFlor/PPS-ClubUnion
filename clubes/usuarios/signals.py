from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from club.models.club import Club
from club.models.documento_vinculado import DocumentoVinculado
from club.models.personal import Personal
from socios.models import Socio
from disciplinas.models import Disciplina, Categoria, Horario, ProfesorCategoria, SocioCategoria
from cuotas.models import EsquemaCuotaDeportiva, EsquemaCuotaSocial, Cuota, Pago
from eventos.models import Evento
from intervenciones.models import Intervencion
from notificaciones.models import Mensaje
from movimientos.models import Ingreso, Egreso
from indumentaria.models import TipoArticulo, Articulo

@receiver(post_migrate)
def create_groups_with_permissions(sender, **kwargs):
    try:
        # Definir los grupos y sus permisos
        grupos_y_permisos = {
            'Administrador de Club': [
                ('change_club', Club),
                ('delete_club', Club),
                ('view_club', Club),
                 ('change_documentovinculado', DocumentoVinculado),
                ('delete_documentovinculado', DocumentoVinculado),
                ('add_documentovinculado', DocumentoVinculado),
                ('change_personal', Personal),
                ('delete_personal', Personal),
                ('add_personal', Personal),
                 ('change_socio', Socio),
                ('delete_socio', Socio),
                ('add_socio', Socio),
                
            ],
            'Administrador de Disciplinas': [
                ('add_disciplina', Disciplina),
                ('change_disciplina', Disciplina),
                ('delete_disciplina', Disciplina),
                ('add_categoria', Categoria),
                ('change_categoria', Categoria),
                ('delete_categoria', Categoria),
                ('add_horario', Horario),
                ('change_horario', Horario),
                ('delete_horario', Horario),
                ('add_profesorcategoria', ProfesorCategoria),
                ('change_profesorcategoria', ProfesorCategoria),
                ('delete_profesorcategoria', ProfesorCategoria),
                ('add_sociocategoria', SocioCategoria),
                ('change_sociocategoria', SocioCategoria),
                ('delete_sociocategoria', SocioCategoria),
              
            ],
            'Administrador de Disciplina Propia': [
                ('view_disciplina', Disciplina),
                ('add_categoria', Categoria),
                ('change_categoria', Categoria),
                ('delete_categoria', Categoria),
                ('add_horario', Horario),
                ('change_horario', Horario),
                ('delete_horario', Horario),
                ('add_profesorcategoria', ProfesorCategoria),
                ('change_profesorcategoria', ProfesorCategoria),
                ('delete_profesorcategoria', ProfesorCategoria),
                ('add_sociocategoria', SocioCategoria),
                ('change_sociocategoria', SocioCategoria),
                ('delete_sociocategoria', SocioCategoria),
            ],
            'Administrador de Cuotas': [
                ('add_esquemacuotadeportiva', EsquemaCuotaDeportiva),
                ('delete_esquemacuotadeportiva',EsquemaCuotaDeportiva),
                ('change_esquemacuotadeportiva',EsquemaCuotaDeportiva),
                ('add_esquemacuotasocial', EsquemaCuotaSocial),
                ('delete_esquemacuotasocial',EsquemaCuotaSocial),
                ('change_esquemacuotasocial',EsquemaCuotaSocial),
                ('add_cuota', Cuota),
                ('delete_cuota', Cuota),
                ('change_cuota',Cuota),
                ('add_pago', Pago),
                ('delete_pago', Pago),
                ('change_pago', Pago),
            ],
            'Vista de Cuotas': [
                ('view_esquemacuotadeportiva', EsquemaCuotaDeportiva),
                ('view_esquemacuotasocial', EsquemaCuotaSocial),
                 ('view_cuota', Cuota),
                ('view_pago', Pago),
                
            ],
            'Administrador de Eventos': [
                ('add_evento', Evento),
                ('delete_evento', Evento),
                ('change_evento', Evento),
            ],

              'Vista de Eventos': [
                ('view_evento', Evento),
                
            ],
             'Administrador de Intervenciones': [
                ('add_intervencion', Intervencion),
                ('delete_intervencion', Intervencion),
                ('change_intervencion', Intervencion),
            ],

              'Vista de Intervenciones': [
                ('view_intervencion', Intervencion),
                
            ],
            'Administrador de Notificaciones': [
                ('add_mensaje', Mensaje),
                ('delete_mensaje', Mensaje),
                ('change_mensaje', Mensaje),
            ],

              'Vista de Notificaciones': [
                ('view_mensaje', Mensaje),
                
            ],
            
             'Administrador de Movimientos Disciplinas': [
                ('add_ingreso', Ingreso),
                ('delete_ingreso', Ingreso),
                ('change_ingreso', Ingreso),
                ('add_egreso', Egreso),
                ('delete_egreso', Egreso),
                ('change_egreso', Egreso),
            ],

              'Vista de Movimientos Disciplinas': [
                ('view_ingreso', Ingreso),
                ('view_egreso', Egreso),
            ],
            'Administrador de Indumentaria': [
                ('add_tipoarticulo', TipoArticulo),
                ('delete_tipoarticulo', TipoArticulo),
                ('change_tipoarticulo', TipoArticulo),
                ('add_articulo', Articulo),
                ('delete_articulo', Articulo),
                ('change_articulo', Articulo),
                
            ],

              'Vista de Indumentaria': [
                ('view_tipoarticulo', TipoArticulo),
                  ('view_articulo', Articulo),
            ],
        }

        for grupo, permisos in grupos_y_permisos.items():
            group, created = Group.objects.get_or_create(name=grupo)

            if created:
                permisos_a_agregar = []
                for codename, model in permisos:
                    content_type = ContentType.objects.get_for_model(model)
                    permiso, _ = Permission.objects.get_or_create(codename=codename, content_type=content_type)
                    permisos_a_agregar.append(permiso)

                # Asignar permisos al grupo
                group.permissions.set(permisos_a_agregar)

    except Exception as e:
        print(f"Error al crear grupos y permisos: {e}")
