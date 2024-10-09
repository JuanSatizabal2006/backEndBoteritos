from .models import Usuario
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

def validateIdUsuario(idUsuario):
    oneUser = Usuario.objects.filter(idusuario = idUsuario).first()
    #Validar que el usuario existe
    if not oneUser:
        return {
            "result" : False,
            "message" : {"message": "No encontrado", "error" : "No se encontró al usuario"},
            "status" :  status.HTTP_404_NOT_FOUND
        }
    
    return {"result" : True , "user" : oneUser}

@api_view(['GET'])
def searchDocument(request, doc):
    
    if request.method == 'GET':
        oneUser = Usuario.objects.filter(documento = doc).first()
        #Validar que el usuario existe
        if oneUser:
            return Response({
                "message" : "Creacion cancelada",
                "error" : "Documento ya existe"
            },status=status.HTTP_400_BAD_REQUEST)
            
        return Response({
            "message" : "¡Documento no existe!, puede continuar"
        },status=status.HTTP_200_OK)