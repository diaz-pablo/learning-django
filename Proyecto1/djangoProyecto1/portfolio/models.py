from django.db import models

# Create your models here.
class Proyecto(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion=models.TextField()
    tecnologias = models.CharField(max_length=200)
    link= models.CharField(max_length=150)
    imagen = models.FilePathField(path='/img')