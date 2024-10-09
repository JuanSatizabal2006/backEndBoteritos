from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..serializers.logrosSerializer import CalificarSerializer
from ..models import Logros, Estudiante, Logroestudiante
       
#LOGROS YA APROBADOS LISTOS PARA QUE SEAN CALIFICADOS
@api_view(['GET'])
def CalificarList(request,idtrim,idprof,idestud):
    
    if request.method == 'GET':
        getLogros = Logros.objects.filter(idprofesor = idprof, idtrimestre = idtrim)
        
        #NO SE ENCONTRARON LOGROS CORRESPONDIENTES AL TRIMESTRE        
        if len(getLogros) == 0:
            return Response({
                "messsage" : "No se puede calificar",
                "errro" : "No hay logros creados"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Obtener los IDs de los logros creados por el profesor
        logros_ids = getLogros.values_list('idlogro', flat=True)
  
      
        # Filtrar los Logroestudiante que están relacionados con los logros creados por el profesor
        query = Logroestudiante.objects.filter(idlogro__in=logros_ids, idestudiante = idestud, estado = 0)
        
        #VALIDAR QUE PARA DICHO ESTUDIANTE EXISTA LOGROS APROBADOS
        if len(query) == 0:
            return Response({
                "message" : "No se puede calificar",
                "error" : "No hay logros aceptados para ser calificados o al estudiante que deseas calificar no existe"
            },status=status.HTTP_404_NOT_FOUND)
        
        # Serializar los datos
        serializer = CalificarSerializer(query, many=True)
        
        return Response(serializer.data)
    
@api_view(['PUT'])
def CalificarSave(request):
    
    if request.method == 'PUT':
        
        arrrayLogros = request.data['logros']
            
        for value in arrrayLogros:
            
            query = Logroestudiante.objects.filter(idlogroestudiante = value['idlogroestudiante'], idestudiante = value['idestudiante']).first()
            
            if not query:
                
                return Response({
                    "message" : "Calificacion cancelada",
                    "error" : "Logro no existe" 
                },status=status.HTTP_400_BAD_REQUEST)
                
            srCalificar = CalificarSerializer(query, data = value)
        
            if srCalificar.is_valid():
        
                srCalificar.save()
        
        return Response({
            "message" : "Calificacion realizada con exito"
        },status=status.HTTP_200_OK)
        

@api_view(['PUT'])
def CalificarSend(request):
    
    if request.method == 'PUT':
        
        arrrayLogros = request.data['logros']
            
        for value in arrrayLogros:
            
            objLogros = value
            
            query = Logroestudiante.objects.filter(idlogroestudiante = value['idlogroestudiante'], idestudiante = value['idestudiante']).first()
            
            if not query:
                
                return Response({
                    "message" : "Envio de calificacion cancelada",
                    "error" : "Logro no existe" 
                },status=status.HTTP_400_BAD_REQUEST)
            
            objLogros['estado'] = 1
            
            srCalificar = CalificarSerializer(query, data = objLogros)
        
            if srCalificar.is_valid():
                srCalificar.save()
        
        return Response({
            "message" : "Envio de calificaciones realizada con exito"
        },status=status.HTTP_200_OK)