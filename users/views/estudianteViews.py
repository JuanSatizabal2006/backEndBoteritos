from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..serialzer.estudianteSerializer import EstudianteSerializer
from ..serialzer.usuarioSerializer import UsuarioSerializer
from ..serialzer.fechasSerizalizer import FechasSerializer
from ..serialzer.direccionSerializer import DireccionSerializer
from ..serialzer.datosMedicosSerializer import DatosMedicosSerializer
from ..serialzer.telefonosSerializer import TelefonosSerializer
from ..serialzer.logrosEstudiante import CalificarSerializer

from ..models import Estudiante, Usuario, Logroestudiante
from ..querySql import querySql
from url import urlHost

@api_view(['POST', 'PUT'])
def EstudianteCreateView(request):
    
    if request.method == 'POST':
        datos = request.data
        
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
        
        #----------DIRECCION----------
        direccionSerializer = DireccionSerializer(data = datos)
        if not direccionSerializer.is_valid():
            return Response({
                "message" : "Insert en direccion cancelado",
                "error" : direccionSerializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
        
        #----------DATOS MEDICOS----------
        datosMedicosSerializer = DatosMedicosSerializer(data = datos)
        if not datosMedicosSerializer.is_valid():
            return Response({
                "message" : "Insert en datos medicos cancelado",
                "error" : datosMedicosSerializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
        
        #----------TELEFONOS----------
        telefonoSerializer = TelefonosSerializer(data = datos)
        if not telefonoSerializer.is_valid():
            return Response({
                "message" : "Insert en telefonos cancelado",
                "error" : telefonoSerializer.errors
            },status=status.HTTP_400_BAD_REQUEST) 
        
        #----------ESTUDIANTE----------
        estudianteSerializer = EstudianteSerializer(data = datos)
        if not estudianteSerializer.is_valid():
            return Response({
                "message" : "Insert en tabla estudiante cancelada",
                "error" : estudianteSerializer.errors
            }, status= status.HTTP_400_BAD_REQUEST)
            
        #GUARDAMOS FECHAS
        serializerFechas.save()
        #GUARDAMOS DIRECCION
        direccionSerializer.save()
        datosMedicosSerializer.save()
        telefonoSerializer.save()
        estudianteSerializer.save()  
             
        return Response({
            "usuario" : serializerUsuario.data,
            "fechas" : serializerFechas.data,
            "direccion" : direccionSerializer.data,
            "datosMedicos" : datosMedicosSerializer.data,
            "telefono" : telefonoSerializer.data,
            "estudiante" : estudianteSerializer.data
        }, status=status.HTTP_201_CREATED)

    if request.method == 'PUT':
        
        idEstud = request.data.get('idestudiante')
        
        if not idEstud:
            return Response({
                "message" : "Actualizacion cancelada",
                "error" : "El id del estudiante es obligatorio"
            },status=status.HTTP_400_BAD_REQUEST)
            
        data = request.data
        #CONSULTA CON ORM QUE ME PERMITE REALIZAR UN JOIIN ENTRE LA TABLA ESTUDIANTES Y USUARIOS
        queryEstud = Estudiante.objects.select_related('idusuario').filter(idestudiante=idEstud).first()
        #VALIDAMOS QUE SE ENCUENTRE EL ESTUDIANTE
        if not queryEstud : 
            return Response({
                "message" : "Actualizacion cancelada",
                "error" : "Estudiante no encontrado"
            }, status=status.HTTP_404_NOT_FOUND)
        
        #OBTENEMOS EL ID DEL USUARIO PARA CONTINUAR CON LA ACTUALIZACION
        idUsuario = queryEstud.idusuario.idusuario
        
        #ASIGNAMOS EL ID DEL USUARIO YA QUE ES UN DATO NECESARIO PARA REALIZAR LA ACTUALIZACION
        data['idusuario'] = idUsuario
         
        srEstud = EstudianteSerializer(queryEstud, data = data)
        
        if not srEstud.is_valid():
            return Response({
                "message" : "Actualizacion cancelada",
                "error" : srEstud.errors
            },status=status.HTTP_400_BAD_REQUEST)
        
        queryUsuario = Usuario.objects.filter(idusuario = idUsuario).first()
        
        srUsuario = UsuarioSerializer(queryUsuario, data = data, partial = True)
        
        if not srUsuario.is_valid():
            return Response({
                "message" : "Actualizacion cancelada",
                "error" : srUsuario.errors
            })
        
        srEstud.save()
        srUsuario.save()
        
        return Response({
            "message" : "Actualizacion realizada con exito",
            "data" : {
                "usuario" : srUsuario.data,
                "estudiante" : srEstud.data
            }
        },status=status.HTTP_201_CREATED)

@api_view(['GET'])
def EstudianteDataPersonal(request,id):
    if request.method == 'GET':
        query = querySql("SELECT `estudiante`.*, `matriculas`.`matricula`, `usuario`.`nombre`,`usuario`.`apellido`,`usuario`.`correo`, `usuario`.`documento`,`usuario`.`idTipoDocumento`, `tipodocumento`.`tipoDocumento`, `usuario`.`edad`, `usuario`.`idSexo`,`sexo`.`sexo` FROM `estudiante` LEFT JOIN `matriculas` ON `estudiante`.`idMatricula` = `matriculas`.`idMatricula` LEFT JOIN `usuario` ON `estudiante`.`idUsuario` = `usuario`.`idUsuario` LEFT JOIN `tipodocumento` ON `usuario`.`idTipoDocumento` = `tipodocumento`.`idTipoDocumento` LEFT JOIN `sexo` ON `usuario`.`idSexo` = `sexo`.`idSexo` WHERE `estudiante`.`idEstudiante` = %s;", [id])
        
        return Response({
            "message" : "Datos encontrados",
            "datos" : query
        })

#ENDPOINT PARA LISTAR LOS ESTUDIANTES PARA LA TABLA DE ADMIN
@api_view(['GET', 'PUT'])
def EstudianteTable(request):
    
    if request.method == "GET":
        query = querySql("SELECT `idUsuario`, `idEstudiante`, `nombre`, `apellido`, `diagnostico` FROM ( SELECT `usuario`.`idUsuario`, `estudiante`.`idEstudiante`, `usuario`.`nombre`, `usuario`.`apellido`, `diagnostico`.`diagnostico` AS `diagnostico`, ROW_NUMBER() OVER (PARTITION BY `usuario`.`idUsuario` ORDER BY `usuario`.`idUsuario`) AS row_num FROM `estudiante` LEFT JOIN `usuario` ON `estudiante`.`idUsuario` = `usuario`.`idUsuario` LEFT JOIN `historiaclinica` ON `historiaclinica`.`idEstudiante` = `estudiante`.`idEstudiante` LEFT JOIN `condicion` ON `condicion`.`idHistoriaClinica` = `historiaclinica`.`idHistoriaClinica` LEFT JOIN `diagnostico` ON `condicion`.`idDiagnostico` = `diagnostico`.`idDiagnostico` WHERE `usuario`.`estado` = 1) AS subquery WHERE row_num = 1;", [])
        
        return Response(query)

    #DESACTIVAR ESTUDIANTE
    if request.method == 'PUT':
        dataEstud = request.data
        
        queryEstud = Estudiante.objects.filter(idestudiante = dataEstud['idestudiante']).first()
        
        if not queryEstud:
            return Response({
                "message" : "Desactivacion cancelada",
                "error" : "Profesor no encontrado"
            },status=status.HTTP_400_BAD_REQUEST)
        
        idUsuario = queryEstud.idusuario.idusuario 
        
        queryUser = Usuario.objects.filter(idusuario = idUsuario).first()
        
        if not queryUser:
            return Response({
                "message" : "Desactivacion cancelada",
                "error" : "Usuario no encontrado"
            },status=status.HTTP_400_BAD_REQUEST)
            
        srUsuario = UsuarioSerializer(queryUser, data = dataEstud, partial= True)
        
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

#ENDPOINT PARA MOSTRAR INFORMACION EN EL HEAD DE CADA LISTA DE ESTUDIANTES
@api_view(['GET'])
def EstudianteHeader(request,idstud,idtrim):
    
    if request.method == "GET":
        
        if not idstud:
            return Response({
                "message" : "Consulta fallida",
                "error" : "El id del estudiante es obligatorio"
            },status=status.HTTP_400_BAD_REQUEST)

        if not idtrim:
            return Response({
                "message" : "Consulta fallida",
                "error" : "El id del trimestre es obligatorio"
            },status=status.HTTP_400_BAD_REQUEST)

        #CONSULTA PARA OBTENER LOS DATOS DEL ESTUDIANTE
        query = querySql("SELECT CONCAT(`responsable`.`nombre`, ' ',`responsable`.`apellido` ) AS `responsable`,`tipoparentesco`.`tipoParentesco`, CONCAT(`usuario`.`nombre` , ' ', `usuario`.`apellido`) AS `estudiante`, `usuario`.`documento` AS `documentoestudiante`, `usuario`.`edad` AS `edadestudiante`, `usuario`.`imagen` AS `imagenestudiante`, `estudiante`.`idestudiante` FROM `estudiante` LEFT JOIN `responsable` ON `responsable`.`idEstudiante` = `estudiante`.`idEstudiante` LEFT JOIN `tipoparentesco` ON `responsable`.`idTipoParentesco` = `tipoparentesco`.`idTipoParentesco` LEFT JOIN `usuario` ON `estudiante`.`idUsuario` = `usuario`.`idUsuario` WHERE `estudiante`.`idEstudiante` = %s LIMIT 2;",[idstud])
        
        if len(query) == 0:
            return Response({
                "message" : "Consulta realizada",
                "error" : "Datos vacios"
            },status=status.HTTP_204_NO_CONTENT)
            
        infoEstudiante = query[0]
        
        #Logica para obtener obtener unicamente la informacion de los responsables del estudiante
        arrayResponsable = []
        for keysSql in query: #RECORREMOS LA CONSULTA
            objVacio = {}
            for values in keysSql:                
                if not "estudiante" in values:
                    objVacio[values] = keysSql[values] #ASIGNAMOS LOS VALORES
                
            arrayResponsable.append(objVacio)
        
        arrayModif = []

        for values in arrayResponsable:
            objVacio = {}
            #ASIGNAMOS LOS VALORES EN UN OBJETO PERSONALIZADO
            objVacio ={
                "name" : values['tipoparentesco'] ,
                "value" : values['responsable']
            }
            arrayModif.append(objVacio)

        #CONSULTA PARA OBTENER TODOS LOS LOGROS RELACIONADOS AL ESTUDIANTE
        queryLogros = querySql("SELECT `logroestudiante`.`idLogroEstudiante`, `logroestudiante`.`resultado`, `logroestudiante`.`idEstudiante` FROM `logroestudiante` LEFT JOIN `logros` ON `logroestudiante`.`idLogro` = `logros`.`idLogro` WHERE `logroestudiante`.`idEstudiante` = %s AND `logros`.`idTrimestre` =%s;", [idstud, idtrim])
        
        #VARIABLES QUE NOS AYUDARAN CON LA SUMATORIA
        sumAprobados = 0
        sumNoAprobados = 0
        sumProceso = 0

        for values in queryLogros:

            if str(values['resultado']) == '0':
                sumNoAprobados += 1 #AUTOINCREMENTAMOS LOS LOGROS NO APROBADOS

            if str(values['resultado']) == '1':
                sumAprobados += 1 #AUTOINCREMENTAMOS LOS LOGROS APROBADOS

            if str(values['resultado']) == '2':
                sumProceso += 1 #AUTOINCREMENTAMOS LOS LOGROS EN PROCESO

        dataHead = {
            'card1' : {
                "id" : infoEstudiante['idestudiante'],
                "nombre" : infoEstudiante['estudiante'],
                "imagen" : f"{urlHost}{infoEstudiante['imagenestudiante']}",
                "documento" : infoEstudiante['documentoestudiante'],
                "edad" : infoEstudiante['edadestudiante']
            },
            'card2' : arrayModif,
            'card3' : [
                  {
                    "name": "LA",
                    "value": sumAprobados,
                },
                {
                    "name": "LP",
                    "value": sumProceso,
                },
                {
                    "name": "LN",
                    "value": sumNoAprobados,
                },
            ]
        }
   
        return Response({
            "message" : "¡Consulta exitosa!",
            "data" : dataHead
        }, status=status.HTTP_200_OK)
        
