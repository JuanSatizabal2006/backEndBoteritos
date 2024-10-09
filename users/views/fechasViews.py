from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Fechas
from ..serialzer.fechasSerizalizer import  FechasSerializer
from ..querySql import querySql

@api_view(['GET'])
def FechasEstudiantesOne(request,id):
    
    if request.method == 'GET':
        query = querySql("SELECT `usuario`.`idUsuario`, `estudiante`.`idEstudiante`, `fechas`.* FROM `usuario` LEFT JOIN `estudiante` ON `estudiante`.`idUsuario` = `usuario`.`idUsuario` LEFT JOIN `fechas` ON `fechas`.`idUsuario` = `usuario`.`idUsuario` WHERE `estudiante`.`idUsuario` = %s;",[id])
        
        if len(query) == 0:
            return Response({
                "message" : "Datos vacios",
                "error" : "Fechas no encontradas"
            }, status=status.HTTP_404_NOT_FOUND)
            
        return Response({
            "message" : "¡Datos encontrados!",
            "data" : query
        },status= status.HTTP_200_OK)

@api_view(['GET'])
def FechasProfesor(request,id):
    
    if request.method == 'GET':
        query = querySql("SELECT `profesor`.`idProfesor`, `usuario`.`idUsuario`, `fechas`.* FROM `profesor` LEFT JOIN `usuario` ON `profesor`.`idUsuario` = `usuario`.`idUsuario` LEFT JOIN `fechas` ON `fechas`.`idUsuario` = `usuario`.`idUsuario` WHERE `profesor`.`idUsuario` = %s;",[id])
        
        if len(query) == 0:
            return Response({
                "message" : "Datos vacios",
                "error" : "Fechas no encontradas"
            }, status=status.HTTP_404_NOT_FOUND)
            
        return Response({
            "message" : "¡Datos encontrados!",
            "data" : query
        },status= status.HTTP_200_OK)      
        
@api_view(['PUT'])
def FechasUpdate(request):
    if request.method == 'PUT':
        query = Fechas.objects.filter(idusuario = request.data['idusuario']).first()
        
    
        if not query:
            return Response({
                "message" : "Actualizacion cancelada",
                "error" : "Datos no encontrados"
            },status=status.HTTP_404_NOT_FOUND)
        
        srFechas = FechasSerializer(query, data = request.data)
        
        if srFechas.is_valid():
            srFechas.save()
            return Response({
                "message" : "Actualizacion de fechas con exito!",
                "data" : srFechas.data
            },status=status.HTTP_201_CREATED)
            
        return Response({
            "message" : "Actualizacion cancelada",
            "error" : srFechas.errors
        },status=status.HTTP_400_BAD_REQUEST) 