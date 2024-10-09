from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..models import Responsable
from ..serialzer.responsableSerializer import ResponsableSerializer
from ..querySql import querySql

@api_view(['GET'])
def ResponsableOne(request, id):
    if request.method == 'GET':
        
        query = querySql("SELECT `responsable`.`nombre`, `responsable`.`idResponsable` , `responsable`.`apellido`, `responsable`.`correo`, `responsable`.`numeroDocumento`, `responsable`.`telefono`, `responsable`.`profesion`, `responsable`.`ocupacion`, `responsable`.`empresa`, `responsable`.`idTipoParentesco`, `tipoparentesco`.`tipoParentesco`, `responsable`.`idTipoDocumento`, `tipodocumento`.`tipoDocumento`, `responsable`.`idSexo`, `sexo`.`sexo` FROM `responsable` LEFT JOIN `tipoparentesco` ON `responsable`.`idTipoParentesco` = `tipoparentesco`.`idTipoParentesco` LEFT JOIN `tipodocumento` ON `responsable`.`idTipoDocumento` = `tipodocumento`.`idTipoDocumento` LEFT JOIN `sexo` ON `responsable`.`idSexo` = `sexo`.`idSexo` WHERE `responsable`.`idEstudiante` = %s;", [id])
        
        if len(query) == 0:
            return Response({
                "message" : "Consulta realizada",
                "error" : "Datos no encontrados"
            },status=status.HTTP_404_NOT_FOUND)
            
        return Response({
            "message" : "Datos encontrados",
            "data" : query
        },status=status.HTTP_200_OK)

@api_view(['POST', 'PUT'])
def ResponsableView(request):
    
    if request.method == 'POST':
        datos = request.data
        srResponsable = ResponsableSerializer(data = datos)
        
        if srResponsable.is_valid():
            srResponsable.save()
            return Response({
                "message" : "Creacion del responsable realizada con exito",
                "error" : srResponsable.data
            }, status=status.HTTP_201_CREATED)
         
        return Response({
            "message" : "Creacion del responsable cancelada",
            "error" : srResponsable.errors
        },status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'PUT':
        
        if not request.data['idresponsable']:
            return Response({
                "message" : "Actualizacion cancelada",
                "error" : "Falta el ID del estudiante"
            })
            
        query = Responsable.objects.filter(idresponsable = request.data['idresponsable']).first()
        
        if not query:
            return Response({
                "message" : "Actualizacion cancelada",
                "error" : "Datos no encontrados"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        srResponsable = ResponsableSerializer(query, data = request.data)
        
        if srResponsable.is_valid():
            srResponsable.save()
            return Response({
                "message" : "¡Actualizacion realizada con exito!",
                "data" : srResponsable.data
            },status=status.HTTP_201_CREATED)

        return Response({
            "message" : "Actualizacion cancelada",
            "error": srResponsable.errors
        },status=status.HTTP_400_BAD_REQUEST)