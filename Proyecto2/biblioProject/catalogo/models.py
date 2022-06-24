from django.db import models
from django.urls import reverse
import uuid
from django.utils.html import mark_safe

class Genero(models.Model):
    nombre = models.CharField(max_length=50, help_text="Ingrese el nombre del género (xej. Programación, BD, SO, etc)")

    def __str__(self):
        return self.nombre

class Autor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fechaNac = models.DateField(null=True, blank=True)
    fechaDeceso = models.DateField('Fallecido', null=True, blank=True)
    image=models.ImageField(upload_to='catalogo/upload/img', null=True, blank=True)

    # Preview de la imagen
    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="50px" height="50px" />'.format(self.image.url))
        return "Sin imagen."

    # Para eliminar imagen cuando se elimina o actualiza
    def remove_on_image_update(self):
        try:
            # is the object in the database yet?
            obj = Autor.objects.get(id=self.id)
        except Autor.DoesNotExist:
            # object is not in db, nothing to worry about
            return
        # is the save due to an update of the actual image file?
        if obj.image and self.image and obj.image != self.image:
            # delete the old image file from the storage in favor of the new file
            obj.image.delete()

    # Para eliminar imagen cuando se elimina o actualiza
    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.image.delete()
        return super(Autor, self).delete(*args, **kwargs)

    # Para eliminar imagen cuando se elimina o actualiza
    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(Autor, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Devuelve la url para acceder a un autor.
        """
        return reverse('author-details', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.apellido, self.nombre)

    class Meta:
        ordering = ["-id", "apellido", "nombre"]

class Idioma(models.Model):
    nombre = models.CharField(max_length=50, help_text="Ingrese el nombre del idioma (xej. Español, Ingles, etc)")

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.SET_NULL, null=True)
    resumen = models.TextField(max_length=1000, help_text="Ingrese un resumen del libro")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Caracteres (<a href="https://www.isbninternational.org/content/what-isbn">ISBN number</a>)')
    genero = models.ManyToManyField(Genero, help_text="Seleccione un género (o varios) para el libro")
    idioma = models.ForeignKey(Idioma, on_delete=models.SET_NULL, null=True)
    image=models.ImageField(upload_to='images', default='catalogo/upload/img/default-libro.jpg')
    
     # Para eliminar imagen cuando se elimina o actualiza
    def remove_on_image_update(self):
        try:
            # is the object in the database yet?
            obj = Libro.objects.get(id=self.id)
        except Libro.DoesNotExist:
            # object is not in db, nothing to worry about
            return
        # is the save due to an update of the actual image file?
        if obj.image and self.image and obj.image != self.image:
            # delete the old image file from the storage in favor of the new file
            obj.image.delete()

    # Para eliminar imagen cuando se elimina o actualiza
    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.image.delete()
        return super(Libro, self).delete(*args, **kwargs)
        
    # Para eliminar imagen cuando se elimina o actualiza
    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(Libro, self).save(*args, **kwargs)

    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="50" height="50" />'.format(self.image.url))
        return "Sin imagen."

    def muestra_genero(self):
        return ', '.join([genero.nombre for genero in self.genero.all()])
        # return ', '.join([genero.nombre for genero in self.genero.all()[:3]])
        
    muestra_genero.short_description = 'Género/s'

    def get_absolute_url(self):
        return reverse('book-details', args=[str(self.id)])
 
    def __str__(self):
        return self.titulo

class Ejemplar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")
    libro = models.ForeignKey(Libro, on_delete=models.SET_NULL, null=True)
    fechaDevolucion = models.DateField(null=True, blank=True)

    ESTADO_EJEMPLAR = (
        ('m', 'en Mantenimiento'),
        ('p', 'Prestado'),
        ('d', 'Disponible'),
        ('r', 'Reservado'),
    )

    estado = models.CharField(max_length=1, choices=ESTADO_EJEMPLAR, default='d', help_text='Disponibilidad del Ejemplar')
    
    def __str__(self):
        return '%s (%s)' % (self.libro, self.id)

    class Meta:
        ordering = ['libro', 'fechaDevolucion']

class POI(models.Model):
    nombre = models.CharField(max_length=255)
    lng = models.FloatField()
    lat = models.FloatField()