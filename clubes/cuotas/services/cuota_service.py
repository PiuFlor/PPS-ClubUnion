from datetime import date, datetime, timedelta
from socios.models import Socio
from cuotas.models import Cuota, EsquemaCuotaDeportiva, EsquemaCuotaSocial
from disciplinas.models import SocioCategoria

class CuotaService:
    
    @staticmethod
    def generar_cuota_deportiva(mes, anio):   
        errores = []
        esq_cuota_error = []
        #socio activos con categorias activas
        socios_categoria = SocioCategoria.objects.filter(categoria__estado = True, socio__activo= True).order_by('socio__fecha_ingreso')
        #chequea q haya esq_Cuota para esas categorias
        if not socios_categoria:
            return {
                'success': False,
                'mensaje_error': "No hay socios inscriptos en categorias"
            }
        existenEsqCuotaDeportiva(socios_categoria, esq_cuota_error, errores)
        if errores:
            return {
                'success': False,
                'mensaje_error': "Ocurrio un error:\n" + "\n".join(errores)
            }

        #crea cuota
        for c in socios_categoria:
            #chequea q no haya cuota creada de esa disc, para ese socio en ese periodo
            if Cuota.objects.filter(socio= c.socio, mes=mes, anio=anio, disciplina= c.categoria.disciplina).exists():
                continue
            esquema_cuota = esquemaCuotaDeportiva(c.categoria)

            num_grupo_fliar = c.socio.grupo_familiar
            descuento = 0
            # los socios con el mismo num de grupo_fliar, q practiquen igual disciplina, ordenados por fecha_ingreso
            tipo_socio = None
            if num_grupo_fliar:
                grupo_fliar = SocioCategoria.objects.filter(
                        socio__grupo_familiar=c.socio.grupo_familiar,
                        categoria__disciplina = c.categoria.disciplina
                    ).order_by('socio__fecha_ingreso')
                indice_socio = 1
                
                for socio in grupo_fliar:
                    
                    esquema_cuota = esquemaCuotaDeportiva(socio.categoria)
                    if(indice_socio == 2):
                        descuento = esquema_cuota.descuento_x_2
                    if(indice_socio == 3):
                        descuento = esquema_cuota.descuento_x_3
                    if (indice_socio >= 4):
                        descuento = esquema_cuota.descuento_x_4
                    generarCuota(mes, anio, esquema_cuota, descuento, socio.socio, c.categoria.disciplina, tipo_socio, errores)
                    indice_socio+=1
               
            else:
                generarCuota(mes, anio, esquema_cuota, descuento, c.socio, c.categoria.disciplina, tipo_socio, errores)
        if errores:
            return {
                'success': False,
                'mensaje_error': "Algunas cuotas no se pudieron generar:\n" + "\n".join(errores)
            }
        return {'success': True, 'mensaje': f"Se han generado con éxito todas las cuotas del periodo: {mes}/{anio}"}

    
    @staticmethod
    def generar_cuota_social(mes, anio):
        errores = []
        esq_cuota_error = []
        socios_activos = Socio.objects.filter(activo=True).order_by('fecha_ingreso')
        #chequea q haya esq_Cuota para esos tipo_socios
        existenEsqCuotaSocial(socios_activos, esq_cuota_error, errores)
        if errores:
            return {
                'success': False,
                'mensaje_error': "Ocurrio un error:\n" + "\n".join(errores)
            }
       
        for socio in socios_activos:
            #chequea si es vitalicio no le cobra cuota social
            anio_actual = date.today().year
            if anio_actual-socio.fecha_ingreso.year >= 25:
                continue
            #chequea q no haya cuota creada de ese tipo socio, para ese socio en ese periodo
            if Cuota.objects.filter(socio = socio, mes =mes, anio = anio, tipo_socio = socio.tipo_socio.id).exists():

                continue
            esquema_cuota = esquemaCuotaSocial(socio.tipo_socio)
            
            num_grupo_fliar = socio.grupo_familiar
           
            descuento = 0
            disciplina = None
            # los socios con el mismo num de grupo_fliar, ordenados por fecha_ingreso
            if num_grupo_fliar:
             
                grupo_fliar = Socio.objects.filter(
                        grupo_familiar=socio.grupo_familiar,
                        activo = True
                    ).order_by('fecha_ingreso')
            
                indice_socio = 1
                
                for socio in grupo_fliar:
                    esquema_cuota = esquemaCuotaSocial(socio.tipo_socio)
                    if(indice_socio == 2):
                        descuento = esquema_cuota.descuento_x_2
                    if(indice_socio == 3):
                        descuento = esquema_cuota.descuento_x_3
                    if (indice_socio >= 4):
                        descuento = esquema_cuota.descuento_x_4
                    
                    generarCuota(mes, anio, esquema_cuota, descuento, socio, disciplina, socio.tipo_socio, errores)
                    indice_socio+=1
               
            else:
                generarCuota(mes, anio, esquema_cuota, descuento, socio, disciplina,  socio.tipo_socio, errores)
        

        if errores:
            return {
                'success': False,
                'mensaje_error': "Algunas cuotas no se pudieron generar:\n" + "\n".join(errores)
            }
        return {'success': True, 'mensaje': f"Se han generado con éxito todas las cuotas del periodo: {mes}/{anio}"}

        
def generarCuota(mes, anio, esquema_cuota, descuento, socio, disciplina, tipo_socio, errores):
    if esquema_cuota.dias_vencimiento:
        fecha_vto = calcular_fecha_vto(mes, anio, esquema_cuota)
    else: 
       fecha_vto = None
    descuento = descuento/100
    monto = esquema_cuota.monto
    try: 
        nueva_cuota = Cuota(
            disciplina=disciplina,
            tipo_socio = tipo_socio,
            mes = mes,
            anio = anio,
            fecha_vencimiento = fecha_vto,
            socio = socio,  
            monto_base= monto,
            monto_neto = monto - (monto*descuento),
            pagada = False
        )
        nueva_cuota.save()
    except Exception as e:
        errores.append(f"Error al crear la cuota para '{socio}': {str(e)}")

def existenEsqCuotaDeportiva(socios, esq_cuota_error, errores):
    for c in socios:
        esquema_cuota = esquemaCuotaDeportiva(c.categoria)
        if not esquema_cuota:
            # para no repetir la categoria q no tiene esq.cuota creada
            if c.categoria not in esq_cuota_error:
                esq_cuota_error.append(c.categoria)
                errores.append(f"No hay Esquema Cuota creado para la categoria {c.categoria} ")
            continue
   
def existenEsqCuotaSocial(socios, esq_cuota_error, errores):
    for socio in socios:
        
        esquema_cuota = esquemaCuotaSocial(socio.tipo_socio)
        if not esquema_cuota:
            # para no repetir el tipo de socio q no tiene esq.cuota creada
            if socio.tipo_socio not in esq_cuota_error:
                esq_cuota_error.append(socio.tipo_socio)
                errores.append(f"No hay Esquema Cuota creado para el tipo de socio {socio.tipo_socio} ")
            continue


def calcular_fecha_vto(mes, anio, esquema_cuota):
    try:
        mes = int(mes)
        anio = int(anio)
        fecha_inicial = datetime(anio, mes, 1)
        fecha_vencimiento = fecha_inicial + timedelta(days=esquema_cuota.dias_vencimiento-1)
        return fecha_vencimiento
    except ValueError as e:
        return None

def esquemaCuotaSocial(tipo):
    try:
        return EsquemaCuotaSocial.objects.get(tipo_socio=tipo)
    except EsquemaCuotaSocial.DoesNotExist:
        return None 


def esquemaCuotaDeportiva(categoria):
    try:
        return EsquemaCuotaDeportiva.objects.get(categoria=categoria)
    except EsquemaCuotaDeportiva.DoesNotExist:
        return None 
