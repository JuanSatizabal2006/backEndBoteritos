import re

tiposDocumento = {
    "1" : {
        "min" : 8,
        "max" : 10
    },
    "2" : {
        "min" : 8,
        "max" : 10
    },
    "3" : {
        "min" : 6,
        "max" : 8
    }
}

def validateCantDocumento(numero, tipo):
    numeroLength = len(str(numero))
    min = tiposDocumento[tipo]["min"]
    max = tiposDocumento[tipo]["max"]

    if not (numeroLength >= min and numeroLength <= max):
        return {
            "error" : f"Numero de documento debe tener como minimo {min} y maximo {max} digitos" , 
            "result" : False
            }
    
    return {"result" : True}

def validateMinCaractEspecial(value, field):

    # Caso 1: Verificar que haya al menos una palabra
    if not re.match(r'^\s*[a-zA-ZÁÉÍÓÚáéíóúÑñ]+(?:\s+[a-zA-ZÁÉÍÓÚáéíóúÑñ]+)*\s*$', value):
        return {"error" : f"El {field} debe contener al menos una palabra." , "result" : False}

    # Caso 2: Verificar que no haya caracteres especiales
    if re.search(r'[^a-zA-ZÁÉÍÓÚáéíóúÑñ\s]', value):
        return {"error" : f"El {field} no puede contener caracteres especiales." , "result" : False}

    # Si pasa todas las validaciones
    return {"result" : True}

def isNumber(value):
    try:
        int(value)
        return True
    except ValueError:
        return False