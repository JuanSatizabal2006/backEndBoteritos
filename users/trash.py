"""
@api_view(['GET','POST'])

def user(request):
    #request es un objeto que contiene muchos atributos, uno de esos es method, que me retorna
    #el metodo http que se utilizó en la peticion
    
    #OBTENER TODOS LOS USUARIOS
    if request.method == 'GET':
        user = Usuarios.objects.all()
        userSerializer = UsuarioSerializer(user, many = True)
        return Response(userSerializer.data,status=status.HTTP_200_OK) 
    
    #Crear Persona y Usuario
    if request.method == 'POST':
        #print(request.data)
        
        userSerializer = UsuarioSerializer(data = request.data)

        if userSerializer.is_valid():
            userSerializer.save()
            return Response(
                {"message" : "Usuario creado" , "Usuario" : userSerializer.data }, 
                status=status.HTTP_200_OK
                )
        
        return Response(
            {"message" : "Creacion cancelada" , "error" : userSerializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
            )

@api_view(['POST', 'PUT'])
def datosMedicos(request):
    print(request.data)

    #Buscar el usuario
    idUsuario = request.data.get('idusuario')
    user = Usuario.objects.filter(idusuario = idUsuario).first()
    print(user)
    #Validar que el usuario existe
    if not user: 
            return Response({"message": "No se encontró al usuario"},status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'POST':
            
        datosMedicos = DatosMedicosSerializer(data=request.data)
        
        if datosMedicos.is_valid():
           datosMedicos.save()
           return Response(
               {"message": "¡Datos medicos registrados con exito!" , "data" : datosMedicos.data},
               status=status.HTTP_201_CREATED
               ) 
        
        return Response(
            {"message" : "¡Algo ha fallado!" , "error" : datosMedicos.errors},
            status=status.HTTP_400_BAD_REQUEST
            )
    
    if request.method == 'PUT':
        dataMedicos = Datosmedicos.objects.filter(idusuario = idUsuario).first()
        data = DatosMedicosSerializer(dataMedicos, data=request.data)
        
        if data.is_valid():
            data.save()
            return Response(
                {"message": "¡Datos medicos actualizados con exito!" , "data" : data.data},
                status=status.HTTP_201_CREATED
                ) 
        
        return Response(
            {"message" : "¡Algo ha fallado!" , "error" : datosMedicos.errors},
            status=status.HTTP_400_BAD_REQUEST
            )






@api_view(['GET'])
def datosMedicosOne(request, idUsuario):
    print(idUsuario)
    #Buscar el usuario
    oneUser = Datosmedicos.objects.filter(idusuario = idUsuario).first()
    #Validar que el usuario existe
    print(oneUser)
    if not oneUser: 
            return Response(
                {"message": "No encontrado", "error" : "No se encontraron los datos medicos de este usuario"},
                status=status.HTTP_404_NOT_FOUND
                )
    
    if request.method == 'GET':
        
        datosMedicos = DatosMedicosSerializer(oneUser)
        return Response(
            {"message" : "Datos medicos encontrados" , "data" : datosMedicos.data},
            status=status.HTTP_200_OK
            )
        
@api_view(['POST', 'PUT'])       
def historiaClinica(request):
    idUsuario = request.data.get('idusuario')
    
    #Validar usuario
    validateUser = validateIdUsuario(idUsuario)
    if not validateUser['result'] :
        return Response(validateUser['message'], status = validateUser['status'])
            
    if request.method == 'POST':
        dataHistoria = HistoriaClinicaSerializer(data = request.data)
        
        if dataHistoria.is_valid():
            dataHistoria.save()
            return Response(
                {"message": "Historia Clinica creada exitosamente", "data" : dataHistoria.data},
                status=status.HTTP_201_CREATED)
            
        return Response(
            {"message" : "Creacion sin exito", "error" : dataHistoria.errors},
            status= status.HTTP_400_BAD_REQUEST
            )
    
    if request.method == 'PUT':
        historiaClinica = Historiaclinica.objects.filter(idusuario = idUsuario).first()
        data = HistoriaClinicaSerializer(historiaClinica , data = request.data)
        
        if data.is_valid():
           data.save()
           return Response(
               {"message": "Historia Clinica actualizada exitosamente", "data" : data.data},
               status=status.HTTP_201_CREATED
               )
        return Response(
            {"message" : "Historia clinica actualizada sin exito" , "error" : data.errors },
            status= status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
def historiaClinicaOne(request, idUsuario):
    
    user = validateIdUsuario(idUsuario)
    
    if not user['result'] :
        return Response(user['message'], status = user['status'])
    
    historiaClinica = Historiaclinica.objects.filter(idusuario = idUsuario).first()
    
    if not historiaClinica:
        return Response(
            {"message" : "No se encuentra" , "error" : "Historia Clinica del usuario no encontrada"},
            status= status.HTTP_404_NOT_FOUND
        )
        
    if request.method == 'GET' : 
        historiaClinicaSeria = HistoriaClinicaSerializer(historiaClinica)
        return Response (
            {"message" : "Historia Clinica encontrada" , "data" : historiaClinicaSeria.data},
            status= status.HTTP_200_OK
        )

@api_view(['POST', 'PUT'])
def responsable(request):
    
    idUsuario = request.data.get('idusuario')
    
    #Validar usuario
    validateUser = validateIdUsuario(idUsuario)
    if not validateUser['result'] :
        return Response(validateUser['message'], status = validateUser['status'])
    
    if request.method == 'POST':
        responsableData = ResponsableSerializer(data = request.data)
        
        if responsableData.is_valid():
            responsableData.save()
            return Response(
                {"message" : "¡Responsable creado con exito!", "data" : responsableData.data},
                status=status.HTTP_201_CREATED
            ) 
            
        return Response(
            {"message" : "Creacion sin exito", "error" : responsableData.errors},
            status= status.HTTP_400_BAD_REQUEST
            )

@api_view(['GET'])
def endPointPruebas(request):
    
    if request.method == 'GET':
        query = querySql("SELECT * FROM rh", None)
        #print(query)
        return Response(query)
        
        
            #ADMINISTRADOR
            if str(idRol) == "1":
                
                otherData = {
                    'idusuario' : idUsuario
                }
                
                adminCreate = AdminSerializer(data = otherData)
                
                if adminCreate.is_valid():
                    adminCreate.save()
                    
                    return Response({
                        "message" : "¡Admin creado exitosamente!",
                        "data" : adminCreate.data
                    }, status= status.HTTP_201_CREATED)
                    
                return Response({
                    "message" : "Creacion del admin cancelada",
                    "error" : adminCreate.errors    
                })
                
            #PROFESOR
            elif str(idRol) == "2":
                
                otherData = {
                    'titulo' : request.data['titulo'],
                    'hojavida' : request.data['hojavida'],
                    'idusuario' : idUsuario,
                    'idarea' : request.data['idarea']
                }
                
                profesorCreate = ProfesorSerializer(data = otherData)
                
                if profesorCreate.is_valid():
                    profesorCreate.save()
                    
                    return Response({
                        "message" : "¡Profesor creado con exito!",
                        "data" : profesorCreate.data
                    })
                    
                return Response({
                    "message" : "Creacion del profesor cancelada",
                    "error" : profesorCreate.errors
                }) 


"""