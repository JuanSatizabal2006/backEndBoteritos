from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..models import Telefonos
from ..serialzer.telefonosSerializer import TelefonosSerializer
from ..querySql import querySql

@api_view(['GET'])
def TelefonosEstudiante(request,id):
    
    if request.method == 'GET':
        query = querySql("SELECT `usuario`.`idUsuario`, `estudiante`.`idEstudiante`, `telefonos`.`telefono1`, `telefonos`.`telefono2`, `telefonos`.`idTelefonos` FROM `usuario` LEFT JOIN `estudiante` ON `estudiante`.`idUsuario` = `usuario`.`idUsuario` LEFT JOIN `telefonos` ON `telefonos`.`idUsuario` = `usuario`.`idUsuario` WHERE ( (`telefonos`.`telefono1` IS NOT NULL) AND (`telefonos`.`telefono1` IS NOT NULL) AND `estudiante`.`idUsuario` = %s);", [id])
        
        if len(query) == 0:
            return Response({
                "message" : "Telefonos no encontrados",
                "error" : "Datos vacios"
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            "message" : "Telefonos encontrados",
            "data" : query
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
def TelefonosProfesor(request,id):
    
    if request.method == 'GET':
        query = querySql("SELECT `profesor`.`idProfesor`, `usuario`.`idUsuario`, `telefonos`.* FROM `profesor` LEFT JOIN `usuario` ON `profesor`.`idUsuario` = `usuario`.`idUsuario` LEFT JOIN `telefonos` ON `telefonos`.`idUsuario` = `usuario`.`idUsuario` WHERE `profesor`.`idUsuario` = %s;", [id])
        
        if len(query) == 0:
            return Response({
                "message" : "Telefonos no encontrados",
                "error" : "Datos vacios"
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            "message" : "Telefonos encontrados",
            "data" : query
        }, status=status.HTTP_200_OK) 
        
@api_view(['PUT'])
def TelefonosUpdate(request):
            
    if request.method == 'PUT':
        query = Telefonos.objects.filter(idusuario = request.data['idusuario']).first()
        
        if not query:
            return Response({
                "message" : "Actualizacion cancelada",
                "error" : "Datos no encontrados"
            },status=status.HTTP_404_NOT_FOUND)
        
        srTelefonos = TelefonosSerializer(query, data = request.data)
        
        if srTelefonos.is_valid():
            srTelefonos.save()
            return Response({
                "message" : "Actualizacion de telefonos con exito!",
                "data" : srTelefonos.data
            },status=status.HTTP_201_CREATED)
            
        return Response({
            "message" : "Actualizacion cancelada",
            "error" : srTelefonos.errors
        },status=status.HTTP_400_BAD_REQUEST) 