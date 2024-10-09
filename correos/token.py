import jwt
from jwt import InvalidSignatureError, ExpiredSignatureError
import pytz
from django.conf import settings
from datetime import datetime, timedelta

def CreateToken(id):
    
    utc_now = datetime.now(pytz.utc)

    payload = {
        'idusuario': id,
        'exp': utc_now + timedelta(seconds=settings.JWT_ACCESS_EXPIRATION_TIME),
        'iat': utc_now
    }
    
    token = jwt.encode(payload, settings.JWT_ACCESS_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    
    return token

def ValidateToken(token):
    #DECODIFICAMOS EL TOKEN
    try:
        
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        
        fechaActual = datetime.now(pytz.utc)
        exp = payload.get('exp')
        
        if not exp:  
            return {"valid" : False, "message" : "El token no cuenta con fecha de expiracion"}
        
        fechaExp = datetime.fromtimestamp(exp, pytz.utc)
        
        #LA FECHA DE CADUCIDAD DEL TOKEN ES MENOR A LA ACTUAL?
        if fechaExp < fechaActual:
            return {'valid': False, 'message': 'El token ha caducado'}
        
        #EL TOKEN NO EXPIRO
        return {'valid': True, 'payload': payload}

    #FIRMAS INVALIDAS
    except InvalidSignatureError:
        return {"valid" : False, "message" : "El token es invalido"}
    #TOKEN EXPIRADO
    except ExpiredSignatureError:
        return {"valid" : False, "message" : "El token ha caducado"}
    
    
    