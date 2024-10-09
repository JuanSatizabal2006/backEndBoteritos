from django.db import models
import bcrypt

# TODOS LOS ATRIBUTOS DE LOS MODELOS DEBEN IR EN LOWERCASE (MINUSCULAS)
class Admin(models.Model):
    idadmin = models.AutoField(db_column='idAdmin', primary_key=True)   
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idUsuario')   

    class Meta:
        managed = False
        db_table = 'admin'

class Areas(models.Model):
    idarea = models.AutoField(db_column='idArea', primary_key=True)   
    area = models.TextField()

    class Meta:
        managed = False
        db_table = 'areas'
    
    def __str__(self) -> str:
        return self.area

class Condicion(models.Model):
    idcondicion = models.AutoField(db_column='idCondicion', primary_key=True)   
    idhistoriaclinica = models.ForeignKey('Historiaclinica', models.DO_NOTHING, db_column='idHistoriaClinica')   
    iddiagnostico = models.ForeignKey('Diagnostico', models.DO_NOTHING, db_column='idDiagnostico')   
    iddiscapacidad = models.ForeignKey('Discapacidad', models.DO_NOTHING, db_column='idDiscapacidad')   

    class Meta:
        managed = False
        db_table = 'condicion'

class Datosmedicos(models.Model):
    iddatosmedicos = models.AutoField(db_column='idDatosMedicos', primary_key=True)   
    lugaratencion = models.TextField(db_column='lugarAtencion')   
    peso = models.TextField()
    altura = models.TextField()
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idUsuario')   
    ideps = models.ForeignKey('Eps', models.DO_NOTHING, db_column='idEps')   
    idrh = models.ForeignKey('Rh', models.DO_NOTHING, db_column='idRh')   

    class Meta:
        managed = False
        db_table = 'datosmedicos'

class Diagnostico(models.Model):
    iddiagnostico = models.AutoField(db_column='idDiagnostico', primary_key=True)   
    diagnostico = models.TextField()

    class Meta:
        managed = False
        db_table = 'diagnostico'

class Direccion(models.Model):
    iddireccion = models.AutoField(db_column='idDireccion', primary_key=True)   
    comuna = models.TextField()
    numero = models.TextField()
    barrio = models.TextField()
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idUsuario')   

    class Meta:
        managed = False
        db_table = 'direccion'

class Discapacidad(models.Model):
    iddiscapacidad = models.AutoField(db_column='idDiscapacidad', primary_key=True)   
    discapacidad = models.TextField()

    class Meta:
        managed = False
        db_table = 'discapacidad'

class Eps(models.Model):
    ideps = models.AutoField(db_column='idEps', primary_key=True)   
    eps = models.TextField()

    class Meta:
        managed = False
        db_table = 'eps'
        
    def __str__(self) -> str:
        return self.eps

class Estudiante(models.Model):
    idestudiante = models.AutoField(db_column='idEstudiante', primary_key=True)   
    tallacamisa = models.TextField(db_column='tallaCamisa')   
    institutoprocedencia = models.TextField(db_column='institutoProcedencia')   
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idUsuario')   
    idmatricula = models.ForeignKey('Matriculas', models.DO_NOTHING, db_column='idMatricula')   

    class Meta:
        managed = False
        db_table = 'estudiante'

class Fechas(models.Model):
    idfecha = models.AutoField(db_column='idFecha', primary_key=True)   
    fecharegistro = models.DateField(db_column='fechaRegistro')   
    fechaingreso = models.DateField(db_column='fechaIngreso')   
    fechanacimiento = models.DateField(db_column='fechaNacimiento')   
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idUsuario')   

    class Meta:
        managed = False
        db_table = 'fechas'

class Logroestudiante(models.Model):
    idlogroestudiante = models.AutoField(db_column='idLogroEstudiante', primary_key=True)   
    resultado = models.TextField()
    fecha = models.DateField()
    idlogro = models.ForeignKey('Logros', models.DO_NOTHING, db_column='idLogro')   
    idestudiante = models.ForeignKey(Estudiante, models.DO_NOTHING, db_column='idEstudiante')   

    class Meta:
        managed = False
        db_table = 'logroestudiante'

class Logros(models.Model):
    idlogro = models.AutoField(db_column='idLogro', primary_key=True)   
    logro = models.TextField()
    idtrimestre = models.ForeignKey('Trimestres', models.DO_NOTHING, db_column='idTrimestre')   
    idtipologro = models.ForeignKey('Tipologro', models.DO_NOTHING, db_column='idTipoLogro')   
    idprofesor = models.ForeignKey('Profesor', models.DO_NOTHING, db_column='idProfesor')   

    class Meta:
        managed = False
        db_table = 'logros'

class Matriculas(models.Model):
    idmatricula = models.AutoField(db_column='idMatricula', primary_key=True)   
    matricula = models.TextField()

    class Meta:
        managed = False
        db_table = 'matriculas'
        
    def __str__(self) -> str:
        return self.matricula

class Profesor(models.Model):
    idprofesor = models.AutoField(db_column='idProfesor', primary_key=True)   
    titulo = models.TextField()
    hojavida = models.FileField(upload_to='archivos/', max_length=512)  
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idUsuario')   
    idarea = models.ForeignKey(Areas, models.DO_NOTHING, db_column='idArea')   

    class Meta:
        managed = False
        db_table = 'profesor'

class Responsable(models.Model):
    idresponsable = models.AutoField(db_column='idResponsable', primary_key=True)   
    nombre = models.TextField()
    apellido = models.TextField()
    correo = models.TextField()
    numerodocumento = models.TextField(db_column='numeroDocumento')   
    telefono = models.TextField()
    profesion = models.TextField()
    ocupacion = models.TextField()
    empresa = models.TextField()
    idestudiante = models.ForeignKey(Estudiante, models.DO_NOTHING, db_column='idEstudiante')   
    idtipodocumento = models.ForeignKey('Tipodocumento', models.DO_NOTHING, db_column='idTipoDocumento')   
    idsexo = models.ForeignKey('Sexo', models.DO_NOTHING, db_column='idSexo')   
    idtipoparentesco = models.ForeignKey('Tipoparentesco', models.DO_NOTHING, db_column='idTipoParentesco')   

    class Meta:
        managed = False
        db_table = 'responsable'

class Rh(models.Model):
    idrh = models.AutoField(db_column='idRh', primary_key=True)   
    rh = models.TextField()

    class Meta:
        managed = False
        db_table = 'rh'
    
    def __str__(self) -> str:
        return self.rh

class Rol(models.Model):
    idrol = models.AutoField(db_column='idRol', primary_key=True)   
    rol = models.TextField()

    class Meta:
        managed = False
        db_table = 'rol'

class Sexo(models.Model):
    idsexo = models.AutoField(db_column='idSexo', primary_key=True)   
    sexo = models.TextField()

    class Meta:
        managed = False
        db_table = 'sexo'

class Telefonos(models.Model):
    idtelefonos = models.AutoField(db_column='idTelefonos', primary_key=True)   
    telefono1 = models.TextField()
    telefono2 = models.TextField()
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idUsuario')   

    class Meta:
        managed = False
        db_table = 'telefonos'

class Tipodocumento(models.Model):
    idtipodocumento = models.AutoField(db_column='idTipoDocumento', primary_key=True)   
    tipodocumento = models.TextField(db_column='tipoDocumento')   

    class Meta:
        managed = False
        db_table = 'tipodocumento'

class Tipologro(models.Model):
    idtipologro = models.AutoField(db_column='idTipoLogro', primary_key=True)   
    tipologro = models.TextField(db_column='tipoLogro')   

    class Meta:
        managed = False
        db_table = 'tipologro'

class Tipoparentesco(models.Model):
    idtipoparentesco = models.AutoField(db_column='idTipoParentesco', primary_key=True)   
    tipoparentesco = models.TextField(db_column='tipoParentesco')   

    class Meta:
        managed = False
        db_table = 'tipoparentesco'

class Trimestres(models.Model):
    idtrimestre = models.AutoField(db_column='idTrimestre', primary_key=True)   
    trimestre = models.TextField()
    fechainicio = models.DateField(db_column='fechaInicio')   
    fechafin = models.DateField(db_column='fechaFin')   

    class Meta:
        managed = False
        db_table = 'trimestres'


class Historiaclinica(models.Model):
    idhistoriaclinica = models.AutoField(db_column='idHistoriaClinica', primary_key=True)   
    medicamentos = models.TextField()
    restriccionesalimenticias = models.TextField(db_column='restriccionesAlimenticias')   
    archivo = models.FileField(upload_to='archivos/', max_length=512)
    observacion = models.TextField()
    idestudiante = models.ForeignKey(Estudiante, models.DO_NOTHING, db_column='idEstudiante')   

    class Meta:
        managed = False
        db_table = 'historiaclinica'

class Usuario(models.Model):
    idusuario = models.AutoField(db_column='idUsuario', primary_key=True)   
    nombre = models.TextField()
    apellido = models.TextField()
    correo = models.TextField()
    contrasena = models.TextField()
    cambiocontrasena = models.TextField(db_column='cambioContrasena')   
    documento = models.TextField()
    estado = models.TextField()
    edad = models.TextField()
    imagen = models.ImageField(upload_to='imagenes/', max_length=512)
    idrol = models.ForeignKey(Rol, models.DO_NOTHING, db_column='idRol')   
    idsexo = models.ForeignKey(Sexo, models.DO_NOTHING, db_column='idSexo')   
    idtipodocumento = models.ForeignKey(Tipodocumento, models.DO_NOTHING, db_column='idTipoDocumento')   
    #foto
    class Meta:
        managed = False
        db_table = 'usuario'
 
    def set_password(self, raw_password):
    #HASH DE CONTRASEÑA
        self.contrasena = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    #FUNCION QUE ME PERMITE VALIDAR MI CONTRASEÑA
    def check_password(self, raw_password):        
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.contrasena.encode('utf-8'))
 