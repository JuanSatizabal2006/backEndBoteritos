import pytz
import jwt
from django.conf import settings
from jwt import InvalidSignatureError, ExpiredSignatureError
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Usuario, Profesor, Admin , Estudiante, Trimestres
from .querySql import querySql
from url import urlHost

def searchRol(idrol,idusuario):
    
    if idrol == 1 :
        rol = Admin.objects.filter(idusuario = idusuario).first()
        if rol :
            return rol.idadmin
        return None
        
    if idrol == 2:
        rol = Profesor.objects.filter(idusuario = idusuario).first()
        
        if rol :
            return rol.idprofesor
        return None

    if idrol == 3 :
        rol = Estudiante.objects.filter(idusuario = idusuario).first()
        
        if rol:
            return rol.idestudiante
        return None
    
    else:
        return None

def getTrimestre():
    #Obtener fecha
    utc_now = datetime.now(pytz.utc)
    # Formatear la fecha para obtener solo año, mes y día
    fechaFormateada = utc_now.strftime("%Y-%m-%d")
        
    query = querySql("SELECT `trimestres`.* FROM `trimestres` WHERE %s BETWEEN `trimestres`.`fechaInicio` AND `trimestres`.`fechaFin`",[fechaFormateada])
    
    return query[0]['idtrimestre']

@api_view(['POST'])
def Login(request):
    
    trimestre = getTrimestre()
        
    if request.method == 'POST':
        
        documento = request.data['documento']
        contrasena = request.data['contrasena']
        
        if (not documento) or (not contrasena):
            return Response({
                "message" : "Ingreso cancelado",
                "error" : "Todos los campos son necesarios"
            },status=status.HTTP_400_BAD_REQUEST)
        #Obtener data del usuario
        usuario = Usuario.objects.filter(documento = documento).first()

        if not usuario:
            #Usuario no encontrado
            return Response({
                "message" : "Ingreso cancelado",
                "error" : "Documento o contraseña incorrectos"
            },status= status.HTTP_400_BAD_REQUEST)
        
        if not usuario.check_password(contrasena):
            #Documento no coincide con la contraseña
            return Response({
                "message" : "Ingreso cancelado",
                "error" : "Documento o contraseña no coinciden"
            })   
        
        rol = searchRol(usuario.idrol, usuario.idusuario)
        
        if not rol:
            return Response({
                "message" : "Ingreso cancelado",
                "error" : "El rol no corresponde al usuario"
            },status=status.HTTP_401_UNAUTHORIZED)
        
        utc_now = datetime.now(pytz.utc)
        
        #Creacion de token de acceso
        access_payload = {
            'idusuario': usuario.idusuario ,
            'nombre': usuario.nombre ,
            'apellido' : usuario.apellido,
            'rol' : usuario.idrol,
            'idjob' : rol,
            'img' : f'{urlHost}{usuario.imagen}',
            'exp': utc_now + timedelta(seconds=settings.JWT_ACCESS_EXPIRATION_TIME),
            'iat': utc_now
        }
        
        access_token = jwt.encode(access_payload, settings.JWT_ACCESS_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        
        #Creacion de token de refresco
        refresh_payload = {
            'idusuario': usuario.idusuario ,
            'nombre': usuario.nombre ,
            'apellido' : usuario.apellido,
            'rol' : usuario.idrol,
            'idjob' : rol,
            'img' : f'{urlHost}{usuario.imagen}',
            'exp': utc_now + timedelta(seconds=settings.JWT_REFRESH_EXPIRATION_TIME),
            'iat': utc_now
        }
        
        refresh_token = jwt.encode(refresh_payload, settings.JWT_REFRESH_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        
        return Response({
            "message" : "¡Ingreso con exito!",
            "data": {    
                "access_token" : access_token,
                "refresh_token" : refresh_token,
                'trimestre' : trimestre
            }
        },status= status.HTTP_202_ACCEPTED)
        
@api_view(['POST'])
def ValidarToken(request):
    if request.method == 'POST':
        try:
            token = request.data.get('token')            
            if not token:
                return Response({
                    "message" : "Autorizacion cancelada",
                    "error" : "El token es obligatorio"
                },status=status.HTTP_401_UNAUTHORIZED)
                
            payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
            
            fechaActual = datetime.now(pytz.utc)
            exp = payload.get('exp')
            
            if not exp:  
                return Response({
                    "message" : "Verificacion cancelada",
                    "error" : "El token no cuenta con fecha de expiracion"
                },status=status.HTTP_401_UNAUTHORIZED)
            
            fechaExp = datetime.fromtimestamp(exp, pytz.utc)
            
            #LA FECHA DE CADUCIDAD DEL TOKEN ES MENOR A LA ACTUAL?
            if fechaExp < fechaActual:
                return Response({
                    "message": "Verificacion cancelada",
                    "error" : "El token ha caducado"
                },status=status.HTTP_401_UNAUTHORIZED)
            
            #EL TOKEN NO EXPIRO
            return Response({
                "message" : "Verificacion con exito",
                "data" : payload.get('rol')
            })

        #FIRMAS INVALIDAS
        except InvalidSignatureError:
            return Response({
                    "message": "El token es invalido",
                    "error" : "El token ha caducado"
                },status=status.HTTP_401_UNAUTHORIZED)
            
        #TOKEN EXPIRADO
        except ExpiredSignatureError:
            return Response({
                    "message": "Verificacion cancelada",
                    "error" : "El token ha caducado"
                },status=status.HTTP_401_UNAUTHORIZED)