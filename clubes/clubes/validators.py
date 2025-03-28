from django.core.exceptions import ValidationError
from cffi.backend_ctypes import xrange
from .errors import ERROR_CUIL_CUIT_INVALIDO, ERROR_VALOR_DESDE_HASTA, ERROR_VALOR_NEGATIVO

def validar_cuit(value):
    try:
        int(value)
    except:
        raise ValidationError(ERROR_CUIL_CUIT_INVALIDO)
    if value:
        if len(value) != 11:
            raise ValidationError(ERROR_CUIL_CUIT_INVALIDO)
        base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
        aux = 0
        for i in xrange(10):
            aux += int(value[i]) * base[i]
        aux = 11 - (aux - (int(aux / 11) * 11))
        if aux == 11:
            aux = 0
        if aux == 10:
            aux = 9
        if not aux == int(value[10]):
            raise ValidationError(ERROR_CUIL_CUIT_INVALIDO)
        

def validate_valor_desde_hasta(value):
    if value < 0 or value > 100:
        raise ValidationError(ERROR_VALOR_DESDE_HASTA)
    
def validate_valor_negativo(value):
    if value < 0:
        raise ValidationError(ERROR_VALOR_NEGATIVO)