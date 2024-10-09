from django.db import models
import bcrypt

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
    idrol = models.IntegerField(db_column='idRol')   
    idsexo = models.IntegerField(db_column='idSexo')   
    idtipodocumento = models.IntegerField(db_column='idTipoDocumento')   
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