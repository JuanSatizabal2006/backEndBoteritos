from django.db import connection

def querySql(consulta, data):
    with connection.cursor() as cursor:
        cursor.execute(consulta, data)
        row = cursor.fetchall()

        #OBTENEMOS UNICAMENTA LAS COLUMNAS DE LA CONSULTA
        columns = [col[0] for col in cursor.description] 
        #ARRAY VACIO QUE CONTENDRÁ LOS OBJETOS 
        arrayQuery = []
        #ITERAMOS EN LAS FILAS (DATOS)
        for item in row:
            #OBJETO VACIO QUE CONTENDRÁ LOS DATOS
            objQuery = {}
            #ITERAMOS EN CADA VALOR ESPECIFICO DE LAS FILAS, PARA OBTENER LOS DATOS UNICOS
            for i in range(len(item)):
                #ASIGNAMOS ESOS VALORES UNICOS A SUS COLUMNAS RESPECTIVAS EN EL OBJETO
                objQuery[columns[i].lower()] = item[i]
            #AÑADIMOS EL OBJETO CON TODA LA INFORMACION DE ESA FILA EN UN ARRAY
            arrayQuery.append(objQuery) 
            
    return arrayQuery