from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import date

from ..serializers.logrosSerializer import LogrosSerializer, CalificarSerializer
from ..models import Logros, Estudiante, Logroestudiante

from helper.querySql import querySql


@api_view(['POST', 'PUT'])
def LogrosViews(request):

    #CUANDO LO CREA EL PROFESOR
    if request.method == 'POST':  
        
        if str(request.data['estado']) == "1":
            
            return Response({
                "message" : "Creacion de logro cancelada",
                "error" : "No puedes crear un logro con un estado de aceptado"
            },status=status.HTTP_406_NOT_ACCEPTABLE)
                  
        serializer = LogrosSerializer(data = request.data)
    
        if serializer.is_valid():
            serializer.save()
            
            return Response({
                "message" : "¡Logro creado con exito!",
                "data" : serializer.data
            },status=status.HTTP_201_CREATED)
        
        return Response({
            "message" : "¡Creacion del logro cancelada!",
            "error" : serializer.errors
        })
    
    #CUANDO LO RECIBE EL ADMINISTRADOR
    if request.method == 'PUT':
        id = request.data['idlogro']
        query = Logros.objects.filter(idlogro = id).first()
                
        if not query:
            return Response({
                "messsage" : "Datos vacios",
                "error" : "No se encontró el logro"
            },status=status.HTTP_404_NOT_FOUND)
        
        serializer = LogrosSerializer(query, data = request.data)
                
        #VALIDACIONES
        if serializer.is_valid():
            serializer.save()
            #SI EL ESTADO ES 1 SIGNIFICA QUE EL LOGRO FUE ACEPTADO, POR LO TANTO ES NECESARIO REALIZAR LOS INSERT EN LA TABLA LOGROESTUDIANTE PARA REALIZAR LA RESPECTIVAS CALIFICACIONES
            if str(serializer.data['estado']) == "1":
                
                #BUSCAR SI EL LOGRO YA HA SIDO ACEPTADO
                
                isAcept = Logroestudiante.objects.filter(idlogro = id)
                
                if len(isAcept) != 0:
                    return Response({
                        "message" : "Aceptacion de logro cancelada",
                        "error" : "Este logro ya ha sido aceptado con anterioridad"
                    },status=status.HTTP_400_BAD_REQUEST)
                    
                
                getAllEstudiantes = Estudiante.objects.all()
                
                nuevosLogrosEstudiantes = []
                
                # Iterar sobre los estudiantes y crear las entradas
                for estudiante in getAllEstudiantes:
                    nuevoLogroEstudiante = Logroestudiante(
                        resultado='2',  # Ajusta según lo que necesitas guardar
                        fecha=date.today(),  # Usa la fecha actual
                        idlogro=query,   # Relacionar con el logro actualizado
                        idestudiante=estudiante,  # Relacionar con cada estudiante
                        estado = '0' #Definir el estado inicial (GUARDADO)
                    )
                    nuevosLogrosEstudiantes.append(nuevoLogroEstudiante)
                
                # Insertar todas las instancias de Logroestudiante de una sola vez
                calificaciones = Logroestudiante.objects.bulk_create(nuevosLogrosEstudiantes)

                srCalificacion = CalificarSerializer(calificaciones, many = True)
            
                return Response({
                    "message" : "¡Aceptacion de logro realizada con exito!",
                    "data" : srCalificacion.data
                },status=status.HTTP_201_CREATED)    
        
            if str(serializer.data['estado']) == "0":
    
                return Response({
                    "message" : "Logro rechazado"
                },status=status.HTTP_200_OK)
                
            else:
                return Response({
                    "message" : "Estado no aceptado"
                },status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
                "message" : "Aceptacion de logros cancelada",
                "data" : serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
        

#PARA ADMIN VER TODOS LOS LOGROS CREADOS
@api_view(['GET'])
def ListLogrosAdmin(request,idtrim):

    if request.method == 'GET':
        
        query = querySql("SELECT `logros`.*, `tipologro`.`tipoLogro`, `trimestres`.`trimestre`, `profesor`.*, `areas`.`area`, CONCAT(`usuario`.`nombre`, ' ', `usuario`.`apellido`) AS `nombre` FROM `logros` LEFT JOIN `tipologro` ON `logros`.`idTipoLogro` = `tipologro`.`idTipoLogro` LEFT JOIN `trimestres` ON `logros`.`idTrimestre` = `trimestres`.`idTrimestre` LEFT JOIN `profesor` ON `logros`.`idProfesor` = `profesor`.`idProfesor` LEFT JOIN `areas` ON `profesor`.`idArea` = `areas`.`idArea` LEFT JOIN `usuario` ON `profesor`.`idUsuario` = `usuario`.`idUsuario` WHERE `trimestres`.`idTrimestre` = %s;",[idtrim])
        
        
        if len(query) == 0 :
            return Response({
                "message" : "Datos vacios",
                "error" :  ""    
            },status=status.HTTP_404_NOT_FOUND)
            
        return Response({
            "message" : "Logros encontrados",
            "data" : query
        },status=status.HTTP_200_OK)
    
#VISTA PARA LOS PROFESORES, PARA VER LOS LOGROS CREADOS POR ELLOS MISMOS    
@api_view(['GET'])
def ListLogrosProfesor(request, idtrim, idprof):
    
    if request.method == 'GET':
        query = Logros.objects.filter(idtrimestre = idtrim, idprofesor = idprof)
        
        if len(query) == 0:
            return Response({
                "message" : "Datos vacios",
                "error" : "No hay logros creados en este trimestre"
            }, status=status.HTTP_204_NO_CONTENT)
        
        serializer = LogrosSerializer(query, many = True)
        
        return Response({
            "message" : "¡Consulta exitosa!",
            "data" : serializer.data
        },status=status.HTTP_200_OK)

