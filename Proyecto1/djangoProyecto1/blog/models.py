from django.db import models

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=30)
    
    def __str__(self):
        return self.nombre

class Posteo(models.Model):
    titulo = models.CharField(max_length=50)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)
    categorias = models.ManyToManyField(Categoria,related_name='posteos')

    def __str__(self):
        return self.titulo  

class Comentario(models.Model):
    autor = models.CharField(max_length=50)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    posteo = models.ForeignKey(Posteo,on_delete=models.CASCADE)

    
    def __str__(self):
        return self.autor + " (" + str(self.posteo.titulo) + ")"  