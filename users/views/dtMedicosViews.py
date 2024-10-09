from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..models import Datosmedicos
from ..serialzer.datosMedicosSerializer import DatosMedicosSerializer
from ..querySql import querySql

@api_view(['GET'])
def DatosMedicosEstudianteOne(request,id):
    if request.method == 'GET':
        query = querySql("SELECT `usuario`.`idUsuario`,`datosmedicos`.`idDatosMedicos`, `estudiante`.`idEstudiante`, `datosmedicos`.`lugarAtencion`,`datosmedicos`.`peso`,`datosmedicos`.`altura`,`datosmedicos`.`idRh`, `rh`.`rh`,`datosmedicos`.`idEps`, `eps`.`eps` FROM `usuario` LEFT JOIN `estudiante` ON `estudiante`.`idUsuario` = `usuario`.`idUsuario` LEFT JOIN `datosmedicos` ON `datosmedicos`.`idUsuario` = `usuario`.`idUsuario` LEFT JOIN `rh` ON `datosmedicos`.`idRh` = `rh`.`idRh` LEFT JOIN `eps` ON `datosmedicos`.`idEps` = `eps`.`idEps` WHERE `estudiante`.`idUsuario` = `usuario`.`idUsuario` AND `estudiante`.`idEstudiante` = %s;",[id])
        
        if len(query) == 0:
            return Response({
                "message" : "Datos vacios",
                "error" : "Datos no encontrados"
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            "message" : "¡Datos encontrados!",
            "data" : query
        }, status=status.HTTP_200_OK)
        
@api_view(['GET'])
def DatosMedicosProfesor(request,id):
    if request.method == 'GET':
        query = querySql("SELECT `profesor`.`idProfesor`, `usuario`.`idUsuario`, `datosmedicos`.*, `eps`.*, `rh`.* FROM `profesor` LEFT JOIN `usuario` ON `profesor`.`idUsuario` = `usuario`.`idUsuario` LEFT JOIN `datosmedicos` ON `datosmedicos`.`idUsuario` = `usuario`.`idUsuario` LEFT JOIN `eps` ON `datosmedicos`.`idEps` = `eps`.`idEps` LEFT JOIN `rh` ON `datosmedicos`.`idRh` = `rh`.`idRh` WHERE `profesor`.`idProfesor` = %s;",[id])
        
        if len(query) == 0:
            return Response({
                "message" : "Datos vacios",
                "error" : "Datos no encontrados"
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            "message" : "¡Datos encontrados!",
            "data" : query
        }, status=status.HTTP_200_OK)

@api_view(['PUT'])
def DatosMedicosUpdate(request):
            
    if request.method == 'PUT':
        query = Datosmedicos.objects.filter(idusuario = request.data['idusuario']).first()
        
        if not query:
            return Response({
                "message" : "Actualizacion cancelada",
                "error" : "Datos no encontrados"
            },status=status.HTTP_404_NOT_FOUND)
        
        srDatosMedicos = DatosMedicosSerializer(query, data = request.data)
        
        if srDatosMedicos.is_valid():
            srDatosMedicos.save()
            return Response({
                "message" : "Actualizacion de datos medicos con exito!",
                "data" : srDatosMedicos.data
            },status=status.HTTP_201_CREATED)
            
        return Response({
            "message" : "Actualizacion cancelada",
            "error" : srDatosMedicos.errors
        },status=status.HTTP_400_BAD_REQUEST) 