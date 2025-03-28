from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages
from .services.cuota_service import CuotaService


def generacion_cuotas(request):
    anio_actual = datetime.now().year - 1
    if request.method == 'POST':
        tipo_cuota = request.POST.get('tipo_cuota')
        mes = request.POST.get('mes')
        anio = request.POST.get('anio')
        resultado = None
        try:
            if tipo_cuota == "dep":
                resultado = CuotaService.generar_cuota_deportiva(mes, anio)
                
                #messages.success(request, resultado)
            elif tipo_cuota == "soc":
                
                resultado = CuotaService.generar_cuota_social(mes, anio)
                #messages.success(request, resultado)
            else:
                raise ValueError("Tipo de cuota no válido.")

            #return JsonResponse({'success': True, 'redirect_url': '/admin/club/cuota/'})
            if resultado['success']:
                messages.success(request, resultado['mensaje'])
                return JsonResponse({'success': True, 'redirect_url': '/admin/cuotas/cuota/'})
            else:
                
                return JsonResponse({
                    'success': False,
                    'mensaje_error': resultado['mensaje_error']
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'mensaje_error': f"Hubo un error al generar las cuotas: {str(e)}"
            })
    return render(request, 'generacion_cuotas.html', {'anio' : anio_actual})
