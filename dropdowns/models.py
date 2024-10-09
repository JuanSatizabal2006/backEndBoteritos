from django.db import models

# Create your models here.
class Areas(models.Model):
    idarea = models.AutoField(db_column='idArea', primary_key=True)   
    area = models.TextField()

    class Meta:
        managed = False
        db_table = 'areas'

class Eps(models.Model):
    ideps = models.AutoField(db_column='idEps', primary_key=True)   
    eps = models.TextField(db_column='eps')   

    class Meta:
        managed = False
        db_table = 'eps'

class Rh(models.Model):
    idrh = models.AutoField(db_column='idRh', primary_key=True)   
    rh = models.TextField(db_column='rh')   

    class Meta:
        managed = False
        db_table = 'rh'

class Sexo(models.Model):
    idsexo = models.AutoField(db_column='idSexo', primary_key=True) 
    sexo = models.TextField()

    class Meta:
        managed = False
        db_table = 'sexo'

class Tipodocumento(models.Model):
    idtipodocumento = models.AutoField(db_column='idTipoDocumento', primary_key=True)  
    tipodocumento = models.TextField(db_column='tipoDocumento')  

    class Meta:
        managed = False
        db_table = 'tipodocumento'
        
class Rol(models.Model):
    idrol = models.AutoField(db_column='idRol', primary_key=True)
    rol = models.TextField()

    class Meta:
        managed = False
        db_table = 'rol'
        
class Diagnostico(models.Model):
    iddiagnostico = models.AutoField(db_column='idDiagnostico', primary_key=True)
    diagnostico = models.TextField()

    class Meta:
        managed = False
        db_table = 'diagnostico'
        
class Discapacidad(models.Model):
    iddiscapacidad = models.AutoField(db_column='idDiscapacidad', primary_key=True)
    discapacidad = models.TextField()

    class Meta:
        managed = False
        db_table = 'discapacidad'

class Matriculas(models.Model):
    idmatricula = models.AutoField(db_column='idMatricula', primary_key=True)
    matricula = models.TextField()

    class Meta:
        managed = False
        db_table = 'matriculas'
        
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