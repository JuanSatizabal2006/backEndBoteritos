from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import Usuario
from .token import CreateToken, ValidateToken
from .serializers import UsuarioSerializer

def GenerarCorreos(asunto, texto, nombre, email,token):
    
    html_content = render_to_string('recupContra.html', {
        'mensaje': texto,
        'nombre' : nombre,
        'token' : token
    })
    #ASUNTO, MENSAJE, CORREO DE ENVIO, CORREOS QUE RECIBEN
    #ENVIAMOS EL CORREO
    send_mail(asunto, None, None, [email], html_message=html_content)
        
def EncriptarCorreo(correo):
    #DIVISIONES DEL CORREO
    arrayCorreo = correo.split('@')
    #OBTENCION DE DATOS
    correoTxt = arrayCorreo[0]
    type = arrayCorreo[1]
    letrasVis = correoTxt[:3]
    
    #ANADIMOS LOS *
    encriptado = f"{letrasVis}{'*'* (len(correoTxt) - 3 ) }"
        
    return f"{encriptado}@{type}" 
    
@api_view(['PUT'])
def RecuperarContrasena(request):
    
    if request.method == 'PUT':
        
        documento = request.data.get('documento')
        
        query = Usuario.objects.filter(documento = documento).first()
        
        if not query:
            return Response({
                "message" : "Cambio de contraseña cancelado",
                "error" : "Documento no encontrado"
            },status=status.HTTP_404_NOT_FOUND)
        
        correo = query.correo
        #Encriptacion del correo
        correoEncriptado = EncriptarCorreo(correo)
        #VARIABLES PARA EL CORREO
        asunto = "Recuperacion de contraseña"
        nombre = f"{query.nombre} {query.apellido}"
        texto = "Haz clic en el enlace de abajo para recuperar tu contraseña y poder iniciar sesión"
        
        token = CreateToken(query.idusuario)
        
        GenerarCorreos(asunto,texto,nombre,correo,token)
        
        return Response({
            "message" : "Correo enviado con exito!" ,
            "data" : {
                "correo" : correoEncriptado
            }
        },status=status.HTTP_200_OK)

@api_view(['PUT'])
def CambiarContrasena(request):
    
    if request.method == 'PUT':
        idUsuario = request.data.get('idusuario')
        contrasena = request.data.get('contrasena')
        nuevaContra = request.data.get('nuevacontrasena')
        
        if not idUsuario:
            return Response({
                "message" : "Cambio de contraseña cancelado",
                "error": {
                    "idusuario" : "El id del usuario es obligatorio"
                    }
            },status=status.HTTP_400_BAD_REQUEST)
            
        if not contrasena:
            return Response({
                "message" : "Cambio de contraseña cancelado",
                "error" : {
                    "contrasena" : "La contraseña es obligatoria"
                }
            },status=status.HTTP_400_BAD_REQUEST)
        
        if not nuevaContra:
            return Response({
                "message" : "Cambio de contraseña cancelado",
                "error" : {
                    "nuevacontrasena" : "La nueva contraseña es obligatoria"
                }
            })
            
        #VALIDAMOS QUE LA NUEVA CONTRASENA NO SEA IGUAL A LA ANTERIOR
        if contrasena == nuevaContra:
            return Response({
                "message" : "Cambio de contraseña cancelado",
                "error" : "La nueva contraseña no puede ser igual a la actual"
            },status=status.HTTP_400_BAD_REQUEST)
        
        query = Usuario.objects.filter(idusuario = idUsuario).first()
        
        #USUARIO NO ENCONTRADO
        if not query:
            return Response({
                "message" : "Cambio de contraseña cancelado",
                "error" : "Usuario no encontrado"
            },status=status.HTTP_400_BAD_REQUEST)
            
        checkContra = query.check_password(contrasena)
        
        #CONTRASENA INCORRECTA
        if not checkContra:
            return Response({
                "message" : "Cambio de contraseña cancelado",
                "error" : "Contraseña incorrecta"
            },status=status.HTTP_400_BAD_REQUEST)
        
        srUsuario = UsuarioSerializer(query, data = {"contrasena" : nuevaContra}, partial = True)
        
        if srUsuario.is_valid():
            srUsuario.save() 
            
            return Response({
                "message" : "Contraseña cambiada con exito"
            },status=status.HTTP_200_OK)
        
        return Response({
            "message" : "Cambio de contraseña cancelado",
            "error" : srUsuario.errors
        },status=status.HTTP_400_BAD_REQUEST)
        


#ENDPOINT QUE CAMBIA LA CONTRASENA
@api_view(['PUT'])
def ActualizarContrasena(request):
    if request.method == 'PUT':
        token = request.data.get('token')
        #VALIDAR QUE EL TOKEN ESTE PRESENTE
        if not token:
            return Response({
                "message" : "Cambio de contraseña cancelado",
                "error" : "El token es obligatorio"
            },status=status.HTTP_400_BAD_REQUEST)
        
        tokenValid = ValidateToken(token)
        
        #EL TOKEN ES INVALIDO
        if not tokenValid['valid']:
            return Response({
               "message" : "Cambio de contraseña cancelado",
               "error" : tokenValid['message'] 
            },status=status.HTTP_400_BAD_REQUEST)
        
        idUsuario = tokenValid.get('payload').get('idusuario')
        #BUSCAMOS AL USUARIO  
        query = Usuario.objects.filter(idusuario = idUsuario).first()
        
        if not query:
            return Response({
                "message" : "Cambio de contraseña cancelada",
                "error" : "Usuario no existe"
            },status=status.HTTP_400_BAD_REQUEST)
        
        srUsuario = UsuarioSerializer(query, data = request.data, partial = True)
        
        if not srUsuario.is_valid():
            return Response({
                "message" : "Actualizacion de contrasena cancelada",
                "error" : srUsuario.errors
            },status=status.HTTP_400_BAD_REQUEST)
        #ACTUALIZAMOS LA CONTRASENA
        srUsuario.save()
        
        return Response({
            "message" : "Cambio de contraseña realizado con exito",
            "data" : srUsuario.data
        },status=status.HTTP_200_OK)