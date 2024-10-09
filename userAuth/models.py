from django.db import models
import bcrypt

# Create your models here.

class Admin(models.Model):
    idadmin = models.AutoField(db_column='idAdmin', primary_key=True)   
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idUsuario')   

    class Meta:
        managed = False
        db_table = 'admin'

class Estudiante(models.Model):
    idestudiante = models.AutoField(db_column='idEstudiante', primary_key=True)   
    tallacamisa = models.TextField(db_column='tallaCamisa')   
    institutoprocedencia = models.TextField(db_column='institutoProcedencia')   
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idUsuario')   
    idmatricula = models.IntegerField(db_column='idMatricula')   

    class Meta:
        managed = False
        db_table = 'estudiante'

class Profesor(models.Model):
    idprofesor = models.AutoField(db_column='idProfesor', primary_key=True)   
    titulo = models.TextField()
    hojavida = models.FileField(upload_to='archivos/', max_length=512)  
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idUsuario')   
    idarea = models.IntegerField(db_column='idArea')   

    class Meta:
        managed = False
        db_table = 'profesor'
        
class Trimestres(models.Model):
    idtrimestre = models.AutoField(db_column='idTrimestre', primary_key=True)
    trimestre = models.TextField()
    descripcion = models.TextField()
    fechainicio = models.DateField(db_column='fechaInicio')
    fechafin = models.DateField(db_column='fechaFin')

    class Meta:
        managed = False
        db_table = 'trimestres'

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
    imagen = models.TextField()
    idrol = models.IntegerField(db_column='idRol')
    idsexo = models.IntegerField(db_column='idSexo')
    idtipodocumento = models.IntegerField(db_column='idTipoDocumento')
    
    class Meta:
        managed = False
        db_table = 'usuario'
    
    #FUNCION QUE ME PERMITE VALIDAR MI CONTRASEÑA
    def check_password(self, raw_password):        
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.contrasena.encode('utf-8'))