from django.db import models
from django.urls import reverse

import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from tensorflow.python.keras.models import load_model, model_from_json
from tensorflow.python.keras.initializers import glorot_uniform
from keras.utils import CustomObjectScope
from keras.applications.mobilenet import MobileNet
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input
from keras.applications import imagenet_utils
from keras import backend as K

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
    img = models.ImageField(upload_to='images')
    prediction = models.CharField(max_length=200, blank=True)


    def predict(self):
    
        K.reset_uids()
        
        model = 'sepomex/model/model_mobilenet.json'
        weights = 'sepomex/model/weights_mobilenet.h5'

        with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
            with open(model, 'r') as f:
                model = model_from_json(f.read())
                model.load_weights(weights)

        img = image.load_img(self.img, target_size=(224,224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0) 
        x = preprocess_input(x)
        result = model.predict(x)
        result_decode = imagenet_utils.decode_predictions(result)

        for (i, (predId, pred, prob)) in enumerate(result_decode[0]):
            return "{}.-  {}: {:.2f}%".format(i + 1, pred, prob * 100)


    def save(self, *args, **kwargs):
        self.prediction = self.predict()
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('list')
