from django.db import models
from django.urls import reverse

class Funcion(models.Model):
    funcionid = models.AutoField(db_column='FuncionID', primary_key=True)  # Field name made lowercase.
    funcionpadreid = models.IntegerField(db_column='FuncionPadreID', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=100, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    tipofuncionid = models.IntegerField(db_column='TipoFuncionID')  # Field name made lowercase.
    activo = models.BooleanField(db_column='Activo')  # Field name made lowercase.
    metadata = models.CharField(db_column='Metadata', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    orden = models.IntegerField(db_column='Orden', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Funcion'

class Rol(models.Model):
    rolid = models.AutoField(db_column='RolID', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50)  # Field name made lowercase.
    activo = models.BooleanField(db_column='Activo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Rol'

class Rolfuncion(models.Model):
    rolfuncionid = models.AutoField(db_column='RolFuncionID', primary_key=True)  # Field name made lowercase.
    rolid = models.IntegerField(db_column='RolID')  # Field name made lowercase.
    funcionid = models.IntegerField(db_column='FuncionID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RolFuncion'

class Tipofuncion(models.Model):
    tipofuncionid = models.AutoField(db_column='TipoFuncionID', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TipoFuncion'

class Usuario(models.Model):
    usuarioid = models.AutoField(db_column='UsuarioID', primary_key=True)  # Field name made lowercase.
    pass_field = models.CharField(db_column='Pass', max_length=50)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    nombre = models.CharField(db_column='Nombre', max_length=50)  # Field name made lowercase.
    activo = models.BooleanField(db_column='Activo')  # Field name made lowercase.
    recordarme = models.BooleanField(db_column='Recordarme', blank=True, null=True)  # Field name made lowercase.
    foto = models.CharField(db_column='Foto', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    nombrecompleto = models.CharField(db_column='NombreCompleto', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return "{} - {}".format(self.usuarioid, self.nombre)
    class Meta:
        managed = False
        db_table = 'Usuario'

class Usuariorol(models.Model):
    usuariorolid = models.AutoField(db_column='UsuarioRolID', primary_key=True)  # Field name made lowercase.
    usuarioid = models.IntegerField(db_column='UsuarioID')  # Field name made lowercase.
    rolid = models.IntegerField(db_column='RolID')  # Field name made lowercase.

    def __str__(self):
        return "{} - {}".format(self.title, self.artist)

    class Meta:
        managed = False
        db_table = 'UsuarioRol'

class Classification(models.Model):
    def predict(self):
        return "empty"

    def save(self, *args, **kwargs):
        return "empty"

    def get_absolute_url(self):
        return "empty"
