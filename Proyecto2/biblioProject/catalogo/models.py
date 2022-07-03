from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from datetime import date
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"))
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

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

    # Previsualización de la imagen
    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="50px" height="50px" />'.format(self.image.url))
        return "Sin imagen."

    # Eliminar imagen fisicamente
    def remove_on_image_update(self):
        try:
            obj = Autor.objects.get(id=self.id)
        except Autor.DoesNotExist:
            return
            
        if obj.image and self.image and obj.image != self.image:
            obj.image.delete()

    def delete(self, *args, **kwargs):
        self.image.delete()

        return super(Autor, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.remove_on_image_update()

        return super(Autor, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('author-details', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.apellido, self.nombre)

    class Meta:
        ordering = ['-id', 'apellido', 'nombre']

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
    image=models.ImageField(upload_to='catalogo/upload/img', default='catalogo/upload/img/default-libro.jpg')
    
    
    # Eliminar imagen fisicamente
    def remove_on_image_update(self):
        try:
            obj = Libro.objects.get(id=self.id)
        except Libro.DoesNotExist:
            return
            
        if obj.image and self.image and obj.image != self.image:
            obj.image.delete()

    def delete(self, *args, **kwargs):
        self.image.delete()

        return super(Libro, self).delete(*args, **kwargs)
        
    def save(self, *args, **kwargs):
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
    usuario = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def es_deudor(self):
        """Determina si un usuario devolvio o no un libro prestado."""
        return bool(self.fechaDevolucion and date.today() > self.fechaDevolucion)

    def __str__(self):
        return '%s (%s)' % (self.libro, self.id)

    class Meta:
        ordering = ['libro', 'fechaDevolucion']

        permissions = (("can_reserve_a_copy", "Puede reservar ejemplar"), ("can_cancel_reservation", "Puede cancelar reserva"), ("can_view_my_loans", "Puedo ver mis prestamos"))

# class POI(models.Model):
#     usuario = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
#     nombre = models.CharField(max_length=255)
#     lng = models.FloatField()
#     lat = models.FloatField()