from django.db import models

# Create your models here.
class Areas(models.Model):
    idareas = models.AutoField(db_column='idAreas', primary_key=True)   
    nombre = models.TextField()
    descripcion = models.TextField()

    class Meta:
        managed = False
        db_table = 'areas'


class Areaslogros(models.Model):
    idareaslogros = models.AutoField(db_column='idAreasLogros', primary_key=True)   
    resultado = models.TextField()
    idareas = models.IntegerField(db_column='idAreas')   
    idlogros = models.IntegerField(db_column='idLogros')   
    idusuario = models.IntegerField(db_column='idUsuario')   

    class Meta:
        managed = False
        db_table = 'areaslogros'

class Logros(models.Model):
    idlogro = models.AutoField(db_column='idLogro', primary_key=True)
    logro = models.TextField()
    estado = models.TextField()
    observacion = models.TextField()
    idtrimestre = models.ForeignKey('Trimestres', models.DO_NOTHING, db_column='idTrimestre')
    idtipologro = models.ForeignKey('Tipologro', models.DO_NOTHING, db_column='idTipoLogro')
    idprofesor = models.ForeignKey('Profesor', models.DO_NOTHING, db_column='idProfesor')

    class Meta:
        managed = False
        db_table = 'logros'
    
    def __str__(self) -> str:
        return self.logro

class Trimestres(models.Model):
    idtrimestre = models.AutoField(db_column='idTrimestre', primary_key=True)
    trimestre = models.TextField()
    descripcion = models.TextField()
    fechainicio = models.DateField(db_column='fechaInicio')
    fechafin = models.DateField(db_column='fechaFin')
    estado = models.TextField()
    
    class Meta:
        managed = False
        db_table = 'trimestres'
        
class Profesor(models.Model):
    idprofesor = models.AutoField(db_column='idProfesor', primary_key=True)
    titulo = models.TextField()
    hojavida = models.TextField(db_column='hojaVida')
    idusuario = models.IntegerField(db_column='idUsuario')
    idarea = models.ForeignKey(Areas, models.DO_NOTHING, db_column='idArea')

    class Meta:
        managed = False
        db_table = 'profesor'

class Tipologro(models.Model):
    idtipologro = models.AutoField(db_column='idTipoLogro', primary_key=True)
    tipologro = models.TextField(db_column='tipoLogro')

    class Meta:
        managed = False
        db_table = 'tipologro'
        
class Estudiante(models.Model):
    idestudiante = models.AutoField(db_column='idEstudiante', primary_key=True)   
    tallacamisa = models.TextField(db_column='tallaCamisa')   
    institutoprocedencia = models.TextField(db_column='institutoProcedencia')   
    idusuario = models.IntegerField(db_column='idUsuario')   
    idmatricula = models.IntegerField(db_column='idMatricula')   

    class Meta:
        managed = False
        db_table = 'estudiante'

class Logroestudiante(models.Model):
    idlogroestudiante = models.AutoField(db_column='idLogroEstudiante', primary_key=True)   
    resultado = models.TextField()
    estado = models.IntegerField()
    fecha = models.DateField()
    idlogro = models.ForeignKey('Logros', models.DO_NOTHING, db_column='idLogro')   
    idestudiante = models.ForeignKey(Estudiante, models.DO_NOTHING, db_column='idEstudiante')   

    class Meta:
        managed = False
        db_table = 'logroestudiante'
        

class Informes(models.Model):
    idinforme = models.AutoField(db_column='idInforme', primary_key=True)
    informe = models.TextField()
    fecha = models.DateField()
    observacion = models.TextField()
    idestudiante = models.ForeignKey(Estudiante, models.DO_NOTHING, db_column='idEstudiante')
    
    class Meta:
        managed = False
        db_table = 'informes'