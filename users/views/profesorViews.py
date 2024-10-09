from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..models import Profesor, Usuario

from ..serialzer.profesorSerializer import ProfesorSerializer
from ..serialzer.usuarioSerializer import UsuarioSerializer
from ..serialzer.fechasSerizalizer import FechasSerializer
from ..serialzer.direccionSerializer import DireccionSerializer
from ..serialzer.datosMedicosSerializer import DatosMedicosSerializer
from ..serialzer.fechasSerizalizer import FechasSerializer
from ..serialzer.telefonosSerializer import TelefonosSerializer
from ..querySql import querySql
from url import urlHost

@api_view(['POST', 'PUT'])
def ProfesorCreateView(request):
    
    if request.method == 'POST':
        datos = request.data
        print(datos)
        #----------USUARIO----------
        serializerUsuario = UsuarioSerializer(data = datos)
        
        if not serializerUsuario.is_valid():
            return Response({
                "message" : "Creacion del usuario cancelada",
                "error" : serializerUsuario.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        serializerUsuario.save()
        
        idUsuario = serializerUsuario.data['idusuario']
        datos['idusuario'] = idUsuario
        
        #----------FECHAS----------
        serializerFechas = FechasSerializer(data = datos)
        #VALIDAMOS FECHAS
        if not serializerFechas.is_valid():
            return Response({
                "message" : "Insert en fechas cancelado",
                "erorr" : serializerFechas.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        #GUARDAMOS FECHAS
        serializerFechas.save()
        
        #----------DIRECCION----------
        direccionSerializer = DireccionSerializer(data = datos)
        if not direccionSerializer.is_valid():
            return Response({
                "message" : "Insert en direccion cancelado",
                "error" : direccionSerializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
        
        #GUARDAMOS DIRECCION
        direccionSerializer.save()
        
        #----------DATOS MEDICOS----------
        datosMedicosSerializer = DatosMedicosSerializer(data = datos)
        if not datosMedicosSerializer.is_valid():
            return Response({
                "message" : "Insert en datos medicos cancelado",
                "error" : datosMedicosSerializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
        
        datosMedicosSerializer.save()
        
        #----------TELEFONOS----------
        telefonoSerializer = TelefonosSerializer(data = datos)
        if not telefonoSerializer.is_valid():
            return Response({
                "message" : "Insert en telefonos cancelado",
                "error" : telefonoSerializer.errors
            },status=status.HTTP_400_BAD_REQUEST) 
        telefonoSerializer.save()
        
        #----------PROFESOR----------
        profesorSerializer = ProfesorSerializer(data = datos)
        if not profesorSerializer.is_valid():
            return Response({
                "message" : "Insert en tabla profesor cancelada",
                "error" : profesorSerializer.errors
            }, status= status.HTTP_400_BAD_REQUEST)
        profesorSerializer.save()  
             
        return Response({
            "usuario" : serializerUsuario.data,
            "fechas" : serializerFechas.data,
            "direccion" : direccionSerializer.data,
            "datosMedicos" : datosMedicosSerializer.data,
            "telefono" : telefonoSerializer.data,
            "profesor" : profesorSerializer.data
        }, status=status.HTTP_201_CREATED)
    
    if request.method == 'PUT':
        
        idProf = request.data.get('idprofesor')
        
        if not idProf:
            return Response({
                "message" : "Actualizacion cancelada",
                "error" : "El id del profesor es obligatorio"
            },status=status.HTTP_400_BAD_REQUEST)
     
        data = request.data
        
        #CONSULTA CON ORM QUE ME PERMITE REALIZAR UN JOIIN ENTRE LA TABLA PROFESOR Y USUARIOS
        queryProf = Profesor.objects.select_related('idusuario').filter(idprofesor=idProf).first()
        
        #VALIDAMOS QUE SE ENCUENTRE EL PROFESOR
        if not queryProf : 
            return Response({
                "message" : "Actualizacion cancelada",
                "error" : "Profesor no encontrado"
            }, status=status.HTTP_404_NOT_FOUND)
        
        #OBTENEMOS EL ID DEL USUARIO PARA CONTINUAR CON LA ACTUALIZACION
        idUsuario = queryProf.idusuario.idusuario
        
        #ASIGNAMOS EL ID DEL USUARIO YA QUE ES UN DATO NECESARIO PARA REALIZAR LA ACTUALIZACION
        data['idusuario'] = idUsuario
        
        srProf = ProfesorSerializer(queryProf, data = data)
        
        #VALIDACION
        if not srProf.is_valid():
            return Response({
                "message" : "Actualizacion cancelada",
                "error" : srProf.errors
            },status=status.HTTP_400_BAD_REQUEST)
        
        #CONSULTA AL USUARIO
        queryUsuario = Usuario.objects.filter(idusuario = idUsuario).first()
                
        srUsuario = UsuarioSerializer(queryUsuario, data = data, partial = True)
        
        if not srUsuario.is_valid():
            return Response({
                "message" : "Actualizacion cancelada",
                "error" : srUsuario.errors
            })
            
        #INSERCION DE DATOS EN AMBAS TABLAS
        srUsuario.save()
        srProf.save()
    
        return Response({
            "message" : "Actualizacion realizada con exito",
            "data" : {
                "usuario" : srUsuario.data,
                "profesor" : srProf.data
            }
        },status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT'])
def ProfesorTable(request):
    if request.method == 'GET':
        query = querySql("SELECT `profesor`.`idProfesor`, CONCAT(`usuario`.`nombre`, ' ', `usuario`.`apellido` ) AS `nombre` , `profesor`.`titulo`, `areas`.`area` FROM `profesor` LEFT JOIN `areas` ON `profesor`.`idArea` = `areas`.`idArea` LEFT JOIN `usuario` ON `profesor`.`idUsuario` = `usuario`.`idUsuario` WHERE `usuario`.`estado` = 1", [])
        
        if len(query) == 0:
            return Response({
                "message" : "Datos vacios",
                "error" : "No se encontraron profesores"
            },status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            "message" : "Profesores encontrados",
            "data" : query
        },status=status.HTTP_200_OK)
    
    #DESACTIVAR PROFESOR
    if request.method == 'PUT':
        dataProf = request.data
        
        queryProf = Profesor.objects.filter(idprofesor = dataProf['idprofesor']).first()
        
        if not queryProf:
            return Response({
                "message" : "Desactivacion cancelada",
                "error" : "Profesor no encontrado"
            },status=status.HTTP_400_BAD_REQUEST)
        
        idUsuario = queryProf.idusuario.idusuario 
                
        queryUser = Usuario.objects.filter(idusuario = idUsuario).first()
        
        if not queryUser:
            return Response({
                "message" : "Desactivacion cancelada",
                "error" : "Usuario no encontrado"
            },status=status.HTTP_400_BAD_REQUEST)
            
        srUsuario = UsuarioSerializer(queryUser, data = dataProf, partial =True)
        
        if srUsuario.is_valid():
            srUsuario.save()
            return Response({
                "message" : "Desactivacion realizada con exito",
                "data" : srUsuario.data
            },status=status.HTTP_200_OK)
            
        return Response({
            "message" : "Desactivacion cancelada",
            "error" : srUsuario.errors
        },status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
def ProfesorHead(request, idprof ,idtrim):
    
    if request.method == 'GET':

        if not idprof:
            return Response({
                "message" : "Consulta fallida",
                "error" : "El id del estudiante es obligatorio"
            },status=status.HTTP_400_BAD_REQUEST)

        if not idtrim:
            return Response({
                "message" : "Consulta fallida",
                "error" : "El id del trimestre es obligatorio"
            },status=status.HTTP_400_BAD_REQUEST)

        query = querySql("SELECT `profesor`.`idProfesor`, CONCAT(`usuario`.`nombre`, ' ', `usuario`.`apellido` ) AS `nombre` ,`usuario`.`imagen`, `usuario`.`documento`, `usuario`.`edad` ,`profesor`.`titulo`, `areas`.`area` FROM `profesor` LEFT JOIN `areas` ON `profesor`.`idArea` = `areas`.`idArea` LEFT JOIN `usuario` ON `profesor`.`idUsuario` = `usuario`.`idUsuario` WHERE `profesor`.`idProfesor` = %s;", [idprof])
        
        if len(query) == 0:
            return Response({
                "message" : "Datos vacios",
                "error" : "No se encontro el profesor"
            },status=status.HTTP_404_NOT_FOUND)
        
        data = query[0]
                
        queryLogros = querySql("SELECT `logroestudiante`.`estado`,`logroestudiante`.`idLogroEstudiante`, `logros`.`logro` FROM `logroestudiante` LEFT JOIN `logros` ON `logroestudiante`.`idLogro` = `logros`.`idLogro` WHERE `logros`.`idProfesor` = %s AND `logros`.`idTrimestre` = %s;", [idprof, idtrim])

        sumEnviados = 0
        sumGuardados = 0

        for values in queryLogros:

            if str(values["estado"]) == "1":
                sumEnviados+= 1

            if str(values["estado"]) == "0":
                sumGuardados+= 1
        
        dataHead = {
            "card1" : {
                "id": data["idprofesor"],
                "nombre": data["nombre"],
                "imagen": f"{urlHost}{data['imagen']}",
                "documento" : data["documento"],
                "edad": data["edad"]
            },
            "card2" : [
                {
                    "name" : "Titulo",
                    "value" : data["titulo"]
                },
                {
                    "name" : "Area",
                    "value" : data["area"]
                }
            ],
            "card3": [
                {
                    "name" : "Enviados",
                    "value" : sumEnviados
                },
                {
                    "name" : "Guardados",
                    "value" : sumGuardados
                }
            ]
        }

        return Response({
            "message" : "Profesores encontrados",
            "data" : dataHead
        },status=status.HTTP_200_OK)

@api_view(['GET'])
def ProfesorDataPersonal(request,id):
    
    if request.method == 'GET':
        
        query = querySql("SELECT `profesor`.*, `areas`.*, `usuario`.`nombre`,`usuario`.`apellido`, `usuario`.`correo`, `usuario`.`documento`, `usuario`.`edad`, `usuario`.`idSexo`, `usuario`.`idTipoDocumento` , `sexo`.`sexo`, `tipodocumento`.`tipoDocumento` FROM `profesor` LEFT JOIN `areas` ON `profesor`.`idArea` = `areas`.`idArea` LEFT JOIN `usuario` ON `profesor`.`idUsuario` = `usuario`.`idUsuario` LEFT JOIN `sexo` ON `usuario`.`idSexo` = `sexo`.`idSexo` LEFT JOIN `tipodocumento` ON `usuario`.`idTipoDocumento` = `tipodocumento`.`idTipoDocumento` WHERE `profesor`.`idProfesor` = %s;",[id])
        
        if len(query) == 0:
            return Response({
                "message" : "Datos vacios",
                "error" : "Datos no existen"
            },status=status.HTTP_404_NOT_FOUND)
        
        data = query[0]
        
        data['hojavida'] = f"{urlHost}{data['hojavida']}"
        
        return Response({
            "message" : "Consulta realizada con exito",
            "data" : data
        },status=status.HTTP_200_OK)
    